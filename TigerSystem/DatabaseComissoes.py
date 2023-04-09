# -*- coding: iso-8859-1 -*-
import sqlite3

class DatabaseComissoes:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS comissoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comissao TEXT NOT NULL
        );
        """)
        self.conn.commit()


    def save_comissoes(self, comissoes):
        self.cursor.executemany("""
        INSERT INTO comissoes (comissao)
        VALUES (?)
        """, [(comissao,) for comissao in comissoes])
        self.conn.commit()


    def delete_comissao(self, comissao_id):
        self.cursor.execute("""
        DELETE FROM comissoes WHERE id = ?
        """, (comissao_id,))
        self.conn.commit()


    def get_comissoes(self):
        self.cursor.execute("""
        SELECT * FROM comissoes
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
