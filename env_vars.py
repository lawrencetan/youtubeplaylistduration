import os

db_user = os.environ.get('DB_USER')
api_key = os.environ.get('api_key')
Path = os.environ.get('Path')


print(db_user)
print(api_key)
print(Path)