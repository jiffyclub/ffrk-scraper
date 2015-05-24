# encoding: utf-8

import csv
from urllib.request import urlopen

from lxml.html import parse

URL_TPL = (
    'https://ffrkstrategy.gamematome.jp/game/951/wiki/'
    'Character_Rankings_{}%20Ranking')

PAGES = ['Attack', 'Defense', 'Magic', 'Mind', 'HP', 'Resistance', 'Speed']

TABLE_XPATH = '//*[@id="content_block_2"]'


def get_table(url):
    with urlopen(url) as u:
        return parse(u).xpath(TABLE_XPATH)[0]


def process_name_cell(cell):
    name = cell.findtext('a')
    game = cell.text_content().lstrip(name)
    return name, game


def process_table(table):
    rows = table.iterchildren()
    next(rows)

    chars = {}

    for r in rows:
        _, _, name_cell, stat_cell = r.getchildren()
        name, game = process_name_cell(name_cell)
        stat = int(stat_cell.text)
        chars[name] = {'name': name, 'game': game, 'stat': stat}

    return chars


def write_csv(data):
    cols = ['Name', 'Game'] + PAGES
    names = sorted(data[PAGES[0]].keys())

    with open('ffrk_en.csv', 'w') as f:
        writer = csv.DictWriter(f, cols)
        writer.writeheader()

        for n in names:
            d = {
                'Name': n,
                'Game': data[PAGES[0]][n]['game'],
            }
            for p in PAGES:
                d[p] = data[p][n]['stat']
            writer.writerow(d)


def main():
    data = {}

    for stat in PAGES:
        table = get_table(URL_TPL.format(stat))
        data[stat] = process_table(table)

    write_csv(data)


if __name__ == '__main__':
    main()
