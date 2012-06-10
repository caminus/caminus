import badges.api
from django.contrib.auth.models import User
import pydot
import tempfile
from minecraft import download_avatar

def update_badges(user):
    inviteCount = len(user.invites.filter(claimer__isnull=False))
    if inviteCount >= 3:
        badges.api.award(user, "three_invites")
    if inviteCount >= 5:
        badges.api.award(user, "five_invites")
    if inviteCount >= 10:
        badges.api.award(user, "ten_invites")

def _user_graph(user, graph, avatarDir):
    parentNode = graph.get_node(user.username)
    if len(parentNode) == 0:
        avatar = "%s/%s.png"%(avatarDir, user.username)
        avatarFile = open(avatar, "w")
        avatarFile.write(download_avatar(user.username, 64))
        avatarFile.close()
        parentNode = pydot.Node(user.username, image=avatar)
        graph.add_node(parentNode)
    for i in user.invites.filter(claimer__isnull=False):
        node = graph.get_node(i.claimer.username)
        if len(node) == 0:
            avatar = "%s/%s.png"%(avatarDir, i.claimer.username)
            avatarFile = open(avatar, "w")
            avatarFile.write(download_avatar(i.claimer.username, 64))
            avatarFile.close()
            node = pydot.Node(i.claimer.username, image=avatar)
            graph.add_node(node)
            graph.add_edge(pydot.Edge(parentNode, node))
            _user_graph(i.claimer, graph, avatarDir)

def social_graph(userList = []):
    graph = pydot.Dot(rankdir="LR")
    avatarDir = tempfile.mkdtemp()
    if len(userList) == 0:
        userList = User.objects.all()
    for u in userList:
        _user_graph(u, graph, avatarDir)
    return graph
