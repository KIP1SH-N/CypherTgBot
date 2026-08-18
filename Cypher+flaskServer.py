import telebot
from zxcvbn import zxcvbn
import requests
import hashlib
from flask import Flask, request

bot = telebot.TeleBot('BOT_TOKEN')
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def main (message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! I can help you to check reliability of your password\n\nYou can control me by sending these commands:\n\n<b>/help</b> - output this message\n<b>/test</b> - check how strong your password against bruteforce', parse_mode='html')
    
@bot.message_handler(commands=['test'])
def askForPass (message):
    ask_pass = bot.send_message(message.chat.id, 'Type the password which you wanna check:')
    bot.register_next_step_handler(ask_pass, test)

def test(message):
    userInput = message.text
    results = zxcvbn(userInput)
    
    hashPass=hashlib.sha1(userInput.encode()).hexdigest().upper()
    prefix=hashPass[:5]
    suffix = hashPass[5:]
    
    url=f"https://api.pwnedpasswords.com/range/{prefix}"
    response=requests.get(url)
    
    if response.status_code == 200:
        hashes=response.text.splitlines()
        for h in hashes:
            getSuffix, count = h.split(":")
            if getSuffix==suffix:
                bot.reply_to(message, f"<b>BruteForce Test:</b>\n\nSafety of password: {results['score']}/5\nTime for crack: {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n<b>Leak Check:</b>\n\nThis password has been seen {count} times before in data breaches!" , parse_mode='html')
                break
        else:
            bot.reply_to(message, f"<b>BruteForce Test:</b>\n\nSafety of password: {results['score']}/5\nTime for crack: {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n <b>Leak Check:</b>\n\n Password isn't in data breaches", parse_mode='html')
    else:
        bot.reply_to(message, f"<b>BruteForce Test:</b>\n\nSafety of password: {results['score']}/5\nTime for crack: {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n <b>Leak Check:</b>\n\n Server Unreacheble :(", parse_mode='html')

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return '', 200  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
