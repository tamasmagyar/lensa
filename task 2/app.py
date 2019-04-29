from flask import Flask, url_for, request
from flask import jsonify
import json

app = Flask(__name__)

ITEM_LIST = []


class AlreadyInDataBase(Exception):
    pass


# todo unexpected errors

def get_data():
    with open("results.json", "r") as input_data:
        return json.load(input_data)


def check_if_in_db(data):
    try:
        get_data()["items"].index(data)
        raise AlreadyInDataBase()
    except ValueError:
        pass


def check_if_in_list(data):
    try:
        ITEM_LIST.index(data)
        raise AlreadyInDataBase()
    except ValueError:
        pass


def write_data():
    with open("results.json", "r+") as data_writer:
        data = get_data()["items"]  # todo if not exist
        print(f" data: {data}")
        data_to_write = {}
        data_to_write["items"] = data + ITEM_LIST
        print(f" data: {data_to_write}")
        json.dump(data_to_write, data_writer)


@app.route('/', methods=['GET', 'POST'])
def api():
    try:
        data = request.json
        print(f"{data}")
        data = data["item"]
        check_if_in_db(data)
        check_if_in_list(data)
        ITEM_LIST.append(data)
        while len(ITEM_LIST) > 9:
            write_data()

            del ITEM_LIST[:]
        return f"{data} inserted to database."
    except AlreadyInDataBase:
        return f"{data} is already in DB."
    except Exception:  # todo get
        return jsonify(get_data()["items"]), 200


if __name__ == '__main__':
    app.run()
