import os
import stat
import git
import sys
import json
import subprocess
import stat

from git import Repo

def __main__(
    event,
    lambda_context,
):

    os.mkdir("/tmp/builds")
    os.mkdir("/tmp/cache")

    Repo.clone_from(
        "https://oauth2:"
        + os.environ["ACCESS_TOKEN"]
        + "@"
        + os.environ["GITLAB_REPOSITORY_URL"],
        "/tmp/builds/root/test",
    )

    script = open("/tmp/script.sh", "w")
    script.write(event)
    script.close()

    st = os.stat("/tmp/script.sh")
    os.chmod("/tmp/script.sh", st.st_mode | stat.S_IEXEC)

    proc = subprocess.Popen(
        "/tmp/script.sh",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = proc.stdout.read()
    error = proc.stderr.read()

    return output + error
