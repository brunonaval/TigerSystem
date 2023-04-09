# -*- coding: iso-8859-1 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

class AdicionarComissoesTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.load_comissoes()
        
    
    def load_comissoes(self):
        comissoes = self.main_window.comissoesdb.get_comissoes()
        for comissao in comissoes:
            self.listbox_comissoes.insert(tk.END, comissao[1])
    



    def create_widgets(self):
        self.lbl_nome_comissao = ttk.Label(self.frame, text="Nome da Comissão")
        self.lbl_nome_comissao.grid(row=0, column=0, padx=10, pady=10)

        self.txt_nome_comissao = ttk.Entry(self.frame)
        self.txt_nome_comissao.grid(row=0, column=1, padx=10, pady=10)

        self.btn_adicionar_comissao = ttk.Button(self.frame, text="Adicionar Comissão", command=self.adicionar_comissao)
        self.btn_adicionar_comissao.grid(row=1, column=0, padx=10, pady=10)

        self.listbox_comissoes = tk.Listbox(self.frame)
        self.listbox_comissoes.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.btn_excluir_comissao = ttk.Button(self.frame, text="Excluir Comissão", command=self.excluir_comissao)
        self.btn_excluir_comissao.grid(row=3, column=0, padx=10, pady=10)

        
    def adicionar_comissao(self):
        nome_comissao = self.txt_nome_comissao.get()

        if not nome_comissao:
            msgbox.showerror("Erro", "O nome da comissão não pode estar vazio.")
            return

        confirma = msgbox.askyesno("Confirmação", "Deseja adicionar a comissão '{}'?".format(nome_comissao))
        if confirma:
            self.listbox_comissoes.insert(tk.END, nome_comissao)
            self.txt_nome_comissao.delete(0, tk.END)
            self.main_window.comissoes_adicionadas.append(nome_comissao) 
            self.main_window.comissoesdb.save_comissoes(self.main_window.comissoes_adicionadas)  # Adicione esta linha
            self.main_window.comissoes_adicionadas = []  # Adicione esta linha

    #def get_comissoes(self):
        # Retorna uma lista das comissões que você deseja salvar
        #return self.listbox_comissoes.get(0, tk.END)


    def excluir_comissao(self):
        if not self.listbox_comissoes.curselection():
            msgbox.showerror("Erro", "Selecione uma comissão para excluir.")
            return

        index = self.listbox_comissoes.curselection()[0]
        comissao_id = self.main_window.comissoesdb.get_comissoes()[index][0]
        nome_comissao = self.listbox_comissoes.get(index)

        confirma = msgbox.askyesno("Confirmação", "Deseja excluir a comissão '{}'?".format(nome_comissao))
        if confirma:
            self.listbox_comissoes.delete(index)
            self.main_window.comissoesdb.delete_comissao(comissao_id)

