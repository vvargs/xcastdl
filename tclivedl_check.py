import requests

import time
import json
import base64
import os

user_id = os.getenv("M3U8_URL").split("/")[3]

def is_live(user_id):
    print("check Live status:")
    url = f"https://twitcasting.tv/userajax.php?c=islive&u={user_id}"
    loop = True
    while loop:
        try:
            response = requests.get(url).json()
            if response == 0:
                loop = True
                print(f"{user_id} is OFFLINE")
                time.sleep(30)
            else:
                with open("info.json", "w") as outfile:json.dump(response, outfile)
                print(f"{user_id} is ONLINE")
                loop = False
        except:
            continue

is_live(user_id)
