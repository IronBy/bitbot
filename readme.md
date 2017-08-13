# Description
This is a Slack bot which is based on [this bot](https://github.com/lins05/slackbot). It returns information about Pull Requests for a project.
The bot runs in Windows based Docker container.

# Usage

## Build Docker Image
From current folder run
```powershell
docker build -t bitbot .
```

## Run Container
```powershell
docker run -d --name prs_slack_bot -e SLACK_API_TOKEN=<your api toker> -e BITBUCKET_USERNAME=<BitBucket Username> -e BITBUCKET_PASSWORD=<User Password> -e BITBUCKET_URL=<base url to BitBucket> bitbot
```
'base url to BitBucket' should not contain either 'http' or 'https'. It's just domain and port (if necessary)

## Use Bot Commands
* `get prs` - returns list of all open Pull Requests
* `get prs <jira task id>` - returns list of all open Pull Requests for specified Jira task.

### Restrictions
The bot currently works only for one particular project in our company