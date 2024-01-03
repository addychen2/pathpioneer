from flask import Flask
app = Flask(__name__)

@app.route('/calculateRoute')
def calculateRoute():
   return {
        "test": "response received!"
    }

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)