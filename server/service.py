import os
import json
import psycopg2
import re

class DBService:

    def __init__(self):
        self.params = {
            "host": "host",
            "database": "database",
            "user": "user",
            "password": "password"
        }

    
    def get_actors_from_db(self):
        conn = psycopg2.connect(**self.params)
        sql_cmd = "SELECT row_to_json(file_name) FROM Facebook"
        cur = conn.cursor()
        actors = json
        cur.execute(sql_cmd, actors)
        conn.commit()
        # actors = {'actors':[]}
        # actors_tuple = cur.fetchall()
        # actors_list = []
        # for row in actors_tuple:
        #     actors_list.append(row[0])
        # actors['actors'] = actors_list
        # actors = json.dumps(actors, indent=2, ensure_ascii=False)
        return actors
        

if __name__ == '__main__':
    dbs = DBService()
    dbs.get_actors_from_db()
