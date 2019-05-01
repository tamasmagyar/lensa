from flask import Flask, request
from flask import jsonify
import json
import argparse

app = Flask(__name__)
IN_MEMORY_STORAGE = []


class AlreadyInDataBase(Exception):
    pass


def check_storage():
    """
    Creates backup file if doesn't exist with an empty dictionary.
        Empty dictionary:
        {
        'items': []
        }
    """
    try:
        with open(BACKUP_FILE, "r") as backup_file:
            _ = backup_file.readlines()
    except FileNotFoundError:
        with open(BACKUP_FILE, "w") as backup_file:
            json.dump({"items": []}, backup_file)


def get_data():
    """
    :return:    @BACKUP_FILE's items as a list.
                e.g: ["dog", "beer"]
    """
    print(f"getting data from {BACKUP_FILE}")
    with open(BACKUP_FILE, "r") as input_data:
        backup_data = json.load(input_data)
        return backup_data["items"]


def check_if_in_db(data):
    """Checks if @data is already in @BACKUP_FILE."""
    _check_data_in_storage(get_data(), data)


def check_if_in_memory(data):
    """Checks if @data is already in memory."""
    _check_data_in_storage(IN_MEMORY_STORAGE, data)


def _check_data_in_storage(storage, data):
    """
    Checks if @data is already in @storage.
        If ValueError is raised means it isn't stored yet.
    :param data: Data to check.
    :raises AlreadyInDataBase exception if already in @storage.
    """
    try:
        storage.index(data)
        raise AlreadyInDataBase()
    except ValueError:
        pass


def save_to_memory(data_to_append):
    """
    Saves @data_to_append to memory.
    After 10 successful PUT requests.
    :param data_to_append: Data to store.
    """
    check_if_in_memory(data_to_append)
    IN_MEMORY_STORAGE.append(data_to_append)
    while len(IN_MEMORY_STORAGE) % 10 == 0:
        write_data_to_file(IN_MEMORY_STORAGE[-10:])
        print(f"Data saved to {BACKUP_FILE}.")
        break


def write_data_to_file(data_to_append):
    """
    Writes @data_to_write to BACKUP_FILE file.
    :param data_to_append: data to write
    """
    with open(BACKUP_FILE, "r+") as data_writer:
        data = get_data()
        check_if_in_db(data_to_append[0])
        data_to_write = {"items": data + data_to_append}
        json.dump(data_to_write, data_writer)


def set_args():
    """
    Sets backup file and storage type.
        Backup file:    sunshine.json
                    default is backup.json
        Storage:    If it's set to 'file' then writes put requests' data to backup file.
                    Else    Stores in memory and writes to file after 10 successful put requests.
    """
    global BACKUP_FILE, STORAGE
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup_file", help="backup file name, should end with '.json'", default="backup.json")
    parser.add_argument("--storage", help="storage type, if set to file stores all the data in a file, else in memory",
                        default="file")
    args = parser.parse_args()
    BACKUP_FILE, STORAGE = args.backup_file, args.storage


@app.route('/', methods=['GET', 'POST'])
def api():
    try:
        while request.method == "GET":
            while STORAGE == "file":
                return jsonify(get_data()), 200
            else:
                return jsonify(IN_MEMORY_STORAGE), 200
        while request.method == "POST":
            data = request.json["item"]
            while STORAGE == "file":
                write_data_to_file(data_to_append=[data])
                break
            else:
                save_to_memory(data_to_append=data)
            return f"{data} inserted to database."
    except AlreadyInDataBase:
        return f"'{data}' is already in DB."
    except Exception as e:
        return f"Unexpected error: {e}"


if __name__ == '__main__':
    set_args()
    check_storage()
    app.run(host='0.0.0.0')
