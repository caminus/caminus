import subprocess
from django.conf import settings

def git_version(request):
    proc = subprocess.Popen(["git", "--git-dir", settings.APPVERSION_GIT_REPO, "describe"], stdout=subprocess.PIPE)
    proc.wait()
    version = proc.stdout.read().strip()
    return {"app_version": version}
