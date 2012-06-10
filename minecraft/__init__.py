import badges.api

def update_badges(user):
    playtime = user.minecraftprofile.totalPlaytime();
    if playtime.days >= 1:
        badges.api.award(user, "24h_playtime")
    if playtime.days >= 7:
        badges.api.award(user, "7d_playtime")
    if playtime.days >= 30:
        badges.api.award(user, "30d_playtime")
