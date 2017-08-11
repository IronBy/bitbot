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
docker run -d --name prs_slack_bot -e SLACK_API_TOKEN=<your api toker> -e BITBUCKET_USERNAME=<BitBucket Username> -e BITBUCKET_PASSWORD=<User Password> bitbot
```

## Use Bot Commands
* `get prs` - returns list of all open Pull Requests
* `get prs <jira task id>` - returns list of all open Pull Requests for specified Jira task.

### Restrictions
The bot currently works only for one particular project in our company