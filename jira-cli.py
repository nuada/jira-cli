#!/usr/bin/env python

import json
import sys
import unicodedata

from dateutil.parser import parse
from jira.client import JIRA


USAGE = '''usage: jira-cli.py <command>

Commands:
    * boards              - list all Agile boards
    * sprints <boadrd_id> - list all sprints and issues for a board
'''


def read(file_path):
    with open(file_path) as f:
        return f.read()


def normalize(u):
    return unicodedata.normalize('NFKD', u).encode('ascii', 'ignore')


if __name__ == '__main__':
    config = json.load(open('config.json'))
    options = dict(server=config['server'])
    auth = dict(access_token=config['access_token'],
                access_token_secret=config['access_token_secret'],
                consumer_key=config['consumer_key'],
                key_cert=read('private_key.pem'))
    jira = JIRA(options=options, oauth=auth)

    if len(sys.argv) == 1:
        print(USAGE)
    elif sys.argv[1] == 'boards':
        for board in jira.boards():
            print('{:<5} {}'.format(board.id, board.name))
    elif sys.argv[1] == 'sprints':
        board_id = int(sys.argv[2])
        for sprint in jira.sprints(board_id, extended=True):
            dates = ''
            if sprint.state != 'future':
                dates = '{:%Y-%m-%d/%H:%M} -> {:%Y-%m-%d/%H:%M}'.format(parse(sprint.startDate),
                                                                           parse(sprint.endDate))
            print('{} {:36} {}'.format(sprint.state, dates, sprint.name))
            for issue in jira.search_issues('Sprint={} ORDER BY key'.format(sprint.id)):
                 print('   * {:6} {:11} {}'.format(issue.key, issue.fields.status, normalize(issue.fields.summary)))
            print('')
