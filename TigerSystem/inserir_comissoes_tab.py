# -*- coding: iso-8859-1 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

class InserirComissoesTab:
    def __init__(self, tab_control, main_window, comissoes_tab):
        self.frame = ttk.Frame(tab_control)
        self.main_window = main_window
        self.comissoes_tab = comissoes_tab
        self.create_widgets()
        self.main_window.inserir_comissoes_tab = self
        self.load_comissoes()
        self.atualizar_navios()


    def load_comissoes(self):
        comissoes = self.main_window.comissoesdb.get_comissoes()
        for comissao in comissoes:
            self.listbox_comissoes.insert(tk.END, comissao[1])

    def atualizar_navios(self):
        self.combobox_navio['values'] = self.main_window.adicionar_navios_tab.get_navios()



    def create_widgets(self):


        # Label navio
        self.label_navio = ttk.Label(self.frame, text="Navio:")
        self.label_navio.grid(column=0, row=0, padx=10, pady=10)

        # Combobox navio
        self.combobox_navio = ttk.Combobox(self.frame, state='readonly')
        self.combobox_navio.grid(column=1, row=0, padx=10, pady=10)
        #self.combobox_navio['values'] = ['FRAGATA DEFENSORA - F41', 'FRAGATA CONSTITUI��O - F42', 'FRAGATA LIBERAL - F43', 'FRAGATA INDEPEND�NCIA - F44', 'FRAGATA UNI�O - F45']

        # Label data de in�cio
        self.label_data_inicio = ttk.Label(self.frame, text="Data de in�cio da Comiss�o (DD/MM/AAAA):")
        self.label_data_inicio.grid(column=0, row=1, padx=10, pady=10)

        # Entry data de in�cio
        self.entry_data_inicio = DateEntry(self.frame, date_pattern='dd/mm/yyyy', locale='pt_BR')
        self.entry_data_inicio.grid(column=1, row=1, padx=10, pady=10)

        # Label data de fim
        self.label_data_fim = ttk.Label(self.frame, text="Data de fim da Comiss�o (DD/MM/AAAA):")
        self.label_data_fim.grid(column=0, row=2, padx=10, pady=10)

        # Entry data de fim
        self.entry_data_fim = DateEntry(self.frame, date_pattern='dd/mm/yyyy', locale='pt_BR')
        self.entry_data_fim.grid(column=1, row=2, padx=10, pady=10)

        # Label Observa��es
        self.label_observacoes = ttk.Label(self.frame, text="Observa��es:")
        self.label_observacoes.grid(column=0, row=3, padx=10, pady=10)

        # Entry Observa��es
        self.entry_observacoes = ttk.Entry(self.frame)
        self.entry_observacoes.grid(column=1, row=3, padx=10, pady=10)

        # Label Comiss�es
        self.label_comissoes = ttk.Label(self.frame, text="Comiss�es:")
        self.label_comissoes.grid(column=2, row=0, padx=10, pady=10)

        # ListBox Comiss�es
        self.listbox_comissoes = tk.Listbox(self.frame)
        self.listbox_comissoes.grid(column=2, row=1, rowspan=4, padx=10, pady=10)
             
        self.btn_atualizar = ttk.Button(self.frame, text="Atualizar", command=self.atualizar_comissoes)
        self.btn_atualizar.grid(column=3, row=1, padx=10, pady=10)  # Atualize esta linha


        # Bot�o Inserir
        self.button_inserir = ttk.Button(self.frame, text="Inserir", command=self.inserir_comissao)
        self.button_inserir.grid(column=0, row=4, padx=10, pady=10)



    def atualizar_comissoes(self):
        self.listbox_comissoes.delete(0, tk.END)  # Limpa a ListBox
        comissoes = self.main_window.comissoesdb.get_comissoes()  # Busca as comiss�es no banco de dados
        for comissao in comissoes:
            self.listbox_comissoes.insert(tk.END, comissao[1])  # Atualiza a ListBox com as novas comiss�es

    def inserir_comissao(self):
        # Valida��o de campos
        navio = self.combobox_navio.get()
        if not navio:
            messagebox.showerror("Erro", "Selecione um navio.")
            return

        data_inicio = self.entry_data_inicio.get()
        data_fim = self.entry_data_fim.get()
        # Converter as datas para o tipo datetime
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
            data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Insira uma data v�lida.")
            return

        if data_fim_dt < data_inicio_dt:
            messagebox.showerror("Erro", "A data de fim da comiss�o n�o pode ser anterior � data de in�cio.")
            return

        observacoes = self.entry_observacoes.get()

        # Pegar a comiss�o selecionada na ListBox
        comissao_selecionada_index = self.listbox_comissoes.curselection()
        if not comissao_selecionada_index:
            messagebox.showerror("Erro", "Selecione uma comiss�o.")
            return
        comissao_selecionada = self.listbox_comissoes.get(comissao_selecionada_index)

        # Inserir na TreeView
        self.comissoes_tab.treeview.insert("", "end", values=(navio, comissao_selecionada, data_inicio, data_fim, observacoes))


        # Adicionar comiss�o ao banco de dados
        #self.main_window.db.insert_comissao(navio, data_inicio_dt.strftime("%Y-%m-%d"), data_fim_dt.strftime("%Y-%m-%d"), observacoes)

        # Atualizar a treeview na aba ComissoesTab
        #self.comissoes_tab.carregar_comissoes()

        # Limpar campos ap�s inser��o bem-sucedida
        self.combobox_navio.set('')
        self.entry_data_inicio.set_date(datetime.now())
        self.entry_data_fim.set_date(datetime.now())
        self.entry_observacoes.delete(0, 'end')

        messagebox.showinfo("Sucesso", "Comiss�o inserida com sucesso!")


   




