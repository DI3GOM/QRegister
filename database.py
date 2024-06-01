import sqlite3
        
conn = sqlite3.connect('events.db')

cursor = conn.cursor()



cursor.execute("""CREATE TABLE events_table (
            event_name text NOT NULL,
            code text PRIMARY KEY NOT NULL,
            name text NOT NULL,
            entered_party integer NOT NULL 
        )""")

conn.commit()

conn.close()