from django.db import models
from django.contrib.auth.models import User
import shortuuid
from minecraft.models import MinecraftProfile
from django.db.models.signals import post_save
from badges.models import Badge
import badges.api
from django.db.models import F
from local import update_badges

class CurrencyAccount(models.Model):
    profile = models.OneToOneField(MinecraftProfile)
    username = models.CharField(max_length=255, unique=True, null=True)
    balance = models.FloatField(default=3000)
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.profile.mc_username
        super(CurrencyAccount, self).save(*args, **kwargs)

class Quote(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

class Invite(models.Model):
    code = models.CharField(max_length=30)
    creator = models.ForeignKey(User, related_name='invites')
    claimer = models.OneToOneField(User, related_name='claimed_invite', blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = shortuuid.uuid()[:6].upper()
        super(Invite, self).save(*args, **kwargs)

    class Meta:
        ordering = ['deleted']

    @models.permalink
    def get_absolute_url(self):
        return ('local.views.claimInvite', [], {'code': self.code})

def create_account(sender, instance, created, **kwargs):
    if created:
        CurrencyAccount.objects.get_or_create(profile=instance)

post_save.connect(create_account, sender=MinecraftProfile)

def update_invite_badges(sender, instance, created, **kwargs):
    user = instance.creator
    update_badges(user)

post_save.connect(update_invite_badges, sender=Invite)

class AwardBonus(models.Model):
    badge = models.OneToOneField(Badge, related_name='minecraft_bonus')
    value = models.IntegerField()
    
    def __unicode__(self):
        return badge.__unicode__()

def award_grist(sender, award, *args, **kwargs):
    try:
        bonus = award.badge.minecraft_bonus
        account = award.user.minecraftprofile.currencyaccount
        account.balance = F('balance')+bonus.value
        account.save()
    except AwardBonus.DoesNotExist:
        pass

badges.api.badge_awarded.connect(award_grist)
