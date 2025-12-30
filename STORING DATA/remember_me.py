#   from pathlib import Path
#   import json

#   username = input('What is your name? ')

#   path = Path('STORING DATA/username.json')
#   contents = json.dumps(username)
#   path.write_text(contents)

#   print(f"We'll remember you when you come back, {username}!")

#   REVISED TO COMBINE REMEMBER_ME.PY AND GREET_USER.PY
#   from pathlib import Path
#   import json

#   path = Path('STORING DATA/username.json')
#   if path.exists():
#       contents = path.read_text()
#       username = json.loads(contents)
#       print(f"Welcome back {username}!")

#   else:
#       username = input("What is your name? ")
#       contents = json.dumps(username)
#       path.write_text(contents)
#       print(f"We'll remember you when you come back, {username}!")

#REFACTORING
# from pathlib import Path
# import json

# def greet_user():
#    path = Path(f'STORING DATA/username.json')
#    if path.exists():
#        contents = path.read_text()
#        username = json.loads(contents)
#        print(f"Welcome back {username}!")

#    else:
#        username = input("What is your name? ")
#        contents = json.dumps(username)
#        path.write_text(contents)
#        print(f"We'll remember you when you come back, {username}!")

# greet_user()

#REFACTORING GREET_USER()
from pathlib import Path
import json

def get_stored_username(path):
    if path.exists():
        contents = path.read_text()
        username = json.loads(contents)
        return username
    else:
        return None

def greet_user():
    path = Path('STORING DATA/username.json')
    username = get_stored_username(path)
    if username:
        print(f"Welcome back, {username}!")
    else:
        username = input("What is your name? ")
        contents = json.dumps(username)
        path.write_text(contents)
        print(f"We'll remember you when you come back, {username}!")

greet_user()