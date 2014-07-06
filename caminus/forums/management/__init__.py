from django.db.models.signals import post_syncdb
from notification import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type('forum_reply', 'Forum Reply', 'A forum post you wrote recieved a reply.')

post_syncdb.connect(create_notice_types, sender=notification)
