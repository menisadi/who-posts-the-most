from telethon.sync import TelegramClient
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import box
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

console = Console()

# Print a colorful title
console.rule("[bold cyan]📊 Telegram Channel Message Race")
console.print(
    f"Analyzing message activity over the past [bold magenta]{days_back}[/bold magenta] days...\n"
)

# Create a nice table
table = Table(title="Average Messages Per Day", box=box.SIMPLE_HEAVY)
table.add_column("Channel", style="bold green")
table.add_column("Messages", justify="right", style="yellow")
table.add_column("Avg/Day", justify="right", style="cyan")

with client:
    for channel in channels:
        count = 0
        for message in client.iter_messages(channel):
            if message.date < cutoff_date:
                break
            count += 1
        avg_per_day = count / days_back
        table.add_row(channel, str(count), f"{avg_per_day:.1f}")

console.print(table)
