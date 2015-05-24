# encoding: utf-8

from urllib.parse import urljoin
from urllib.request import urlopen

from jinja2 import Template
from lxml.html import parse, tostring

URL_TPL = (
    'https://ffrkstrategy.gamematome.jp/game/951/wiki/'
    'Character_Rankings_{}%20Ranking')

PAGES = ['Attack', 'Defense', 'Magic', 'Mind', 'HP', 'Resistance', 'Speed']

TABLE_XPATH = '//*[@id="content_block_2"]'


def get_table(url):
    with urlopen(url) as u:
        return parse(u).xpath(TABLE_XPATH)[0]


def process_name_cell(cell):
    name_link = cell.find('a')
    name_link.set('href', urljoin(URL_TPL, name_link.get('href')))

    game = cell.text_content().lstrip(name_link.text_content())

    return tostring(name_link, encoding='unicode'), game


def process_table(table):
    rows = table.iterchildren()
    next(rows)

    chars = {}

    for r in rows:
        _, img_cell, name_cell, stat_cell = r.getchildren()
        img = tostring(img_cell.find('a/img'), encoding='unicode')
        name, game = process_name_cell(name_cell)
        stat = int(stat_cell.text)
        chars[name] = {'name': name, 'game': game, 'stat': stat, 'img': img}

    return chars


def data_to_list(data):
    names = sorted(data[PAGES[0]].keys())

    data_list = []

    for char in names:
        data_list.append(
            [data[PAGES[0]][char]['img'], char, data[PAGES[0]][char]['game']] +
            [data[k][char]['stat'] for k in PAGES])

    return data_list


def write_page(data):
    with open('ffrk-en.html.tpl') as f:
        tpl = f.read()

    html = Template(tpl).render(data=data, col_titles=PAGES)

    with open('ffrk-en.html', 'w') as f:
        f.write(html)


def main():
    data = {}

    for stat in PAGES:
        table = get_table(URL_TPL.format(stat))
        data[stat] = process_table(table)

    data = data_to_list(data)
    write_page(data)


if __name__ == '__main__':
    main()
