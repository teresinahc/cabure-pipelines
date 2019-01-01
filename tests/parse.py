import unittest
import xml.etree.ElementTree as ET

import lib


class TestParseName(unittest.TestCase):
    def test_parse_name(self):
        page_with_name = '''
<page>
    <text>Lorem ipsum</text>
    <text>Lorem ipsum</text>
    <text>Lorem ipsum</text>
    <text>Lorem ipsum</text>
    <text>Lorem ipsum</text>
    <text>Lorem ipsum</text>
    <text><b> Parlamentar: ASDUBRAL GOMES  </b></text>
</page>
        '''
        page = ET.fromstring(page_with_name)
        name = lib.parse.parse_name(page)

        self.assertEqual(name, 'ASDUBRAL GOMES')


class TestParseDescription(unittest.TestCase):
    def test_parse_description(self):
        description_text = ' IIV  Lorem Ipsum Dolor Sit Amet     '
        description = lib.parse.parse_description(description_text)
        self.assertEqual(description, 'Lorem Ipsum Dolor Sit Amet')


class TestParseValue(unittest.TestCase):
    def test_parse_value(self):
        value_text = '      9.000,00'
        value = lib.parse.parse_value(value_text)
        self.assertEqual(value, 9000.0)


class TestParseSpends(unittest.TestCase):
    def test_parse_spends(self):
        page_xml = '''
<page>
    <text font="5"> IV Lorem Ipsum </text>
    <text font="5">  9.000,00 </text>
    <text font="5"> XXII Lorem Ipsum Dolor </text>
    <text font="5">  90,00 </text>
</page>
        '''

        page = ET.fromstring(page_xml)
        spends = lib.parse.parse_spends_from_page(page)

        self.assertEqual(tuple(spends), (
            ('Lorem Ipsum', 9000.0),
            ('Lorem Ipsum Dolor', 90.0)
        ))


class TestMonthI18n(unittest.TestCase):
    def test_month(self):
        self.assertEqual(lib.parse.i18nmonth(1), 'Janeiro')
        self.assertEqual(lib.parse.i18nmonth(2), 'Fevereiro')
        self.assertEqual(lib.parse.i18nmonth(3), 'Marco')
        self.assertEqual(lib.parse.i18nmonth(4), 'Abril')
        self.assertEqual(lib.parse.i18nmonth(5), 'Maio')
        self.assertEqual(lib.parse.i18nmonth(6), 'Junho')
        self.assertEqual(lib.parse.i18nmonth(7), 'Julho')
        self.assertEqual(lib.parse.i18nmonth(8), 'Agosto')
        self.assertEqual(lib.parse.i18nmonth(9), 'Setembro')
        self.assertEqual(lib.parse.i18nmonth(10), 'Outubro')
        self.assertEqual(lib.parse.i18nmonth(11), 'Novembro')
        self.assertEqual(lib.parse.i18nmonth(12), 'Dezembro')