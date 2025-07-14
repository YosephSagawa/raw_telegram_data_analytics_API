import asyncio
import os
import json
import logging
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    filename='../logs/scrape.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Telegram credentials
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

# Channels to scrape
channels = ['chemed123', 'lobelia4cosmetics', 'tikvahpharma']

async def scrape_channel(client, channel, date):
    data_dir = f"data/raw/telegram_messages/{date}/{channel}"
    img_dir = f"data/raw/images/{date}/{channel}"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    
    messages = []
    try:
        async for message in client.iter_messages(channel, limit=100):
            msg_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.text,
                'has_media': message.media is not None
            }
            messages.append(msg_data)
            
            # Download images
            if isinstance(message.media, MessageMediaPhoto):
                img_path = f"{img_dir}/{message.id}.jpg"
                await message.download_media(file=img_path)
                logging.info(f"Downloaded image {img_path}")
            
        # Save messages as JSON
        with open(f"{data_dir}/messages.json", 'w') as f:
            json.dump(messages, f, indent=2)
        logging.info(f"Scraped {len(messages)} messages from {channel}")
        
    except Exception as e:
        logging.error(f"Error scraping {channel}: {str(e)}")

async def main():
    async with TelegramClient('session', api_id, api_hash) as client:
        await client.start(phone=phone)
        date = datetime.now().strftime('%Y-%m-%d')
        for channel in channels:
            await scrape_channel(client, channel, date)

if __name__ == "__main__":
    asyncio.run(main())