import json

FEELINGS = ["hates", "likes", "loves"]
CONJUNCTIONS = ["and", "but"]


def is_breaker(word):
    """
    Checks if @word is a breaker, so ends with ',' or a '\n'
        - ',' means a new feelings starts in the sentence.
        - '\n' means it's the last word.
    :param word: Word to check.
    """
    last_char = word[-1]
    return True if last_char == "," or last_char == "\n" else False


def should_append_to_results(word):
    """
    Checks if @word is a name.
        Word is a name if it's not in FEELINGS or CONJUNCTIONS.
    :param word: word to check
    :return: True if it a name, else False.
    """
    return word not in FEELINGS + CONJUNCTIONS


def get_connections(words):
    """
    Iterates through the list of words.
            - If the word is a feeling ("hates", "likes", "loves") creates a new list.
                    * Adds all the non conjunction words (names) until one name ends with a ',' or a "\n".

    :param words: Current line's words to check.
    :return:    Dictionary
                        - keys are feelings ("hates", "likes", "loves")
                        - values are list of names ["Bob", "Ryan"]

                Example:
                        {
                        "loves": [
                                    "Jane",
                                    "Bob"
                                    ],
                        "hates": [
                                    "Jack",
                                    "Brad"
                                ]
                        }
    """
    connections = {}
    feeling = None
    feeling_names = []
    for word in words:
        if not feeling and word in FEELINGS:
            feeling = word
            feeling_names = []
            continue
        if should_append_to_results(word):
            if is_breaker(word):
                feeling_names.append(word.rstrip()[:-1])
                connections[feeling] = feeling_names
                feeling = None
            else:
                feeling_names.append(word)
    return connections


def get_result(data):
    """
    Iterates through @data and collects result.
    :param data: Input data to check.
    :return: Results about who likes who.
    """
    result = {}
    for line in data:
        words = line.split(" ")
        who = words[0]
        result[who] = get_connections(words[1:])
    return result


def read_inputs():
    with open("inputs.txt", "r") as input_data:
        return input_data.readlines()


def write_results(results):
    with open('results.json', 'w') as result_data:
        json.dump(results, result_data, indent=4)


def main():
    input_data = read_inputs()
    who_likes_who_result = get_result(input_data)
    write_results(who_likes_who_result)


if __name__ == '__main__':
    main()
