import os 
import json
from random import choice, randint
from datetime import datetime 
import model, server, crud 

os.system('dropdb plants')
os.system('createdb plants')

model.connect_to_db(server.app)
model.db.create_all()