from django.core.urlresolvers import reverse
from django import template

register = template.Library()

@register.tag
def avatar(parser, token):
    contents = token.split_contents()
    if len(contents) > 2:
        sizevar = contents[2]
    else:
        sizevar = None
    return AvatarNode(contents[1], sizevar)

class AvatarNode(template.Node):
    def __init__(self, uservar, sizevar):
        self.__user = template.Variable(uservar)
        if sizevar:
            self.__size = template.Variable(sizevar)
        else:
            self.__size = None

    def render(self, context):
        if self.__size:
            size = self.__size.resolve(context)
        else:
            size = 64
        return '<img src="%s"/>'%(reverse('minecraft.views.avatar', kwargs={'username': self.__user.resolve(context), 'size': size}),)
