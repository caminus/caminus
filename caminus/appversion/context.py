from appversion import version
import platform

def git_version(request):
    return {"app_version": version()}

def server_hostname(request):
    return {'server_hostname': platform.node()}
