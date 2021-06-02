import vk_api
import time
import json
import os

settings_file = "settings.json"


def initialize_settings() -> dict:
    if not os.path.isfile(settings_file):
        f = open(settings_file, "w", encoding="utf-8")

        f.write(json.dumps({
            "login": "your login",
            "password": "your password",

            "music_stream": True,
            "music_delay": 3,

            "messages_stream": False,
            "messages_delay": 5,
            "messages_stream_id": "0",
            "last_message_stream": True,
            "last_message_file": "data/last_message.txt",

            "music_file": "data/music.txt",
            "messages_file": "data/messages.txt"
        }, indent=4))
        f.close()

    f = open(settings_file, "r", encoding="utf-8")
    settings = json.loads(f.read())
    f.close()

    return settings


def stream_music(vk, delay, file):
    status = vk.status.get()
    audio = status['audio'] if ('audio' in status) else False

    f = open(file, 'w', encoding='utf-8')
    if audio:
        f.write(status['text'])
    else:
        f.write('')

    f.close()
    time.sleep(delay)


def stream_messages(vk, delay, file, id, last_message_file):
    messages = vk.wall.getComments(post_id=id)
    f = open(file, 'w', encoding='utf-8')

    items = messages["items"]

    for item in items:
        f.write(item["text"] + "\n")

    if last_message_file:
        f = open(last_message_file, 'w', encoding='utf-8')
        f.write(items[-1]["text"])
        f.close()

    f.close()
    time.sleep(delay)


if __name__ == "__main__":
    settings = initialize_settings()
    os.makedirs("data", exist_ok=True)

    music_stream = settings["music_stream"]
    music_delay = settings["music_delay"]  # Should it be only if enabled? May be
    messages_stream = settings["messages_stream"]
    messages_stream_id = settings["messages_stream_id"]  # Should it be only if enabled? May be
    messages_delay = settings["messages_delay"]  # Should it be only if enabled? May be
    last_message_stream = settings["last_message_stream"]

    music_file = settings["music_file"]
    messages_file = settings["messages_file"]
    last_message_file = settings["last_message_file"]

    if music_stream:
        f_music = open(music_file, "w", encoding="utf-8")
        f_music.close()
    if messages_stream:
        f_messages = open(messages_file, "w", encoding="utf-8")
        f_messages.close()
    if last_message_stream:
        f_last_message = open(last_message_file, "w", encoding="utf-8")
        f_last_message.close()

    vk_session = vk_api.VkApi(settings["login"], settings["password"])

    try:
        vk_session.auth()
    except Exception as e:
        print("Incorrect credentials entered")
        raise

    vk = vk_session.get_api()
    print("Successfully logged")

    while True:
        if music_stream:
            stream_music(vk, music_delay, music_file)
        if messages_stream:
            stream_messages(vk, messages_delay, messages_file, messages_stream_id, last_message_file if last_message_stream else False)
