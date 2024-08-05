from flask import Flask, jsonify, request, render_template
from qabot import QABot
from openai.error import RateLimitError
import json


app = Flask(__name__)

@app.route('/')
def home():
    with open('document_config.json', 'r') as FILE:
        config = json.load(FILE)
    return render_template('index.html', title=config['title'])

@app.route('/query')
def ask():
    question = request.args.get('question')
    try:
        answer = qabot.query(question)
    except RateLimitError:
        return jsonify({"error": "Rate limit error, try again later"}), 500
    except Exception as ex:
        return jsonify({"error": ex}), 500
    return jsonify({"answer": answer})


if __name__ == '__main__':
    qabot = QABot()
    qabot.loadDB()
    app.run(debug=True, host='0.0.0.0')
