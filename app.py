from flask import Flask, render_template
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

url = "https://covid-19-asi-api-turkiye.herokuapp.com/"
response = requests.get(url)
content = response.json()
qsecond = list()
qbsecond = list()
for i in content["cities"]:
    qsecond.append(i["secondDose"])
    qbsecond.append("{:,}".format(i["secondDose"]))

with open("data/nufus.json") as file:
    data = json.load(file)

il = list()
nufus = list()
for i in data["data"]:
        il.append(i["il_adi"])
        nufus.append(i["nufus"])


@app.route("/")
def index():
    secondDose = content["totalSecondDose"]["totalSecondDose"]
    percentage = (secondDose * 100) / 85096445
    percentage = str(round(percentage, 2))
    plaka = list(range(1, 82))
    dictData = dict(zip(il, qbsecond))
    ilPercentage = [round((j * 100) / int(k.replace(".", "")), 2) for j, k in zip(qsecond, nufus)]
        

    return render_template("index.html", percentage = percentage, dictData = dictData, ilPercentage = ilPercentage, plaka = plaka)

if __name__ == "__main__":
    app.run(debug=True)