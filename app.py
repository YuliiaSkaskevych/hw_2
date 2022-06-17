import csv
import requests
from statistics import mean
from faker import Faker
from flask import Flask, request

app = Flask(__name__)
fake = Faker()

@app.route("/")
def hello_world():
    return "<p>Welcome to my site!</p>"

@app.route("/requirements/")
def read_file():
    with open('requirements.txt', 'r') as f:
        file = []
        for i in f:
            file.append(f'<p>{i}</p>')
    lst = " ".join(file)
    return lst

@app.route('/generate-users/')
def users():
    num=request.args.get('count',default=100,type=int)
    c = []
    for i in range(num):
        c.append(f'<p>{i + 1} {fake.name()} {fake.email()}</p>')
    users = " ".join(c)
    return users

@app.route("/mean/")
def average():
    with open("hw.csv", "r") as f:
        reader = csv.DictReader(f)
        weight = []
        height = []
        for i in reader:
            weight.append(float(i['Weight(Pounds)']))
            height.append(float(i['Height(Inches)']))
        w_avg = mean(weight) * 0.45
        h_avg = mean(height) * 2.54
    return f'<p>Weight average: {round(w_avg, 3)} kg | Height average: {round(h_avg, 3)} cm</p>'

@app.route("/space/")
def astronauts():
    try:
        get_request = requests.get("http://api.open-notify.org/astros.json")
        if get_request.status_code == 200:
            num_astronaut = get_request.json()['number']
            return f'<p>Number of astronaut in space now: {num_astronaut}</p>'
    except requests.exceptions.ConnectionError:
        return f'<p>No internet connection!</p>'