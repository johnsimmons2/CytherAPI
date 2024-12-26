
import os
import hashlib

usersecret = '0xIJDlKs91mS0$ls'
password = 'penis'
salt = 'd235ad04-33aa-479c-aefb-6bbcf6df7069'

result = ''
try:
    sha = hashlib.sha256()
    sha.update(password.encode(encoding="UTF-8", errors="strict"))
    sha.update(":".encode(encoding="UTF-8"))
    sha.update(salt.encode(encoding="UTF-8", errors="strict"))
    sha.update(usersecret.encode(encoding="UTF-8", errors="strict"))
    result = sha.hexdigest()
except Exception as error:
    print(error)


print(f"Result: {result}")