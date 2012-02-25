import subprocess

def git_version(request):
    proc = subprocess.Popen(["git", "describe"], stdout=subprocess.PIPE)
    proc.wait()
    version = proc.stdout.read().strip()
    return {"app_version": version}
