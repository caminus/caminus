from django.db.models.signals import post_syncdb
from notification import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("donation_paid", "Donation Recieved", "A donation was made")

post_syncdb.connect(create_notice_types, sender=notification)
