
from app.dailygames import load_schedule
from app.dailygames import show_schedule
from pprint import pprint

data = load_schedule()

show_schedule(data)