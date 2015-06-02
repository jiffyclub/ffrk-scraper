# -*- coding: utf-8 -*-

import argparse
from urllib.parse import urljoin

import requests
from jinja2 import Template
from lxml.html import document_fromstring, tostring

EN_URL_TPL = (
    'https://ffrkstrategy.gamematome.jp/game/951/wiki/'
    'Character_Rankings_{} Ranking')
JP_URL_TPL = (
    'https://xn--ffrk-8i9hs14f.gamematome.jp/game/780/wiki/'
    'キャラクター_ランキング_Lv50{}ランキング')

EN_PAGES = ['Attack', 'Defense', 'Magic', 'Mind', 'HP', 'Resistance', 'Speed']
JP_PAGES = ['攻撃', '防御', '魔力', '精神', 'HP', '魔防', '素早さ']

TABLE_XPATH = '//*[@id="content_block_2"]'


def get_table(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return document_fromstring(resp.text).xpath(TABLE_XPATH)[0]


def process_name_cell(cell, base_url):
    name_link = cell.find('a')
    name_link.set('href', urljoin(base_url, name_link.get('href')))

    game = cell.text_content().lstrip(name_link.text_content())

    return tostring(name_link, encoding='unicode'), game


def process_table(table, base_url):
    rows = table.iterchildren()
    next(rows)

    chars = {}

    for r in rows:
        _, img_cell, name_cell, stat_cell = r.getchildren()
        img = tostring(img_cell.find('a/img'), encoding='unicode')
        name, game = process_name_cell(name_cell, base_url)
        stat = int(stat_cell.text)
        chars[name] = {'name': name, 'game': game, 'stat': stat, 'img': img}

    return chars


def data_to_list(data, stat_names):
    any_key = stat_names[0]
    names = sorted(data[any_key].keys())

    data_list = []

    for char in names:
        data_list.append(
            [data[any_key][char]['img'], char, data[any_key][char]['game']] +
            [data[k][char]['stat'] for k in stat_names])

    return data_list


def write_page(data, sub):
    with open('ffrk-char.html.tpl') as f:
        tpl = f.read()

    html = Template(tpl).render(data=data, col_titles=EN_PAGES, sub=sub)

    with open('ffrk-char-{}.html'.format(sub), 'w') as f:
        f.write(html)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Make an HTML page with a table of FFRK character stats.')
    parser.add_argument('source', choices=['en', 'jp'])
    return parser.parse_args()


def main():
    args = parse_args()

    if args.source == 'en':
        pages = EN_PAGES
        url_tpl = EN_URL_TPL
    else:
        pages = JP_PAGES
        url_tpl = JP_URL_TPL

    data = {}

    for stat in pages:
        table = get_table(url_tpl.format(stat))
        data[stat] = process_table(table, url_tpl)

    data = data_to_list(data, pages)
    write_page(data, args.source)


if __name__ == '__main__':
    main()
