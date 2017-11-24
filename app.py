from flask import Flask
from flask import Flask, render_template, request, json
import jwt

app = Flask(__name__)


@app.route("/hello")
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
