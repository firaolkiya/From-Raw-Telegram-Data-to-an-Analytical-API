from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import os
from dotenv import load_dotenv
import asyncio
import json

# Load environment variables
load_dotenv('.env')

api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')
client = TelegramClient('session', api_id, api_hash) # type: ignore

async def scrape_channel(channel_username, limit=50):
    await client.start() # type: ignore
    print(f"Scraping messages from {channel_username}")

    # Prepare directories
    save_dir = os.path.join("data", channel_username)
    os.makedirs(save_dir, exist_ok=True)
    json_path = os.path.join("data", f"telegram_messages/{channel_username}.json")

    messages = await client.get_messages(channel_username, limit=limit)
    all_msgs = []
    for i, message in enumerate(messages): # type: ignore
        msg_dict = message.to_dict()
        all_msgs.append(msg_dict)
        if message.media and isinstance(message.media, MessageMediaPhoto):
            file_path = await message.download_media(file=save_dir + '/')
            print(f"Saved image to: {file_path}")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(all_msgs, jf, ensure_ascii=False, indent=2, default=str)

    print(f"Saved all messages as JSON in: {json_path}")
    await client.disconnect() # type: ignore

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_channel("CheMed123"))
    loop.run_until_complete(scrape_channel("lobelia4cosmetics"))
    loop.run_until_complete(scrape_channel("tikvahpharmacy"))