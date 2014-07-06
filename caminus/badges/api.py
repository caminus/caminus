import models
import django.dispatch

badge_awarded = django.dispatch.Signal(providing_args=["award"])

def award(user, badgeName, reason="", unique=True):
    badge = find_badge(badgeName)
    if unique and user_has_badge(user, badgeName):
        for award in user.awards.all():
            if award.badge == badge:
                return award
    return models.Award.objects.create(badge=badge, user=user, reason=reason)

def find_badge(badgeName):
    return models.Badge.objects.get(slug=badgeName)

def create_badge(badgeName, title, description, secret=False):
    try:
        badge = find_badge(badgeName)
        badge.description = description
        badge.title = title
        badge.secret = secret
        badge.save()
    except models.Badge.DoesNotExist:
        return models.Badge.objects.create(slug=badgeName, name=title, description=description, secret=secret)
    return badge

def user_has_badge(user, badgeName, awardCount=1):
    awards = models.Award.objects.filter(badge=find_badge(badgeName), user=user)
    return len(awards) >= awardCount
