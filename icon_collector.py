#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# icon_collector.py [-t TOKEN] [-f FILE] [-u [USER [USER ...]]]

import argparse
import os
import json_parser
import urllib.request
import ssl

def get_image(url, filename):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(url, context = ctx) as res, open(filename, 'wb') as image:
            image.write(res.read())
            return 1
    except Exception:
        return -1

def icon_collect(user_info_list, team_info):
    # check team directory exist(if not, make)
    path_team_dir = '/'.join((os.path.abspath(os.path.dirname(__file__)), 'deliverable', team_info['name']))
    if not os.path.isdir(path_team_dir):
        os.makedirs(path_team_dir)

    # get team icon
    get_image(team_info['icon'], '/'.join((path_team_dir, 'logo.jpg')))

    # check icon directory exist(if not, make)
    path_icon_dir = '/'.join((path_team_dir, 'icon'))
    if not os.path.isdir(path_icon_dir):
        os.makedirs(path_icon_dir)

    # get user icon
    for user in user_info_list.values():
        get_image(user['icon'], ''.join((path_icon_dir, '/', user['name'], '.png')))

def main():
    # set vars
    token = ''
    user_list_file = ''
    user_list = []

    parser = argparse.ArgumentParser(description = 'get slack users icon')
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

    # get and parse json
    json_user, json_team = json_parser.parse_json(token)

    if json_user['ok']:
        # make user information list and team information
        user_info_list, team_info = json_parser.make_info(json_user, json_team, user_list)

        # collect icons
        icon_collect(user_info_list, team_info)

    else:
        print('Error: invalid token\n')

if __name__ == '__main__':
    main()
