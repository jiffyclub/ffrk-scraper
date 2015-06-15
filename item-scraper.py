# -*- coding: utf-8 -*-

import argparse
from datetime import date
from urllib.parse import urljoin

import requests
from jinja2 import Template
from lxml.html import document_fromstring, tostring

EN_URL_TPL = (
    'https://ffrkstrategy.gamematome.jp/game/951/wiki/Equipment_Rarity {}')
JP_URL_TPL = (
    'https://xn--ffrk-8i9hs14f.gamematome.jp/game/780/wiki/装備品_レア{}')

PAGES = [1, 2, 3, 4, 5]

TABLE_XPATH = '//*[@id="content_block_2"]'


def get_table(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return document_fromstring(resp.text).xpath(TABLE_XPATH)[0]


def process_table(table, base_url, rarity):
    rows = table.iterchildren()
    next(rows)

    items = []

    for r in rows:
        img_cell, name_cell, type_cell, atk_cell, def_cell = r.getchildren()
        img = tostring(img_cell.find('div/a/img'), encoding='unicode')

        name_link = name_cell.find('a')
        name_link.set('href', urljoin(base_url, name_link.get('href')))
        name = tostring(name_link, encoding='unicode')

        typ = type_cell.text_content()
        atk = int(atk_cell.text)
        defense = int(def_cell.text)
        items.append([img, name, typ, rarity, atk, defense])

    return items


def write_page(data, sub):
    with open('ffrk-item.html.tpl') as f:
        tpl = f.read()

    html = Template(tpl).render(
        date=date.today().isoformat(), data=data, sub=sub)

    with open('ffrk-item-{}.html'.format(sub), 'w') as f:
        f.write(html)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Make an HTML page with a table of FFRK character stats.')
    parser.add_argument('source', choices=['en', 'jp'])
    return parser.parse_args()


def main():
    args = parse_args()

    if args.source == 'en':
        url_tpl = EN_URL_TPL
    else:
        url_tpl = JP_URL_TPL

    data = []

    for rarity in PAGES:
        table = get_table(url_tpl.format(rarity))
        data.extend(process_table(table, url_tpl, rarity))

    write_page(data, args.source)


if __name__ == '__main__':
    main()
