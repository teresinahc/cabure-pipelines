import xml.etree.ElementTree as ET
import subprocess
import urllib

import luigi


class XmlParseMixin:
    '''
    Add a parse method which parses the input and return an ElementTree
    root element.
    '''

    def parse(self):
        '''Returns an ElementTree element of the root of XML file'''

        with self.input().open('r') as infile:
            return ET.parse(infile)


class SubprocessTask(luigi.Task):
    '''
    Pipe the input to the stdin of a given command and pipes its stdout
    to the output.
    '''

    def run(self):
        with self.input().open('r') as infile:
            with self.output().open('w') as outfile:
                subprocess.run(
                    self.command.split(),
                    stdin=infile,
                    stdout=outfile,
                    text=True
                )


class DownloadTask(luigi.Task):
    '''Downloads a the content from an URL and pipes it to the output.'''

    url = luigi.Parameter()

    def run(self):
        with urllib.request.urlopen(self.url) as infile:
            with self.output().open('w') as outfile:
                outfile.write(infile.read())
