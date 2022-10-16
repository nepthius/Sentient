from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import requests
import os
app = Flask(__name__)


@app.route("/")
def homepage():
    """View function for Home Page."""
    return render_template("index.html")


@app.route("/10k-analysis", methods=['GET', 'POST'])
def analysisPage():
    """View function for About Page."""
    if request.method == 'POST':
        print(request.form.get('javascript_data'))
    return render_template("10k.html")


if __name__ == "__main__":
    app.run(debug=True)
