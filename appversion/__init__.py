from django.conf import settings
import subprocess
def version():
    proc = subprocess.Popen(["git", "--git-dir", settings.APPVERSION_GIT_REPO, "describe"], stdout=subprocess.PIPE)
    proc.wait()
    version = proc.stdout.read().strip()
    return version
