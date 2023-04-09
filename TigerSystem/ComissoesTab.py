# -*- coding: iso-8859-1 -*-
from Database import Database
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry


class ComissoesTab:
        def __init__(self, tab_control, main_window):
            self.frame = ttk.Frame(tab_control)
            self.main_window = main_window
            self.create_widgets()
            self.create_save_button()
            self.create_edit_button()  # Adicionar esta linha
            self.carregar_comissoes()  # Adicione esta linha

            #self.db = Database('C:\\Users\\bruno\\source\\repos\\PythonApplication2\\PythonApplication2\\database.db')
            #self.carregar_comissoes()

        def carregar_comissoes(self):
            comissoes = self.main_window.db.get_comissoes()
            for comissao in comissoes:
                comissao_dict = {
                    'ID': comissao[0],
                    'Navio': comissao[1],
                    'Comissões': comissao[2],
                    'Data Início': comissao[3],
                    'Data Fim': comissao[4],
                    'Observações': comissao[5]
                }
                self.adicionar_comissao(comissao_dict, self.treeview)

   
       

        def create_widgets(self):
            # Treeview
            self.treeview = ttk.Treeview(self.frame, columns=('Navio', 'Comissões', 'Data Início', 'Data Fim', 'Observações'), show='headings')
            self.treeview.column('Navio', width=200, anchor='center')
            self.treeview.column('Comissões', width=200, anchor='center')
            self.treeview.column('Data Início', width=100, anchor='center')
            self.treeview.column('Data Fim', width=100, anchor='center')
            self.treeview.column('Observações', width=300, anchor='center')
            self.treeview.heading('Navio', text='Navio')
            self.treeview.heading('Comissões', text='Comissões')
            self.treeview.heading('Data Início', text='Data Início')
            self.treeview.heading('Data Fim', text='Data Fim')
            self.treeview.heading('Observações', text='Observações')
            self.treeview.pack(expand=1, fill='both')

    
        def save_comissao(self):
            items = self.treeview.get_children()

            for item in items:
                values = self.treeview.item(item)['values']
                navio = values[0]
                comissoes = values[1]
                data_inicio = values[2]
                data_fim = values[3]
                observacoes = values[4]

            # Verifique se a comissão já existe no banco de dados e atualize-a
            # ou insira-a se não existir
            existing_comissao = self.main_window.db.get_comissao_by_values(navio, comissoes, data_inicio, data_fim, observacoes)
            if existing_comissao:
                self.main_window.db.update_comissao(existing_comissao[0], navio, comissoes, data_inicio, data_fim, observacoes)
            else:
                self.main_window.db.insert_comissao(navio, comissoes, data_inicio, data_fim, observacoes)

            messagebox.showinfo('Sucesso', 'Comissães salvas com sucesso!')




        def editar_comissao(self):
            item_id = self.treeview.focus()
            if not item_id:
                messagebox.showerror('Erro', 'Selecione uma comissão para editar')
                return

            # Obter os valores do item selecionado
            values = self.treeview.item(item_id)['values']
            comissoes_id = self.treeview.item(item_id, option='tags')[0]

            # Exibir a janela de edição de comissão
            self.main_window.abrir_janela_edicao_comissao(item_id, values[0], values[1], values[2], values[3], values[4])






        def delete_comissao(self):
            item_id = self.treeview.focus()
            if not item_id:
                messagebox.showerror('Erro', 'Selecione uma comissão para excluir')
                return

            # Obter o ID da comissão selecionada
            comissoes_id = self.treeview.item(item_id, option='tags')[0]

            # Excluir a comissão do banco de dados
            self.main_window.db.delete_comissao(comissoes_id)

            # Remover a comissão da Treeview
            self.treeview.delete(item_id)

            messagebox.showinfo('Sucesso', 'Comissão excluída com sucesso!')


        def create_save_button(self):
            self.button_salvar = ttk.Button(self.frame, text="Salvar", command=self.save_comissao)
            self.button_salvar.pack(side="left")


        def create_edit_button(self):
            
            self.button_editar = ttk.Button(self.frame, text="Editar", command=self.editar_comissao)
            self.button_editar.pack(side="left")

            self.button_excluir = ttk.Button(self.frame, text="Excluir", command=self.delete_comissao)
            self.button_excluir.pack(side="left")


    


        def inserir_comissao_na_treeview(self, navio, comissoes, data_inicio, data_fim, observacoes):
            comissao_dict = {
                'Navio': navio,
                'Comissões': comissoes,
                'Data Início': data_inicio,
                'Data Fim': data_fim,
                'Observações': observacoes
            }
            self.adicionar_comissao(comissao_dict, self.treeview)

    
        def adicionar_comissao(self, comissao, treeview):
            def convert_date(date_str):
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")

            data_inicio = convert_date(comissao['Data Início'])
            data_fim = convert_date(comissao['Data Fim'])

            treeview.insert('', 'end', values=(
                comissao['Navio'],
                comissao['Comissões'],
                data_inicio,
                data_fim,
                comissao['Observações']
            ), tags=comissao['ID'])
