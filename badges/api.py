import models
import django.dispatch

badge_awarded = django.dispatch.Signal(providing_args=["user", "badge"])

def award(user, badge, reason=""):
    models.Award.objects.create(badge=badge, user=user, reason=reason)
