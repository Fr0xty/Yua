import itertools
import json
import random
import discord
from datetime import datetime

chars = "yuna "
prefixList = list(map(''.join, itertools.product(*zip(chars.upper(), chars.lower()))))

yuna_color = 16235890



def read_from_info():
    with open("./json/info.json", 'r') as f:
        info = json.load(f)
        return info


def read_from_info_clone():
    with open("./json/info_clone.json", 'r') as f:
        info = json.load(f)
        return info


def replenish_song_in_info_clone(server_id, song_list):
    random.shuffle(song_list)
    #set song_list in clone_info
    clone_info = read_from_info_clone()
    for server in clone_info:
        if server['server_id'] == server_id:
            server['songs'] = song_list
            break
    with open("./json/info_clone.json", 'w') as f:
        json.dump(clone_info, f, indent=2)


def get_server_songs(server_id):
    with open("./json/info.json", 'r') as f:
        info = json.load(f)
    for server in info:
        if server['server_id'] == server_id:
            return server['songs']


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour:
        return "%dh %02dm %02ds" % (hour, minutes, seconds)
    elif minutes:
        return "%02dm %02ds" % (minutes, seconds)
    else:
        return "%02ds" % (seconds)



def helpEmbed(client, author):

    _ = []

    embed = discord.Embed(
        title="Yuna's Moderation Commands!",
        color=yuna_color,
        timestamp=datetime.utcnow(),
        description=f"""
I host **24 hour** music channels! I'm only in a *few selected servers*.
My prefix is `yuna`

Github Repo: https://github.com/Fr0xty/Yuna

`setup`
To setup me in the server

`serverreset` • reset the whole server's settings (irreversible)
`addsong <url>` • add song to serverplaylist
`remsong <index>` • remove song from serverplaylist
`changevc` • change which voice channel I will be playing in
`serverplaylist` • view serverplaylist
`clearplaylist` • reset serverplaylist (irreversible)
        """
    )
    embed.set_author(name=f"{client.user.name} | Page 1 / 2", icon_url=client.user.avatar_url)
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    _.append(embed)



    embed = discord.Embed(
        title="User Commands!",
        color=yuna_color,
        timestamp=datetime.utcnow(),
        description=f"""
`vc` • get which voice channel I'm playing in
`nowplaying` `np` • view current playing song
`skip` • skip current song
`queue` `q` • view current song queue
        """
    )
    embed.set_author(name=f"{client.user.name} | Page 2 / 2", icon_url=client.user.avatar_url)
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    _.append(embed)


    return _