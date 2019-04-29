from flask import Flask, url_for, request
from flask import jsonify
import json
import os

app = Flask(__name__)
ITEM_LIST = []


class AlreadyInDataBase(Exception):
    pass


# todo unexpected errorsi


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


def set_backup_file():
    try:
        global BACKUP_FILE
        BACKUP_FILE = os.environ["BACKUP_FILE"]
        # todo regex hogy mire vegzodik hanem json exception
    except KeyError:
        print(f"Backup file is not set. Default is 'backup.json'")
        BACKUP_FILE = "backup.json"


def set_storage():
    try:
        global MEMORY_STORAGE
        MEMORY_STORAGE = os.environ["STORAGE"]
    except KeyError:


def write_data():
    # todo create empty file

    with open(BACKUP_FILE, "r+") as data_writer:
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
    app.run(host='0.0.0.0')
    set_backup_file()
