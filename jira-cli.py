#!/usr/bin/env python

import json
import sys

from dateutil.parser import parse
from jira.client import JIRA, GreenHopperResource


def read(file_path):
    with open(file_path) as f:
        return f.read()


if __name__ == '__main__':
    config = json.load(open('config.json'))
    jira = JIRA(options=dict(server=config['server'],
                             agile_rest_path=GreenHopperResource.AGILE_BASE_REST_PATH),
                oauth=dict(access_token=config['access_token'],
                           access_token_secret=config['access_token_secret'],
                           consumer_key=config['consumer_key'],
                           key_cert=read('private_key.pem')))

    gh = JIRA(options=dict(server=config['server'],
                           agile_rest_path=GreenHopperResource.GREENHOPPER_REST_PATH),
              oauth=dict(access_token=config['access_token'],
                         access_token_secret=config['access_token_secret'],
                         consumer_key=config['consumer_key'],
                         key_cert=read('private_key.pem')))

    if sys.argv[1] == 'boards':
        for board in jira.boards():
            print('{:<5} {}'.format(board.id, board.name))
    elif sys.argv[1] == 'sprints':
        board_id = int(sys.argv[2])
        for sprint in jira.sprints(board_id, extended=True):
            print('{:%Y-%m-%d/%H:%M} -> {:%Y-%m-%d/%H:%M} {}'.format(parse(sprint.startDate),
                                                                     parse(sprint.endDate),
                                                                     sprint.name))
            completed = gh.completed_issues(board_id, sprint.id)
            if completed:
                print('  Completed:')
                for issue in completed:
                    print('   * {:5} {:10} {}'.format(issue.key, issue.statusName, issue.summary))
            incomplete = gh.incompleted_issues(board_id, sprint.id)
            if incomplete:
                print('  Incomplete:')
                for issue in incomplete:
                    print('   * {:5} {:10} {}'.format(issue.key, issue.statusName, issue.summary))
            print('')
