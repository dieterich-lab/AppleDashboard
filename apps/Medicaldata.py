
import modules.load_data_from_database as ldd
from db import connect_db

from AppleWatch.selection_card import selection

rdb=connect_db()
df = ldd.Card(rdb)

month =['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September','October','November','December']
day_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']




#Selection
selection = selection()





