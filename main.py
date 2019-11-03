import os
import stat
import git
import sys
import json
import subprocess
import stat
import shutil

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
        + os.environ["GITLAB_URL"]
        + "/"
        + event["ci_project_path"]
        + ".git",
        "/tmp/builds/root/test",
        branch=event["ci_commit_ref_name"]
    )

    script = open("/tmp/script.sh", "w")
    script.write(event["command"])
    script.close()

    st = os.stat("/tmp/script.sh")
    os.chmod("/tmp/script.sh", st.st_mode | stat.S_IEXEC)

    proc = subprocess.Popen(
        "/tmp/script.sh",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    (stdout, _) = proc.communicate()

    shutil.rmtree("/tmp/builds")
    shutil.rmtree("/tmp/cache")

    return {"return_code": proc.returncode, "output": stdout.decode("utf-8")}
