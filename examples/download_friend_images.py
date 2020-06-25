#!/usr/bin/env python3

import os
from getpass import getpass

import requests

from vrchat_api import VRChatAPI
from vrchat_api.enum import ModerationType

"""
Download friends' avatar thumbnails to `friend_thumbnails`.
This may takes for a while if you have a lot of friends.
"""

DIR = "friend_thumbnails"
if not os.path.exists(DIR):
    os.mkdir(DIR)

a = VRChatAPI(
    getpass("VRChat Username"),
    getpass()
)
a.authenticate()

friends = a.getFriends()
for f in friends:
    print("Downloading {:20} {}".format(f.username+"'s thumbnail:", f.currentAvatarImageUrl))
    ret = requests.get(
        f.currentAvatarImageUrl,
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    assert ret.status_code == 200

    with open(os.path.join(DIR, "{}.png".format(f.username)), "wb") as f:
        for c in ret:
            f.write(c)
