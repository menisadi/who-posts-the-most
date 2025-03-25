# 📊 Chatter Chase

Track and compare how active different Telegram channels are — and see who posts the most 📈

## 🚀 What It Does

Given a list of Telegram channels, `chatter-chase` checks how many messages each one published over a given time period and calculates the average messages per day. It outputs a clean, color-coded leaderboard in your terminal.

---

## 🧰 Features

- ✅ Reads a list of channels from a file
- ✅ Supports custom time ranges: days, weeks, or months
- ✅ Beautiful terminal output using [`rich`](https://github.com/Textualize/rich)

---

## 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/chatter-chase.git
cd chatter-chase
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Telegram API credentials:

```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

You can get these from [my.telegram.org](https://my.telegram.org).

---

## 📂 Usage

Prepare a file called `channels.txt` with one channel username per line:

```
@channel1
@channel2
@some_other_channel
```

Then run:

```bash
python main.py --weeks 2
```

You can also customize the channel list path and time range:

```bash
python main.py --channel_file mychannels.txt --months 1 --days 3
```

---

## 🛡️ Notes

- Only works with **public** Telegram channels
- Channels that are private or don't exist are skipped with a warning
- Uses Telethon, so you'll need to log in once when you first run it

---

## ✨ Example Output

```markdown
─────────────────────────────────────
Analyzing message activity over the past 1 week(s)...

                 Average Messages Per Day

  Channel                             Messages   Avg/Day
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  @hacker_news_feed                        180      25.7
  @techguide                               529      75.6
  @computer_science_and_programming          7       1.0
  @SammyFans                               134      19.1
  @durov                                     1       0.1
```

---

## 🤔 Future Ideas

- Streamlit or web dashboard version
- Trending charts over time
- Weekly top performer highlights 🥇
- Alerts when a channel spikes in activity

---

## 📜 License

