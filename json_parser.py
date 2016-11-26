#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# json_parser.py

import urllib.request
import ssl
import json

def parse_json(token):
    url = 'https://slack.com/api/'
    query_user = ''.join((url, 'users.list?token=', token))
    query_team = ''.join((url, 'team.info?token=', token))
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    json_user = json.loads(urllib.request.urlopen(query_user, context = ctx).read().decode('utf-8'))
    json_team = json.loads(urllib.request.urlopen(query_team, context = ctx).read().decode('utf-8'))

    return json_user, json_team

def make_info(json_user, json_team, user_list):
    # make user info list
    user_info_list = {}
    if user_list != []:
        for user in user_list:
            for user_info in json_user['members']:
                if user_info['name'] == user:
                    # seach largest icon url
                    if 'image_original' in user_info['profile']:
                        icon_url = user_info['profile']['image_original']
                    elif 'image_1024' in user_info['profile']:
                        icon_url = user_info['profile']['image_1024']
                    elif 'image_512' in user_info['profile']:
                        icon_url = user_info['profile']['image_512']
                    elif 'image_192' in user_info['profile']:
                        icon_url = user_info['profile']['image_192']
                    user_info_list[user] = {
                            'name': user_info['name'],
                            'real_name': user_info['profile']['real_name'],
                            'title': user_info['profile']['title'],
                            'icon': icon_url
                            }
            # user is not exist
            if user not in user_info_list:
                print(''.join((user, ' is not exist in ', json_team['team']['name'] ,'.\n')))

    # make team info
    team_info = {
            'name': json_team['team']['name'],
            'icon': json_team['team']['icon']['image_original']
            }

    return user_info_list, team_info

def main():
    print('it does not be used independently.\n')

if __name__ == '__main__':
    main()
