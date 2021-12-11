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