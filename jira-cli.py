#!/usr/bin/env python

import json
import sys

from jira.client import GreenHopper


def read(file_path):
    with open(file_path) as f:
        return f.read()


if __name__ == '__main__':
    config = json.load(open('config.json'))
    jira = GreenHopper(options={'server': config['server']},
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
            print('{} {} {}'.format(sprint.startDate, sprint.endDate, sprint.name))
            completed = jira.completed_issues(board_id, sprint.id)
            if completed:
                print('  Completed:')
                for issue in completed:
                    print('   * {:5} {:10} {}'.format(issue.key, issue.statusName, issue.summary))
            incomplete = jira.incompleted_issues(board_id, sprint.id)
            if incomplete:
                print('  Incomplete:')
                for issue in incomplete:
                    print('   * {:5} {:10} {}'.format(issue.key, issue.statusName, issue.summary))
            print('')
