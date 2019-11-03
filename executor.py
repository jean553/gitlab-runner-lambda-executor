#!/usr/bin/env python3

import os
import sys
import json
import base64
import boto3

def main():

    with open(sys.argv[1]) as file:
        command = file.read()

    payload = json.dumps({
        "command": command,
        "ci_project_path": os.environ["CI_PROJECT_PATH"],
    })

    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='LAMBDA_ARN', # use your own lambda ARN here
        Payload=payload,
        LogType='Tail'
    )

    result_json = response['Payload'].read().decode('utf-8')
    result = json.loads(result_json)
    print(result["output"])

    # there was an error during the CI job, we need to tell
    # the gitlab runner the job has failed
    if result["return_code"] != 0:
        # we terminate as recommanded by gitlab documentation
        # https://docs.gitlab.com/runner/executors/custom.html#build-failure
        exit(os.environ["BUILD_FAILURE_EXIT_CODE"])

if __name__ == '__main__':
    main()
