from flask import Flask
from tabulate import tabulate

app = Flask(__name__)

idk = {
    '1': {
        "Name": 'Bob',
        "Age": 12,
        "Is dead?": False,
        "Country": "Brasil"
    },
    '2': {
        "Name": 'Joe Goes',
        "Age": 15,
        "Is dead?": True,
        "Country": "Brasil"
    },
    '3': {
        "Name": 'Alice',
        "Age": 18,
        "Is dead?": False,
        "Country": "USA"
    },
    '4': {
        "Name": 'Emma',
        "Age": 21,
        "Is dead?": False,
        "Country": "Russia"
    },
    '5': {
        "Name": 'John',
        "Age": 32,
        "Is dead?": False,
        "Country": "Belarus"
    },
    '6': {
        "Name": 'Sarah',
        "Age": 25,
        "Is dead?": False,
        "Country": "Chile"
    },
    '7': {
        "Name": 'David',
        "Age": 40,
        "Is dead?": False,
        "Country": "Argentina"
    },
    '8': {
        "Name": 'Sophia',
        "Age": 29,
        "Is dead?": True,
        "Country": "França"
    },
    '9': {
        "Name": 'Michael',
        "Age": 35,
        "Is dead?": False,
        "Country": "Madagascar"
    },
    '10': {
        "Name": 'Olivia',
        "Age": 27,
        "Is dead?": False,
        "Country": "USA"
    },
    '11': {
        "Name": 'William',
        "Age": 19,
        "Is dead?": False,
        "Country": "Canada"
    },
    '12': {
        "Name": 'Emily',
        "Age": 23,
        "Is dead?": False,
        "Country": "USA"
    },
    '13': {
        "Name": 'Daniel',
        "Age": 30,
        "Is dead?": False,
        "Country": "Peru"
    },
    '14': {
        "Name": 'Mia',
        "Age": 16,
        "Is dead?": False,
        "Country": "Império Otomano"
    },
    '15': {
        "Name": 'Matthew',
        "Age": 28,
        "Is dead?": True,
        "Country": "Canada"
    },
    '16': {
        "Name": 'Ava',
        "Age": 22,
        "Is dead?": False,
        "Country": "USA"
    },
    '17': {
        "Name": 'James',
        "Age": 33,
        "Is dead?": False,
        "Country": "Australia"
    },
    '18': {
        "Name": 'Charlotte',
        "Age": 14,
        "Is dead?": False,
        "Country": "Brazil"
    },
    '19': {
        "Name": 'Benjamin',
        "Age": 37,
        "Is dead?": False,
        "Country": "Canada"
    },
    '20': {
        "Name": 'Scarlett',
        "Age": 26,
        "Is dead?": False,
        "Country": "USA"
    }
}

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/about')
def about():
    return 'About page'

@app.route('/information')
def information():
    global idk
    headers = ["ID", "Name", "Age", "Is dead?", "Country"]
    table_data = []

    for key, value in idk.items():
        row = [key] + [str(value[field]) for field in headers[1:]]
        table_data.append(row)

    table = tabulate(table_data, headers, tablefmt="pipe")
    return "<pre>" + table + "</pre>"

if __name__ == '__main__':
    app.run(port=3302)