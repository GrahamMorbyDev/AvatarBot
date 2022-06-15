import re
from email import message
from tokenize import Token
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL

global bot
global TOKEN
 
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), method=['POST'])
def respond():
    # retrieve a message in JSON and then turn into a telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8
    text = update.message.text.encode('utf-8').decode()

    print("Got text message:", text)
    if text == '/start':
        bot_welcome = """
            Welcome to Avatar bot, the bot is using a service to create cool
            avatars 
        """

        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        try:
            # Clear the message with any non alphabets
            text = re.sub(r"\W", "_", text)
            
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())

            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:

            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))

    if s:
        return 'Webhook setup ok'
    else:
        return "Webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)