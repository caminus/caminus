import models
import django.dispatch

badge_awarded = django.dispatch.Signal(providing_args=["award"])

def award(user, badgeName, reason=""):
    badge = find_badge(badgeName)
    return models.Award.objects.create(badge=badge, user=user, reason=reason)

def find_badge(badgeName):
    return models.Badge.objects.get(slug=badgeName)

def create_badge(title, description, badgeName=None, secret=False):
    if badgeName is None:
        return models.Badge.objects.create(name=title, description=description, secret=secret)
    else:
        try:
            badge = find_badge(badgeName)
        except models.Badge.DoesNotExist:
            return models.Badge.objects.create(slug=badgeName, name=title, description=description, secret=secret)
        return badge

def user_has_badge(user, badgeName, awardCount=1):
    awards = models.Award.objects.filter(badge=find_badge(badgeName), user=user)
    return len(awards) >= awardCount
