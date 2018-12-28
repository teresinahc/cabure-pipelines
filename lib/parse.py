import re


def parse_name(page):
    '''
    Finds and filters the name of the parliamentarian within a `page` element.
    '''

    el = page.find('./text[7]/b')
    if el is not None:
        return name_replacement.sub('', el.text)


def parse_description(description):
    '''Remove padding spaces from the description field.'''

    return description_replacement.sub('', description)


def parse_value(value):
    '''Filters the value string and parses it to a float.'''

    filtered_value = value_regex.findall(value)[0]

    return float(filtered_value.replace('.', '').replace(',', '.'))


def parse_spends_from_page(page):
    '''Iters over an element children and parses the parliamentarian spends.'''

    spends = page.findall('./text[@font="5"]')

    for i in range(0, len(spends), 2):
        yield (
            parse_description(spends[i].text),
            parse_value(spends[i + 1].text)
        )


# Unfortunaly musl has no time locales, so we need to do this.
def i18nmonth(month):
    '''
    Return the month name in portuguese given its number.

    This is needed because musl does not support locales for time.
    '''

    return [
        'Janeiro',
        'Fevereiro',
        'Marco',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
    ][int(month) - 1]


name_replacement = re.compile(r'(^ Parlamentar: )|([\s]+$)')
description_replacement = re.compile(r'(^(\s+)([IVXD]+)([\s]+))|([\s]+$)')
value_regex = re.compile(r'[\d\.,]+')
