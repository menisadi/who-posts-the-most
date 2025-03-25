from telethon.sync import TelegramClient
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
_ = load_dotenv()

api_id_raw = os.getenv("TELEGRAM_API_ID")
if api_id_raw is None:
    raise ValueError("Missing api_id variable.")
api_id = int(api_id_raw)
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("message-counter-session", api_id, api_hash)

# Replace with the public channels you want to monitor
channels = ["@amitsegal", "@lieldaphna", "@MichaelShemesh", "@grinzaig"]
days_back = 7
cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

with client:
    for channel in channels:
        count = 0
        for message in client.iter_messages(channel):
            if message.date < cutoff_date:
                break
            count += 1
        avg_per_day = count / days_back
        print(
            f"{channel}: {count} messages in last {days_back} days → {avg_per_day:.1f}/day"
        )
