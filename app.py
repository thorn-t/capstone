from flask import Flask, render_template, render_template_string
import pandas as pd
from markupsafe import Markup
import sortcsv
app = Flask(__name__)
# All html files must be in the templates folder

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/players/all")
def getAllPlayers():
    # df is the flattened df from sortcsv
    df = sortcsv.getList()
    # dfHtml is df in a safe html form so jinja will render it
    dfHtml = Markup(df.to_html())
    return render_template("allplayers.html", dfHtml=dfHtml)

if __name__ == "__main__":
    app.run(debug=True)