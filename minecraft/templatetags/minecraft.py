from django.core.urlresolvers import reverse
from django import template

register = template.Library()

@register.tag
def avatar(parser, token):
    return AvatarNode(token.split_contents()[1])

class AvatarNode(template.Node):
    def __init__(self, uservar):
        self.__user = template.Variable(uservar)

    def render(self, context):
        return '<img src="%s"/>'%(reverse('minecraft.views.avatar', kwargs={'username': self.__user.resolve(context)}),)
