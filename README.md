# gitlab-lambda-executor

**IMPORTANT: This is a Work In Progress.**

An attempt to create a Gitlab CI executor running builds into AWS lambda.

## Lambda configuration

### Code

Create a new Python virtualenv with your Lambda code:

```python
import os
import stat
import git
import sys
import json
import subprocess
import stat

from git import Repo


def __main__(event, lambda_context):

    os.mkdir("/tmp/builds")
    os.mkdir("/tmp/cache")

    print("Cloning the project")
    Repo.clone_from(
        "https://oauth2:"
        + os.environ["ACCESS_TOKEN"]
        + "@YOUR_GITLAB_URL.git",
        "/tmp/builds/root/test",
    )

    script = open("/tmp/script.sh", "w")
    script.write(event)
    script.close()

    st = os.stat("/tmp/script.sh")
    os.chmod("/tmp/script.sh", st.st_mode | stat.S_IEXEC)

    proc = subprocess.Popen(
        "/tmp/script.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output = proc.stdout.read()
    error = proc.stderr.read()

    return output + error
```

### Dependencies

(into your script virtualenv)

```shell
pip3 install gitpython black 
```

### Archive

Ensure `black` can be accessed from your archive root directory.

```sh
cp YOUR_VIRTUAL_ENV/bin/black .
```

Create a ZIP archive and upload it to the Lambda.

```sh
zip -r9 lambda.zip YOUR_VIRTUAL_ENV/lib/python3.7/site-packages/* && 
zip -g lambda.zip main.py &&
zip -g lambda.zip black
```

### Environment variables

Set the environment variable `ACCESS_TOKEN` for your lambda.

This token can be generated for one of your Gitlab user.

## Gitlab runner configuration

### Runner execution script

(ensure `awscli` is callable by configuring $PATH and your IAM user has enough privileges to run serverless functions)

```python
import os
import sys
import boto3
import json
import base64

with open(sys.argv[1]) as file:
    command = file.read()

payload = json.dumps(command)

client = boto3.client('lambda')
response = client.invoke(
    FunctionName='arn:aws:lambda:eu-west-3:538175400773:function:test',
    Payload=payload,
    LogType='Tail'
)

result = response['Payload'].read().decode('utf-8')
print(result)
```

### Start runner command

Start your Gitlab runner with the following command:

```sh
sudo gitlab-runner register \
    --non-interactive \
    --url https://gitlab.your-domain.com/ \
    --registration-token YOUR_TOKEN \
    --executor custom \
    --custom-run-exec=/home/ubuntu/executors/run-script.py \
    --builds-dir=/tmp/builds \
    --cache-dir=/tmp/cache
```
