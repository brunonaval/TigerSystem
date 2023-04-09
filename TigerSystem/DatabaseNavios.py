# -*- coding: iso-8859-1 -*-
import sqlite3

class DatabaseNavios:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS navios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            navio TEXT NOT NULL
        );
        """)
        self.conn.commit()

    def navio_exists(self, navio):
        self.cursor.execute("SELECT * FROM navios WHERE navio=?", (navio,))
        resultado = self.cursor.fetchone()
        return resultado is not None


    def save_navios(self, navios):
        for navio in navios:
            if not self.navio_exists(navio):
                self.cursor.execute("""
                INSERT INTO navios (navio)
                VALUES (?)
                """, (navio,))
                self.conn.commit()
            else:
                print(f"Navio '{navio}' já existe no banco de dados.")


    def delete_navio(self, navio_id):
        self.cursor.execute("""
        DELETE FROM navios WHERE id = ?
        """, (navio_id,))
        self.conn.commit()

    def get_navios(self):
        self.cursor.execute("""
        SELECT * FROM navios
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()




