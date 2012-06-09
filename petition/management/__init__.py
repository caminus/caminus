from django.db.models.signals import post_syncdb
from notification import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type('petition_closed', 'Petition Closed', 'A petition was closed.')
    notification.create_notice_type('petition_commented', 'Petition Commented', 'A petition was commented upon.')
    notification.create_notice_type('petition_opened', 'Petition Opened', 'A petition was opened.')

post_syncdb.connect(create_notice_types, sender=notification)

