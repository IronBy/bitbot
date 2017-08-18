from collections import namedtuple
import json
import os
import re

import requests
from slackbot.bot import respond_to
from slackbot.bot import default_reply


OK_STATUS_CODE = 200


@default_reply
def my_default_hanlder(message):
    message.reply("I'm sorry. I did not catch what you mean.")


@respond_to('^hi$', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')


@respond_to('^get prs$', re.IGNORECASE)
def getallprs(message):
    message.reply(get_prs_text())


@respond_to('^get prs (LLS-\d*)$', re.IGNORECASE)
def getallprs(message, taskId):
    message.reply(get_prs_text(taskId))


def get_prs_text(*args):
    pull_requests = read_matching_prs(*args)
    if len(pull_requests) > 0:
        return '\n'.join([get_pr_presentation(pr)
                          for pr in pull_requests])
    else:
        return 'There are no open Pull Requests'


def get_pr_presentation(pr):
    # TODO: All of the methods that interract
    # with the bitbucker API a better to be moved
    # to the separate Client class
    return ('{0}. (Reviewers: {1})'
            .format(pr.title,
                    ', '.join([format_reviewer(reviewer)
                               for reviewer in pr.reviewers])))


def format_reviewer(reviewer):
    return '{0} ({1})'.format(reviewer.user.displayName, reviewer.status)


def read_matching_prs(*args):
    return [pr
            for pr in read_open_prs()
            if len(args) == 0 or pr_matches(pr, args[0])]


def pr_matches(pr, taskId):
    return taskId.lower() in pr.title.lower()


def get_pull_requests_url(self, bitbucket_url):
    return ("https://{}/rest/api/latest/projects/LLS/repos/lyles/pull-requests"
            .format(os.environ['BITBUCKET_URL']))


def _as_object(d):
    cls_ = namedtuple('X', d.keys())
    return cls_(*d.values())


def read_open_prs():
    auth = os.environ['BITBUCKET_USERNAME'], os.environ['BITBUCKET_PASSWORD']
    response = requests.get(
        get_pull_requests_url(os.environ['BITBUCKET_URL']),
        auth=auth)
    if response.status_code != OK_STATUS_CODE:
        raise Exception("Can't read PRs. HTTP Status code is '{}'"
                        .format(response.status_code))
    else:
        return json.loads(response.text, object_hook=_as_object).values
