# CypherTgBot 
Telegram bot for checking password security: evaluating resistance to brute-force attacks and checking for data breaches.

## Features
- Password strength assessment (using the zxcvbn algorithm) - score from 0 to 5 and estimated cracking time
- Password breach checking using [Have I Been Pwned](https://haveibeenpwned.com/) API (k-anonymity, the full password is never sent)

## Technologies
- Python, Flask, pyTelegramBotAPI
- Webhook architectures, deployed Render

## Bot commands
- `/start`, `/help` - welcome message and list of available commands
- `/test` - check a password

## Local Installation and Setup
\`\`\`bash
git clone https://github.com/KIP1SH-N/CypherTgBot.git
cd CypherTgBot
pip install -r requirements.txt
export BOT_TOKEN=(your token)
python main.py
\`\`\`

## Deploy
The bot is deployed on Render.com using a webhook architecture (scale-to-zero, free tier).
