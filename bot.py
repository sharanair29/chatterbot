from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import nltk
from twilio.twiml.messaging_response import MessagingResponse
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()


app = Flask(__name__)

english_bot= ChatBot("Chatterbot",storage_adapter = "chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")


def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def get_bot_response(text):
    # userText = request.args.get("msg") # data from input
    return str(english_bot.get_response(text))


ls = []



@app.route('/get', methods=['GET', 'POST'])

def reply():
	 message = request.form.get('Body')
	 user = request.form.get('From')
	 if message:
		 ls.append(f'{user} : {message}')
		 bot = get_bot_response(str(message))
		 ls.append(f'WhatsappBot: {bot}')
	 return (respond(bot))

if __name__ == "__main__":
    app.run(debug=True)

