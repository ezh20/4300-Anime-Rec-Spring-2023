import json
import os
from flask import Flask, render_template, request, session
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from ranking import ranking
import pandas as pd


# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# # These are the DB credentials for your OWN MySQL
# # Don't worry about the deployment credentials, those are fixed
# # You can use a different DB name if you want to
# MYSQL_USER = "root"
# MYSQL_USER_PASSWORD = "secretpassword"
# MYSQL_PORT = 3306
# MYSQL_DATABASE = "animerecs_db"

# mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# # Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
# mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template('main.html',title="AnimeRecs")

@app.route("/results", methods = ["POST"])
def to_results():
    anime = request.form['anime-input']
    genres = request.form.getlist('genre-select')
    keywords = request.form['keyword-input']
    df = pd.read_csv('../data/output.csv')
    r = ranking(df)
    return render_template("results.html", results = r.get_ranking(anime, genres, keywords), title='Results', uinp = r.self_info(anime, genres, keywords))

if __name__ == "__main__":
    app.run(debug=True)