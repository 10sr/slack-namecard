#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# card_maker.py [-t TOKEN] [-f FILE] [-u [USER [USER ...]]]

import argparse
import os
import json_parser
import icon_collector
import yaml
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from PyPDF2 import PdfFileWriter, PdfFileReader

def make_pdf(user_info_list, team_info, template):
    # check pdf directory exist(if not, make)
    path_team_dir = '/'.join((os.path.abspath(os.path.dirname(__file__)), 'deliverable', team_info['name']))
    path_card_dir = '/'.join((path_team_dir, 'namecard'))
    path_pdf_dir = '/'.join((path_team_dir, 'pdf'))
    if not os.path.isdir(path_pdf_dir):
        os.makedirs(path_pdf_dir)

    base = Image(width = template['width'] * 2, height = template['height'] * 5)

    # make dummy cards pdf
    path_dummy_card = '/'.join((path_team_dir, 'dummy.png'))
    if os.path.isfile(path_dummy_card):
        cards_base = base.clone()
        dummy = Image(filename = path_dummy_card)
        for i in range(10):
            cards_base.composite(dummy, dummy.width * (i % 2), dummy.height * (i // 2))
        cards_base.save(filename = '/'.join((path_team_dir, 'dummy.pdf')))

    # split users by 10
    pdf_list = []
    sorted_users = sorted(user_info_list)
    while sorted_users != []:
        pdf_list.append(sorted_users[0:10])
        del(sorted_users[0:10])

    # make user cards pdf
    path_output_pdf = ''.join((path_team_dir, '/', team_info['name'], '.pdf'))
    output_pdf = PdfFileWriter()
    for j, users in enumerate(pdf_list):
        cards_base = base.clone()
        for i, name in enumerate(users):
            path_user_card = ''.join((path_card_dir, '/', name, '.png'))
            if os.path.isfile(path_user_card):
                card = Image(filename = path_user_card)
                cards_base.composite(card, card.width * (i % 2), card.height * (i // 2))
        path_tmp_pdf = ''.join((path_pdf_dir, '/', str(j), '.pdf'))
        cards_base.save(filename = path_tmp_pdf)
        input_pdf = PdfFileReader(open(path_tmp_pdf, 'rb'))
        output_pdf.addPage(input_pdf.getPage(0))

    with open(path_output_pdf, 'wb') as output_file:
        output_pdf.write(output_file)
    

def make_namecard(user_info_list, team_info, template):
    # check team directory exist(if not, make)
    path_team_dir = '/'.join((os.path.abspath(os.path.dirname(__file__)), 'deliverable', team_info['name']))
    if not os.path.isdir(path_team_dir):
        os.makedirs(path_team_dir)

    # check icon directory exist(if not, make)
    path_icon_dir = '/'.join((path_team_dir, 'icon'))
    if not os.path.isdir(path_icon_dir):
        os.makedirs(path_icon_dir)

    # check namecard directory exist(if not, make)
    path_card_dir = '/'.join((path_team_dir, 'namecard'))
    if not os.path.isdir(path_card_dir):
        os.makedirs(path_card_dir)

    # make plain card
    base = Image(width = template['width'], height = template['height'], background = Color('rgb(255, 255, 255)'))
    frame = Drawing()
    frame.stroke_color = Color('rgb(0, 0, 0)')
    frame.fill_color = Color('rgba(255, 255, 255, 0)')
    frame.rectangle(left = 0, top = 0, width = base.width - 1, height = base.height - 1)
    frame(base)

    # draw team logo
    if template['logo']['display']:
        # check team icon exist offline(if not, get)
        path_logo_file = ''.join((path_team_dir, '/logo.jpg'))
        if not os.path.isfile(path_logo_file):
            icon_collector.get_image(team_info['icon'], path_logo_file)
        logo_draw = Image(filename = path_logo_file)
        logo_draw.resize(template['logo']['size'], template['logo']['size'])
        if template['logo']['align'] == 'left':
            logo_left = template['logo']['x']
        elif template['logo']['align'] == 'center':
            logo_left = template['logo']['x'] - int(template['logo']['size'] / 2)
        elif template['logo']['align'] == 'right':
            logo_left = template['logo']['x'] - template['logo']['size']
        logo_top = template['logo']['y']
        base.composite(logo_draw, logo_left, logo_top)

    # draw team name
    if template['team']['display']:
        team_draw = Drawing()
        if template['team']['font'] != 'default':
            team_draw.font = template['team']['font']
        if template['team']['size'] != 'default':
            team_draw.font_size = template['team']['size']
        mtr_team = team_draw.get_font_metrics(base, team_info['name'])
        if template['team']['align'] == 'left':
            team_left = template['team']['x']
        elif template['team']['align'] == 'center':
            team_left = template['team']['x'] - int(mtr_team.text_width / 2)
        elif template['team']['align'] == 'center':
            team_left = template['team']['x'] - int(mtr_team.text_width)
        team_top = template['team']['y'] + int(mtr_team.ascender)
        team_draw.text(team_left, team_top, team_info['name'])
        team_draw(base)

    #save dummy card
    base.save(filename = ''.join((path_team_dir, '/dummy.png')))

    for user in user_info_list.values():
        base_clone = base.clone()
        # draw user icon
        if template['icon']['display']:
            # check user icon exist offline(if not, get)
            path_icon_file = ''.join((path_icon_dir, '/', user['name'], '.png')) 
            if not os.path.isfile(path_icon_file):
                icon_collector.get_image(user['icon'], path_icon_file)
            icon_draw = Image(filename = path_icon_file)
            icon_draw.resize(template['icon']['size'], template['icon']['size'])
            if template['icon']['align'] == 'left':
                icon_left = template['icon']['x']
            elif template['icon']['align'] == 'center':
                icon_left = template['icon']['x'] - int(template['icon']['size'] / 2)
            elif template['icon']['align'] == 'right':
                icon_left = template['icon']['x'] - template['icon']['size']
            icon_top = template['icon']['y']
            base_clone.composite(icon_draw, icon_left, icon_top)

        # draw real name
        if template['real']['display']:
            real_draw = Drawing()
            if template['real']['font'] != 'default':
                real_draw.font = template['real']['font']
            if template['real']['size'] != 'default':
                real_draw.font_size = template['real']['size']
            user_real_name = user['real_name']
            mtr_real = real_draw.get_font_metrics(base_clone, user_real_name)
            if mtr_real.text_width > template['real']['width']:
                user_real_name = user['real_name'].replace(' ', '\n')
                mtr_real = real_draw.get_font_metrics(base_clone, user_real_name)
            if template['real']['align'] == 'left':
                real_left = template['real']['x']
            elif template['real']['align'] == 'center':
                real_left = template['real']['x'] - int(mtr_real.text_width / 2)
            elif template['real']['align'] == 'center':
                real_left = template['real']['x'] - int(mtr_real.text_width)
            real_top = template['real']['y'] + int(mtr_real.ascender)
            real_draw.text(real_left, real_top, user_real_name)
            real_draw(base_clone)

        # draw name
        if template['name']['display']:
            name_draw = Drawing()
            if template['name']['font'] != 'default':
                name_draw.font = template['name']['font']
            if template['name']['size'] != 'default':
                name_draw.font_size = template['name']['size']
            user_name = ''.join(('@', user['name']))
            mtr_name = name_draw.get_font_metrics(base_clone, user_name)
            if template['name']['align'] == 'left':
                name_left = template['name']['x']
            elif template['name']['align'] == 'center':
                name_left = template['name']['x'] - int(mtr_name.text_width / 2)
            elif template['name']['align'] == 'center':
                name_left = template['name']['x'] - int(mtr_name.text_width)
            name_top = template['name']['y'] + int(mtr_name.ascender)
            name_draw.text(name_left, name_top, user_name)
            name_draw(base_clone)

        # draw title
        if template['title']['display']:
            title_draw = Drawing()
            if template['title']['font'] != 'default':
                title_draw.font = template['title']['font']
            if template['title']['size'] != 'default':
                title_draw.font_size = template['title']['size']
            user_title = user['title']
            mtr_title = title_draw.get_font_metrics(base_clone, user_title)
            if template['title']['align'] == 'left':
                title_left = template['title']['x']
            elif template['title']['align'] == 'center':
                title_left = template['title']['x'] - int(mtr_title.text_width / 2)
            elif template['title']['align'] == 'center':
                title_left = template['title']['x'] - int(mtr_title.text_width)
            title_top = template['title']['y'] + int(mtr_title.ascender)
            title_draw.text(title_left, title_top, user_title)
            title_draw(base_clone)

        base_clone.save(filename = ''.join((path_card_dir, '/', user['name'], '.png')))

def main():
    # set vars
    token = ''
    user_list_file = ''
    user_list = []

    parser = argparse.ArgumentParser(description = 'make namecard image')
    parser.add_argument('-t', '--token', default = '', help = 'slack api token')
    parser.add_argument('-f', '--file', default = '', help = 'user list file')
    parser.add_argument('-u', '--user', nargs = '*', default = [], help = 'user list')
    args = parser.parse_args()
    if args.token != '':
        token = args.token
    if args.file != '':
        user_list_file = args.file
    if args.user != []:
        user_list = args.user

    if user_list_file != '':
        with open(user_list_file) as f:
            for user in f.readlines():
                user_list.append(user.replace('\n', ''))

    with open('template.yaml', 'r') as f:
        template = yaml.load(f)

    # get and parse json
    json_user, json_team = json_parser.parse_json(token)

    if json_user['ok']:
        # make user information list and team information
        user_info_list, team_info = json_parser.make_info(json_user, json_team, user_list)

        # make namecard
        make_namecard(user_info_list, team_info, template['default'])

    else:
        print('Error: invalid token\n')

if __name__ == '__main__':
    main()

