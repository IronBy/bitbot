from slackbot.bot import respond_to
from slackbot.bot import default_reply
import re
import requests
from collections import namedtuple
import json
import os

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
  message.reply(getPrsText())

@respond_to('^get prs (LLS-\d*)$', re.IGNORECASE)
def getallprs(message, taskId):
  message.reply(getPrsText(taskId))

def getPrsText(*args):
  pullRequests = readMatchingPrs(*args)
  if len(pullRequests) > 0:
    return '\n'.join([getPrPresentation(pr) for pr in pullRequests])
  else:
    return 'There are no open Pull Requests'

def getPrPresentation(pr):
  return '{0}. (Reviewers: {1})'.format(
    pr.title,
    ', '.join([formatReviewer(reviewer) for reviewer in pr.reviewers]))

def formatReviewer(reviewer):
  return '{0} ({1})'.format(reviewer.user.displayName, reviewer.status)

def readMatchingPrs(*args):
  return [pr for pr in readOpenPrs() if len(args) == 0 or prMatches(pr, args[0])]

def prMatches(pr, taskId):
  return taskId.lower() in pr.title.lower()

def readOpenPrs():
  response = requests.get(
    "https://git.itransition.com/rest/api/latest/projects/LLS/repos/lyles/pull-requests",
    auth=(os.environ['BITBUCKET_USERNAME'], os.environ['BITBUCKET_PASSWORD']))

  if response.status_code > 200:
    raise Exception("Can't read PRs. HTTP Status code is '{}'".format(response.status_code))
  else:
    return json.loads(response.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())).values