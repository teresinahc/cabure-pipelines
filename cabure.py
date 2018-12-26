'''
Data pipelines of Piaui's Legislative Assembly parliamentaries spends.
'''

import datetime
import locale

import luigi
from luigi.contrib import postgres
from decouple import config

import lib

PDFTOHTML_COMMAND = '/usr/bin/pdftohtml -xml -stdout -i - /dev/null'
BASE_PDF_URL = 'http://ccheque.hospedagemdesites.ws/transparencia/verbas/{date:%Y/%m%%s/cota_parlamentar%m%Y}.pdf'


class DownloadPDFTask(lib.task.DownloadTask):
    '''Download a report PDF for a given `validity` month.'''

    validity = luigi.parameter.MonthParameter()

    def output(self):
        return luigi.LocalTarget(
            'data/{date:%m-%Y}/cota-parlamentar.pdf'.format(date=self.validity),
            format=luigi.format.Nop
        )


class PdfToXml(lib.task.SubprocessTask):
    '''Converts a PDF to a XML format in order to parse it.'''

    command = PDFTOHTML_COMMAND
    base_url = BASE_PDF_URL

    validity = luigi.parameter.MonthParameter()

    def requires(self):
        return DownloadPDFTask(
            validity=self.validity,
            url=self.base_url.format(date=self.validity) % lib.parse.i18nmonth(self.validity.month)
        )
    
    def output(self):
        return luigi.LocalTarget('data/{date:%m-%Y}/cota-parlamentar.xml'.format(date=self.validity))


class DumpMonthSpendsTask(luigi.Task, lib.task.XmlParseMixin):
    '''Parse the monthly spends and dumps it into a CSV file.'''

    validity = luigi.parameter.MonthParameter()

    def requires(self):
        return PdfToXml(validity=self.validity)
    
    def output(self):
        return luigi.LocalTarget(
            'data/{date:%m-%Y}/spends.csv'.format(date=self.validity),
            format=lib.format.CSVFormat(
                delimiter=';',
                columns=('name', 'description', 'value')
            )
        )
    
    def run(self):
        with self.output().open('w') as outfile:
            for page in self.parse().findall('./page'):
                name = lib.parse.parse_name(page)
                for description, value in lib.parse.parse_spends_from_page(page):
                    outfile.write(name, description, value)                


class CopyMonthToPostgresTask(postgres.CopyToTable):
    '''Copy the CSV rows into a PostgreSQL table'''

    validity = luigi.parameter.MonthParameter(default=datetime.date.today())

    host = config('DB_HOST', default='')
    database = config('DB_NAME', default='')
    user = config('DB_USER', default='')
    password = config('DB_PASSWORD', default='')
    table = 'spends'

    columns = [
        ('congressman', 'VARCHAR(40)'),
        ('description', 'TEXT'),
        ('value', 'FLOAT'),
        ('validity', 'DATE')
    ]

    def requires(self):
        return DumpSpendsTask(validity=self.validity)
    
    def rows(self):
        with self.input().open('r') as infile:
            for row in infile:
                yield row + (self.validity,)


class RunForYear(luigi.Task):
    '''Dump reports for a entire year'''

    year = luigi.parameter.YearParameter()

    def requires(self):
        for i in range(12):
            yield DumpMonthSpendsTask(validity=self.year.replace(month=i + 1))

    def output(self):
        return luigi.LocalTarget(
            'data/year-report-{date:%Y}.csv'.format(date=self.year),
            format=lib.format.CSVFormat(
                delimiter=';',
                columns=('name', 'description', 'value', 'month')
            )
        )
    
    def run(self):
        with self.output().open('w') as outfile:
            i = 1
            for month in self.input():
                validity = '{date:%m/%Y}'.format(date=self.year.replace(month=i))
                with month.open('r') as infile:
                    rows = iter(infile)
                    next(rows) # dumping header

                    for row in rows:
                        row_with_validity = tuple(row) + (validity,)
                        outfile.write(*row_with_validity)
                
                i += 1