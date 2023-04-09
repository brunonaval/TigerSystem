# -*- coding: iso-8859-1 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

class AdicionarNaviosTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.load_navios()
        self.frame.pack()
        self.main_window.adicionar_navios_tab = self  # Adicione esta linha

    def load_navios(self):
        navios = self.main_window.naviosdb.get_navios()
        for navio in navios:
            self.listbox_navios.insert(tk.END, navio[1])

    def get_navios(self):
        # Retorna uma lista dos navios na ListBox
        return self.listbox_navios.get(0, tk.END)


    def create_widgets(self):
        self.lbl_nome_navio = ttk.Label(self.frame, text="Nome do Navio")
        self.lbl_nome_navio.grid(row=0, column=0, padx=10, pady=10)

        self.txt_nome_navio = ttk.Entry(self.frame)
        self.txt_nome_navio.grid(row=0, column=1, padx=10, pady=10)

        self.btn_adicionar_navio = ttk.Button(self.frame, text="Adicionar Navio", command=self.adicionar_navio)
        self.btn_adicionar_navio.grid(row=1, column=0, padx=10, pady=10)

        self.listbox_navios = tk.Listbox(self.frame)
        self.listbox_navios.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.btn_excluir_navio = ttk.Button(self.frame, text="Excluir Navio", command=self.excluir_navio)
        self.btn_excluir_navio.grid(row=3, column=0, padx=10, pady=10)

    def adicionar_navio(self):
        nome_navio = self.txt_nome_navio.get()

        if not nome_navio:
            msgbox.showerror("Erro", "O nome do navio não pode estar vazio.")
            return

        confirma = msgbox.askyesno("Confirmação", "Deseja adicionar o navio '{}'?".format(nome_navio))
        if confirma:
            self.listbox_navios.insert(tk.END, nome_navio)
            self.txt_nome_navio.delete(0, tk.END)
            self.main_window.save_navios()
            self.main_window.inserir_comissoes_tab.atualizar_navios()  # Adicione esta linha# Adicione esta linha

    def excluir_navio(self):
        if not self.listbox_navios.curselection():
            msgbox.showerror("Erro", "Selecione um navio para excluir.")
            return

        index = self.listbox_navios.curselection()[0]
        navio_id = self.main_window.naviosdb.get_navios()[index][0]
        nome_navio = self.listbox_navios.get(index)

        confirma = msgbox.askyesno("Confirmação", "Deseja excluir o navio '{}'?".format(nome_navio))
        if confirma:
            self.listbox_navios.delete(index)
            self.main_window.naviosdb.delete_navio(navio_id)
            self.main_window.save_navios()  # Adicione esta linha
            self.main_window.inserir_comissoes_tab.atualizar_navios()  # Adicione esta linha

    def get_navios(self):
        # Retorna uma lista dos navios que você deseja salvar
        return self.listbox_navios.get(0, tk.END)
