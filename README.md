# gitlab-lambda-executor

**IMPORTANT: This is a Work In Progress.**

An attempt to create a Gitlab CI executor running builds into AWS lambda.

## TODO
 * find a way to get the `gitlab-ci.yml` commands from the Gitlab custom executor script (they are passed... this way `/builds/root/test"\necho $\'\\x1b[32;1m$ echo "Hello world"\\x1b[0;m\'\necho "Hello world"\necho $\'\\x1b[32;1m$ black .\\x1b[0;m\'\nblack .\n'`... so need to find a way to use that)

## Lambda configuration

### Code

Create a new Python virtualenv with your Lambda code:

```python
import os
import git
import json
import subprocess

def __main__(event, lambda_context):

    git.Git("/tmp").clone("https://oauth2:" + os.environ["ACCESS_TOKEN"] + "@YOUR_GITLAB_URL/YOUR_REPO.git")
    os.chdir("/tmp/YOUR_REPO")

    for command in event:
        #XXX: shell=True for POC only, split your commands for safe interpretation :)
        subprocess.call(command, shell=True)

    rmtree("/tmp/YOUR_REPO")
```

### Dependencies

(into your script virtualenv)

```shell
pip3 install gitpython 
```

### Archive

Create a ZIP archive and upload it to the Lambda.

```sh
zip -r9 lambda.zip YOUR_VIRTUAL_ENV/lib/python3.7/site-packages/* && 
zip -g lambda.zip main.py
```

### Environment variables

Set the environment variable `ACCESS_TOKEN` for your lambda.

This token can be generated for one of your Gitlab user.

## Gitlab runner configuration

### Runner execution script

(ensure `awscli` is callable by configuring $PATH and your IAM user has enough privileges to run serverless functions)

```sh
#!/bin/bash
aws lambda invoke
    --function-name arn:aws:lambda:eu-west-3:YOUR_ACCOUNT_ID:function:YOUR_LAMBDA_NAME output
    --payload '["echo \"Hello world\"", "black ."]'
```

### Start runner command

Start your Gitlab runner with the following command:

```sh
sudo gitlab-runner register \
    --non-interactive \
    --url https://gitlab.your-domain.com/ \
    --registration-token YOUR_TOKEN \
    --executor custom \
    --custom-run-exec=/home/ubuntu/executors/run-script.sh \
    --builds-dir=/builds \
    --cache-dir=/cache
```
