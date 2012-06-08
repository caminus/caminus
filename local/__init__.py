import badges.api

def update_badges(user):
    inviteCount = len(user.invites.filter(claimer__isnull=False))
    if inviteCount >= 3:
        badges.api.award(user, "three_invites")
    if inviteCount >= 5:
        badges.api.award(user, "five_invites")
    if inviteCount >= 10:
        badges.api.award(user, "ten_invites")
