import csv
import io

import luigi.format

class CSVInputProcessor:
    '''
    luigi input processor for CSV files
    '''

    def __init__(self, input_pipe, delimiter=',', columns=None):
        self.input_pipe = input_pipe
        self.columns = columns
        self.reader = csv.reader(input_pipe, delimiter=delimiter)

        if columns is not None:
            self.header = next(self.reader)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        # TODO: abort when catching an error
        self.input_pipe.close()
    
    def __iter__(self):
        if self.columns is not None:
            yield self.header
        
        for line in self.reader:
            yield tuple(line)


class CSVOutputProcessor:
    '''
    luigi output processor for CSV files
    '''

    def __init__(self, output_pipe, delimiter=',', columns=None):
        self.output_pipe = output_pipe
        self.columns = columns
        self.writer = csv.writer(output_pipe, delimiter=delimiter)

        if columns is not None:
            self.writer.writerow(columns)
    
    def write(self, *args):
        self.writer.writerow(args)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        # TODO: abort when catching an error
        self.output_pipe.close()


class CSVFormat(luigi.format.TextFormat):
    '''
    CSV file format for luigi

    Args:
        delimiter (str): The CSV value delimiter
        columns  (iter): A iterable over the values of the column names
    '''

    def __init__(self, delimiter=',', columns=None):
        self.columns = columns
        self.delimiter = delimiter
    
    def pipe_reader(self, input_pipe):
        return CSVInputProcessor(
            io.TextIOWrapper(input_pipe),
            delimiter=self.delimiter,
            columns=self.columns
        )
    
    def pipe_writer(self, output_pipe):
        return CSVOutputProcessor(
            io.TextIOWrapper(output_pipe),
            delimiter=self.delimiter,
            columns=self.columns
        )