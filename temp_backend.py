import json
import hashlib


def Login_from_json(login, password):
    if len(login) > 0:
        if login[0] == '8':
            login = '+7' + login[1:]

    json_file = open('users.json', 'r')
    json_str = ''
    for line in json_file:
        json_str += line

    json_file.close()

    data = json.loads(json_str)
    for Dict in data["users"]:
        if login == Dict["number"]:
            hash_object = hashlib.sha1(password.encode('utf-8'))
            hash_dig = hash_object.hexdigest()
            if hash_dig == Dict["password"]:
                return True

    return False
