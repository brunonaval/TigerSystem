# -*- coding: iso-8859-1 -*-
import sqlite3
import os
import sys

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS comissoes (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                navio TEXT,
                comissoes TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                observacoes TEXT
            )
            """
        )
        self.connection.commit()

    def insert_comissao(self, navio, comissoes, data_inicio, data_fim, observacoes):
        self.cursor.execute(
            """
            INSERT INTO comissoes (navio, comissoes, data_inicio, data_fim, observacoes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (navio, comissoes, data_inicio, data_fim, observacoes),
        )
        self.connection.commit()

    def get_comissoes(self):
        self.cursor.execute("SELECT rowid, navio, comissoes, data_inicio, data_fim, observacoes FROM comissoes")
        return self.cursor.fetchall()

    def update_comissao(self, item_id, navio, comissoes, data_inicio, data_fim, observacoes):
        try:
            self.cursor.execute(
            """
            UPDATE comissoes
            SET navio = ?,
                comissoes = ?,
                data_inicio = ?,
                data_fim = ?,
                observacoes = ?
            WHERE rowid = ?
            """,
            (navio, comissoes, data_inicio, data_fim, observacoes, item_id),
        )
            self.connection.commit()
        except Exception as e:
            print(e)

    def delete_comissao(self, item_id):
        self.cursor.execute("DELETE FROM comissoes WHERE rowid=?", (item_id,))
        self.connection.commit()

    def get_navios(self):
        self.cursor.execute("SELECT DISTINCT navio FROM comissoes")
        return [{"nome": row[0]} for row in self.cursor.fetchall()]

    def get_comissao_by_values(self, navio, comissoes, data_inicio, data_fim, observacoes):
        self.cursor.execute(
            """
            SELECT rowid FROM comissoes
            WHERE navio = ? AND comissoes = ? AND data_inicio = ? AND data_fim = ? AND observacoes = ?
            """,
            (navio, comissoes, data_inicio, data_fim, observacoes),
        )
        return self.cursor.fetchone()

    #def __del__(self):
        #self.connection.close()
