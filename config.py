import itertools
import json
import random

chars = "yua "
prefixList = list(map(''.join, itertools.product(*zip(chars.upper(), chars.lower()))))

yua_color = 16235890



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