import unittest
import xml.etree.ElementTree as ET
import io
import tempfile

import luigi
from luigi.mock import MockFileSystem, MockTarget

import lib


class TestXmlParseMixin(unittest.TestCase):
    def test_parse(self):
        
        class MockTask(lib.task.XmlParseMixin):
            def input(self):
                file = io.StringIO()
                file.write('<element>1</element>')
                file.seek(0)

                class Mock:
                    def open(self, mode):
                        return file
                
                return Mock()
        
        task = MockTask()
        self.assertEqual(task.parse().__class__, ET.ElementTree)


class TestSubprocessTask(unittest.TestCase):
    def test_execution(self):
        with tempfile.NamedTemporaryFile() as f:
            infilename = f.name
        
        with tempfile.NamedTemporaryFile() as f:
            outfilename = f.name
            
        class FoobarTask(luigi.Task):
            def output(self):
                with open(infilename, 'w') as f:
                    f.write('foo bar')

                return luigi.LocalTarget(infilename)

        class MockTask(lib.task.SubprocessTask):
            command = 'cat'

            def requires(self):
                return FoobarTask()
            
            def output(self):
                return luigi.LocalTarget(outfilename)
        
        task = MockTask()
        task.run()

        self.assertEqual(open(outfilename).read(), 'foo bar')


class TestDownloadTask(unittest.TestCase):
    def test_download(self):
        class Buffer(io.BytesIO):
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        output_buffer = Buffer()
        class OutputTarget(MockTarget):
            def open(self, mode):
                wrapper = self.format.pipe_writer(output_buffer)
                return wrapper
            
        class MyDownloadTask(lib.task.DownloadTask):
            def output(self):
                return OutputTarget('output.txt', format=luigi.format.Nop)
        
        task = MyDownloadTask('https://www.locaweb.com.br/robots.txt')
        robots_txt = b'User-Agent: *'

        task.run()
        self.assertTrue(output_buffer.getvalue().startswith(robots_txt))