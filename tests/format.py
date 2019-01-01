import unittest
import io
import tempfile

import lib


class TestCSVFormat(unittest.TestCase):
    def test_csv_format_input(self):
        format = lib.format.CSVFormat()
        buffer_io = io.BytesIO()
        buffer_io.write(b'foo,bar,with,123\n')
        buffer_io.seek(0)
        
        with format.pipe_reader(buffer_io) as buffer:
            line = next(iter(buffer))
            
        self.assertEqual(line, ('foo', 'bar', 'with', '123'))
      
    def test_csv_format_output(self):
        format = lib.format.CSVFormat()

        with tempfile.NamedTemporaryFile() as f:
            filename = f.name

        buffer_io = io.FileIO(filename, mode='w+b')
      
        with format.pipe_writer(buffer_io) as buffer:
            buffer.write('foo', 'bar', 'with', '123')

        self.assertEqual(open(filename).read(), 'foo,bar,with,123\n')
