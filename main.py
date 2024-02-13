import http.client
import json
import datetime
import time
import os
from keep_alive import keep_alive
keep_alive()

user_id = os.environ.get('userid')

# Function to get user data from ROBLOX API
def get_user_data(user_id):
    connection = http.client.HTTPSConnection("users.roblox.com")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    connection.request("GET", f"/v1/users/{user_id}", headers=headers)
    response = connection.getresponse()

    if response.status == 200:
        user_data = json.loads(response.read())
        connection.close()
        return user_data
    else:
        print("Failed to retrieve user data. Status code:", response.status)
        connection.close()
        return None

# Function to get thumbnail URL from ROBLOX API
def get_thumbnail_url(user_id):
    connection = http.client.HTTPSConnection("thumbnails.roproxy.com")
    connection.request("GET", f"/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png")
    response = connection.getresponse()

    if response.status == 200:
        data = json.loads(response.read())
        thumbnail_url = data["data"][0]["imageUrl"] if data["data"] else None
        connection.close()
        return thumbnail_url
    else:
        print("Failed to retrieve thumbnail URL. Status code:", response.status)
        connection.close()
        return None

# Main loop
while True:
    print("체크 중...")
    user_data = get_user_data(user_id)

    if user_data:
        is_banned = user_data.get("isBanned", False)
        if is_banned:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nickname = user_data.get("name", "Unknown User")
            thumbnail_url = get_thumbnail_url(user_id)

            webhook_url = os.environ.get('webhook')  # Replace this with your actual webhook URL

            payload = {
                "content": "@everyone",
                "embeds": [
                    {
                        "title": f"{nickname}의 계정이 삭제 당했습니다!",
                        "description": f"```\n삭제된 시간 : {current_time}\n```\n```\n계정 상태 : 계정 삭제됨 ❌\n```",
                        "url": f"https://www.roblox.com/users/{user_id}/profile",
                        "color": 7864189,
                        "thumbnail": {
                            "url": thumbnail_url
                        }
                    }
                ],
                "attachments": []
            }

            headers = {'Content-Type': 'application/json'}

            connection = http.client.HTTPSConnection("discord.com")
            connection.request("POST", webhook_url, body=json.dumps(payload), headers=headers)
            response = connection.getresponse()
            print("Webhook response:", response.status, response.reason)
            connection.close()
            break
        else:
            print("User is not banned.")
    else:
        print("Failed to retrieve user data.")

    time.sleep(0.1)  # Wait 5 seconds before checking again



# 밴 당하기 스피드런 할때 유용한 툴 ㅇㅇ
