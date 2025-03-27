import os
import time
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import (
    UsernameInvalidError,
    ChannelPrivateError,
    FloodWaitError,
)
from rich.console import Console
from rich.table import Table
from rich import box

_ = load_dotenv()

api_id_raw = os.getenv("TELEGRAM_API_ID")
if api_id_raw is None:
    raise ValueError("Missing api_id variable.")
api_id = int(api_id_raw)
api_hash = os.getenv("TELEGRAM_API_HASH")

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Track Telegram channel message activity."
    )
    parser.add_argument(
        "--channel_file",
        default="channels.txt",
        help="Path to the file containing channel list (default: channels.txt)",
    )
    parser.add_argument(
        "--days", type=int, default=0, help="How many days back to look"
    )
    parser.add_argument(
        "--weeks", type=int, default=1, help="How many weeks back to look"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=0,
        help="How many months (30 days each) back to look",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Modify the behaviour to wait if rate limit reached, instead of exiting",
    )
    return parser.parse_args()


def load_channels_from_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def main():
    args = parse_args()
    channels = load_channels_from_file(args.channel_file)

    # Compute total time range
    total_days = args.days + args.weeks * 7 + args.months * 30
    if total_days <= 0:
        console.print(
            "[bold red]Error:[/bold red] You must specify a time period with --days, --weeks, or --months."
        )
        return

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=total_days)

    # Build a friendly string for display
    period_parts = []
    if args.months:
        period_parts.append(f"{args.months} month(s)")
    if args.weeks:
        period_parts.append(f"{args.weeks} week(s)")
    if args.days:
        period_parts.append(f"{args.days} day(s)")
    display_period = ", ".join(period_parts)

    # Header
    console.rule("[bold cyan]📊 Telegram Channel Message Race")
    console.print(
        f"Analyzing message activity over the past [bold magenta]{display_period}[/bold magenta]...\n"
    )

    # Table
    table = Table(title="Average Messages Per Day", box=box.SIMPLE_HEAVY)
    table.add_column("Channel", style="bold green")
    table.add_column("Messages", justify="right", style="yellow")
    table.add_column("Avg/Day", justify="right", style="cyan")

    # Fetch messages
    with TelegramClient("message-counter-session", api_id, api_hash) as client:
        for channel in channels:
            try:
                count = 0
                for message in client.iter_messages(channel):
                    if message.date < cutoff_date:
                        break
                    count += 1
                avg_per_day = count / total_days
                table.add_row(channel, str(count), f"{avg_per_day:.1f}")

            except UsernameInvalidError:
                console.print(
                    f"[bold red]✖ Skipping {channel}:[/bold red] username not found or invalid."
                )
            except ChannelPrivateError:
                console.print(
                    f"[bold yellow]🔒 Skipping {channel}:[/bold yellow] channel is private or requires a join."
                )
            except FloodWaitError as e:
                if args.wait:
                    # TODO: Skipping after sleeping is the simple solution
                    # but the correct solution would be to wrap the 'for' with a sleep loop
                    console.print(
                        f"[bold red]⏳ Rate limit hit![/bold red] Need to wait {e.seconds} seconds. Sleeping..."
                    )
                    time.sleep(e.seconds + 1)
                    console.print(
                        f"[bold yellow]Continuing with next channel after waiting.[/bold yellow]\n"
                    )
                else:
                    console.print(
                        f"[bold red]⏳ Rate limit hit![/bold red] Need to wait {e.seconds} seconds. Exiting..."
                    )
                    # INFO: I assume that the rate limit is a global limit
                    # So there is no point of going on.
                    return
            except Exception as e:
                console.print(
                    f"[bold red]⚠ Error with {channel}:[/bold red] {str(e)}"
                )

    console.print(table)


if __name__ == "__main__":
    main()
