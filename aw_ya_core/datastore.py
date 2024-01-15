import sqlite3
import pandas as pd
import os

class DataStore:
    _instance = None

    def __init__(self):
        if os.getenv('YA_DBFILE_PATH'):
            self.db_name = os.getenv('YA_DBFILE_PATH')
        else:
            self.db_name = "DefDB.db"
        print(self.db_name)
        self.views_table = "AnalysisViewDef"
        self.categories_table = "CategoryDef"
        self.events_table = "SelectedEvents"
        self.words_table = "SelectedWords"
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                (f"CREATE TABLE IF NOT EXISTS {self.views_table}"
                 f"(id INTEGER PRIMARY KEY,name TEXT,color TEXT,use_def_color INTEGER)")
            )
            cur.execute(
                (f"CREATE TABLE IF NOT EXISTS {self.categories_table}"
                 f"(id INTEGER PRIMARY KEY,view_id INTEGER, name TEXT,color TEXT)")
            )
            cur.execute(
                (f"CREATE TABLE IF NOT EXISTS {self.events_table}"
                 f"(id INTEGER PRIMARY KEY,category_id INTEGER, app TEXT,title TEXT)")
            )
            cur.execute(
                (f"CREATE TABLE IF NOT EXISTS {self.words_table}"
                 f"(id INTEGER PRIMARY KEY,category_id INTEGER, word TEXT,positive INTEGER)")
            )
            conn.commit()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def clear(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE from {self.words_table}")
            cur.execute(f"DELETE from {self.events_table}")
            cur.execute(f"DELETE from {self.categories_table}")
            cur.execute(f"DELETE from {self.views_table}")
            conn.commit()

    def query(self, query_str):
        with sqlite3.connect(self.db_name) as conn:
            df = pd.read_sql_query(query_str, conn)
        def_list = df.to_numpy().tolist()
        return def_list

    def execute(self, query_str):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(query_str+" RETURNING id")
            row = cur.fetchone()
            conn.commit()
        rid = row[0] if row[0] else None
        return rid

    def inputTestData(self):
        # テスト用初期データ
        datas = [{"view": ["作業オーダ", "Blue", 0],
                  "categories": [{"category": ["EN0001", '#0000FF'],
                                  "words": [["PMBOK", True], ["エンジニアリング", True],
                                            ["マネージメント", True], ["タイムトラッキング", False]]},
                                 {"category": ["DX0002", "#6A80FF"],
                                  "words": [["Jupyter", True], ["システム", True], ["マネージメント", False]]}]
                  },
                 {"view": ["作業分類", "Green", 0],
                  "categories": [{"category": ["文書作成", '#0000FF'],
                                  "words": [["メモ", True], ["Word", True],
                                            ["新規作成", True]]},
                                 {"category": ["管理作業", "#6A80FF"],
                                  "words": [["freee", True], ["コンソール", True]]}]
                  }]

        # 初期データをデータベースに格納する
        with sqlite3.connect(DataStore().db_name) as conn:
            cur = conn.cursor()
            for data in datas:
                vinfo = data["view"]
                query_str = f"INSERT into {DataStore().views_table} (name, color, use_def_color) values ('{vinfo[0]}','{vinfo[1]}',{vinfo[2]})"
#                print(query_str)
                cur.execute(query_str+" RETURNING id")
                vid = cur.fetchone()
                for cdata in data["categories"]:
                    cinfo = cdata["category"]
                    query_str = f"INSERT into {DataStore().categories_table} (view_id, name, color) values ({vid[0]}, '{cinfo[0]}','{cinfo[1]}')"
#                    print(query_str)
                    cur.execute(query_str+" RETURNING id")
                    cid = cur.fetchone()
                    for winfo in cdata["words"]:
                        # print(winfo)
                        x = 1 if winfo[1] else 0
                        query_str = f"INSERT into {DataStore().words_table} (category_id, word,positive) values ({cid[0]},'{winfo[0]}',{x})"
#                        print(query_str)
                        cur.execute(query_str)
            conn.commit()
