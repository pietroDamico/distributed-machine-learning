from flask import Flask, jsonify
import random, requests

app = Flask(__name__)
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()

@app.route('/random-word', methods=['GET'])
def get_random_word():
    
    random_word = WORDS[random.randint(0,len(WORDS) - 1)].decode('utf-8')

    return random_word

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)