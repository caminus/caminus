import models
import django.dispatch

badge_awarded = django.dispatch.Signal(providing_args=["user",])

def award(user, badge):
  user.badges += badge
  user.save()
  badge_awarded.send_robust(sender=badge, user=user)
