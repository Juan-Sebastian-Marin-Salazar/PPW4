from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("user/index.html")

@app.route("/menu")
def menu():
    return render_template("user/menu.html")

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

