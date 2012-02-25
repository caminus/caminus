import subprocess

def git_version(request):
    version = subprocess.check_output(["git", "describe"])
    return {"app_version": version}
