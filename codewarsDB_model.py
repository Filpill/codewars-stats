import sqlite3

class Product:
    def __init__(self):
        self.con = sqlite3.connect('codewarsDB.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        # self.cur.execute("""DROP TABLE dim_kata_details""")
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS dim_kata_details(
                id TEXT PRIMARY KEY,
                category TEXT,
                tags ARRAY
                rank.name
            )
        """)
