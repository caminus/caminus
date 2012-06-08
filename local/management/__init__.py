from django.db.models.signals import post_syncdb
from notification import models as notification
import badges.api
import badges.models
from local import update_badges
from django.contrib.auth.models import User

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("invite_accepted", "Invite Accepted", "An invitation you sent has been accepted.")

post_syncdb.connect(create_notice_types, sender=notification)

def create_invite_badges(app, created_models, verbosity, **kwargs):
    badges.api.create_badge("three_invites", "Three Invites", "You invited three people")
    badges.api.create_badge("five_invites", "Five Invites", "You invited five people")
    badges.api.create_badge("ten_invites", "Ten Invites", "You invited ten people")
    for u in User.objects.all():
        update_badges(u)

post_syncdb.connect(create_invite_badges, sender=badges.models)
