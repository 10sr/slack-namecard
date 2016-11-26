#! /usr/env/python
# -*- coding: utf-8 -*-
#
# slack_namecard.py [-t TOKEN] [-f FILE] [-u [USER [USER ...]]]

import argparse
import yaml
import json_parser
import card_maker

def main():
    # set vars
    token = ''
    user_list_file = ''
    user_list = ['']

    parser = argparse.ArgumentParser(description = 'make namecard from slack api')
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
        card_maker.make_namecard(user_info_list, team_info, template['default'])

        # make pdf for print
        card_maker.make_pdf(user_info_list, team_info, template['default'])

    else:
        print('Error: invalid token\n')

if __name__ == '__main__':
    main()
