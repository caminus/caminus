from appversion import version

def git_version(request):
    return {"app_version": version()}
