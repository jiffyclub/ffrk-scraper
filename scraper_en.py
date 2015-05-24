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

    names, games, values = [], [], []

    for r in rows:
        _, _, name_cell, value_cell = r.getchildren()
        name, game = process_name_cell(name_cell)
        value = int(value_cell.text)
        names.append(name)
        games.append(game)
        values.append(value)

    return names, games, values


def write_csv(data):
    cols = ['Name', 'Game'] + PAGES

    with open('ffrk_en.csv', 'w') as f:
        writer = csv.DictWriter(f, cols)
        writer.writeheader()

        for i in range(len(data['names'])):
            d = {
                'Name': data['names'][i],
                'Game': data['games'][i],
            }
            for p in PAGES:
                d[p] = data[p][i]
            writer.writerow(d)


def main():
    data = {}

    for p in PAGES:
        table = get_table(URL_TPL.format(p))
        names, games, values = process_table(table)
        data['names'] = names
        data['games'] = games
        data[p] = values

    write_csv(data)


if __name__ == '__main__':
    main()
