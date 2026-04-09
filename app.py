from flask import Flask
from flask import render_template as rn
from flask import request
import csv
import requests
import matplotlib.pyplot as plt
app = Flask(__name__)






@app.route("/team")
def team():
    return rn("team.html")
@app.route('/')
def index():
    return rn('index.html')
@app.route('/github', methods=['POST'])
def github():

    username = request.form['github']

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)

    if response.status_code == 200:

        repos = response.json()

        repo_names = []

        for repo in repos[:10]: 
            repo_names.append(repo['name'])

        return rn(
            "github.html",
            username=username,
            repos=repo_names
        )

    else:
        return "GitHub user not found"




@app.route('/submit', methods=['POST'])
def submit():

    roll = request.form['roll']
    name = request.form['name']
    college = request.form['college']
    skill = request.form['skill']
    github = request.form['github']

   
    url = f"https://api.github.com/users/{github}"

    response = requests.get(url)

    if response.status_code != 200:
        return "Invalid GitHub Username ! Please enter a correct username."
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([roll, name, college, skill, github])

    from flask import redirect, url_for

    return redirect(url_for('pie'))


import csv
import matplotlib.pyplot as plt

@app.route('/pie')
def pie():

    skills = []

    with open('data.csv', 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 4:
                continue

            skills.append(row[3])

    if not skills:
        return "No data available"

    labels = list(set(skills))
    values = []

    for skill in labels:
        values.append(skills.count(skill))

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Skill Distribution")

    # Save with same name
    plt.savefig('static/pie_chart.png')
    plt.close()

    return rn('pie.html')
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


