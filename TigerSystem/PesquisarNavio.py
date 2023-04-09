# -*- coding: iso-8859-1 -*-
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from DatabaseNavios import DatabaseNavios
from DatabaseComissoes import DatabaseComissoes  # Adicionar esta linha
import tkinter.simpledialog





class PesquisarNavio:
    def __init__(self, parent, comissoes_treeview, root, naviosdb, comissoesdb):
        self.frame = tk.Frame(parent)  # Adicione esta linha
        self.parent = parent
        self.comissoes_treeview = comissoes_treeview
        self.root = root
        self.naviosdb = naviosdb
        self.comissoesdb = comissoesdb
        self.create_widgets()         


    def create_widgets(self):

        
        # Navios
        navios = [""] + [navio[1] for navio in self.naviosdb.get_navios()]
        self.navio_combobox = ttk.Combobox(self.frame, values=navios, state="readonly")
        self.navio_combobox.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.navio_combobox.set("Selecione um navio")

        # Comissões
        comissoes_list = [""] + [comissao[1] for comissao in self.comissoesdb.get_comissoes()]
        self.comissao_combobox = ttk.Combobox(self.frame, values=comissoes_list, state="readonly")
        self.comissao_combobox.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.comissao_combobox.set("Selecione uma comissão")

        # Data de início
        self.data_inicio_entry = DateEntry(self.frame, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        self.data_inicio_entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Data de término
        self.data_fim_entry = DateEntry(self.frame, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        self.data_fim_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Botão de pesquisa
        self.pesquisar_button = ttk.Button(self.frame, text="Pesquisar", command=self.pesquisar)
        self.pesquisar_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Caixa de texto de resultados
        self.resultados_text = tk.Text(self.frame, wrap=tk.WORD)
        self.resultados_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Altere todas as chamadas de self.root para self.frame
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)  # Adicione esta linha
        self.parent.rowconfigure(0, weight=1)

        # Função para habilitar/desabilitar campos de data
        def toggle_date_fields():
            if self.disable_dates_var.get():
                self.data_inicio_entry.delete(0, 'end')
                self.data_fim_entry.delete(0, 'end')
                self.data_inicio_entry.config(state='disabled')
                self.data_fim_entry.config(state='disabled')
            else:
                self.data_inicio_entry.config(state='normal')
                self.data_fim_entry.config(state='normal')

        # Caixa de seleção para desabilitar/habilitar campos de data
        self.disable_dates_var = tk.BooleanVar()
        self.disable_dates_checkbutton = tk.Checkbutton(self.frame, text="Desabilitar datas", variable=self.disable_dates_var, command=toggle_date_fields)
        self.disable_dates_checkbutton.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        # Data de início
        self.data_inicio_entry = DateEntry(self.frame, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        self.data_inicio_entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Data de término
        self.data_fim_entry = DateEntry(self.frame, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        self.data_fim_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    def pesquisar(self):

        # Limpar combobox de navios e comissões selecionados
        #self.navio_combobox.current(0)
        #self.comissao_combobox.current(0)

        navio_selecionado = self.navio_combobox.get()
        comissao_selecionada = self.comissao_combobox.get()
        data_inicio_selecionada = self.data_inicio_entry.get_date() if self.data_inicio_entry.get() else None
        data_fim_selecionada = self.data_fim_entry.get_date() if self.data_fim_entry.get() else None

        # Verifique se os valores selecionados são válidos
        if navio_selecionado in ["", "Selecione um navio"]:
            navio_selecionado = None
        if comissao_selecionada in ["", "Selecione uma comissão"]:
            comissao_selecionada = None

        self.resultados_text.delete('1.0', 'end')  # Limpar os resultados anteriores

        todas_linhas = self.comissoes_treeview.get_children()

        if self.disable_dates_var.get():
            if navio_selecionado and not comissao_selecionada:
                comissoes = []

                for linha in todas_linhas:
                    valores = self.comissoes_treeview.item(linha)['values']
                    navio, comissao, data_inicio, data_fim, _ = valores

                    if navio_selecionado == navio:
                        periodo = f"{data_inicio} - {data_fim}"
                        comissoes.append((comissao, periodo))

                comissoes_str = [f"{c} ({p})" for c, p in comissoes]
                mensagem = f"O {navio_selecionado} esta/estará nas seguintes comissões: {', '.join(sorted(comissoes_str))}"
                self.resultados_text.insert('end', mensagem + '\n')

            elif comissao_selecionada and not navio_selecionado:
                navios = set()
                periodo_comissao = ""
                for linha in todas_linhas:
                    valores = self.comissoes_treeview.item(linha)['values']
                    navio, comissao, data_inicio, data_fim, _ = valores

                    if comissao_selecionada == comissao:
                        navios.add(navio)
                        periodo_comissao = f"{data_inicio} - {data_fim}"

                mensagem = f"Na comissão {comissao_selecionada}, que ocorrerá no período de {periodo_comissao}, estará/estarão os seguintes navios: {', '.join(sorted(navios))}"
                self.resultados_text.insert('end', mensagem + '\n')

            elif navio_selecionado and comissao_selecionada:
                mensagem = f"O {navio_selecionado} estará na comissão {comissao_selecionada}, durante os seguintes períodos:"
                self.resultados_text.insert('end', mensagem + '\n')

                periodos = []

                for linha in todas_linhas:
                    valores = self.comissoes_treeview.item(linha)['values']
                    navio, comissao, data_inicio, data_fim, observacoes = valores

                    data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
                    data_fim = datetime.strptime(data_fim, "%d/%m/%Y").date()

                    if navio_selecionado == navio and comissao_selecionada == comissao:
                        periodos.append((data_inicio, data_fim))

                if not periodos:
                    self.resultados_text.insert('end', "Nenhum período encontrado para este navio e comissão\n")
                else:
                    for inicio, fim in periodos:
                        mensagem = f"{inicio.strftime('%d/%m/%Y')} - {fim.strftime('%d/%m/%Y')}"
                        self.resultados_text.insert('end', mensagem + '\n')

            else:
                self.resultados_text.insert('end', "Nenhuma opção selecionada\n")
                return

        else:
        # Seu código original para pesquisar por Navio, Comissão e datas
        # ...
            # Seu código original para pesquisar por Navio, Comissão e datas
            navios_em_comissao = []

            # Buscar todas as linhas na Treeview
            todas_linhas = self.comissoes_treeview.get_children()

            # Iterar sobre as linhas e aplicar as regras de pesquisa

            # Iterar sobre as linhas e aplicar as regras de pesquisa
            for linha in todas_linhas:
                valores = self.comissoes_treeview.item(linha)['values']
                navio, comissao, data_inicio, data_fim, observacoes = valores

                data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
                data_fim = datetime.strptime(data_fim, "%d/%m/%Y").date()

                navio_match = navio_selecionado == navio or not navio_selecionado
                comissao_match = comissao_selecionada == comissao or not comissao_selecionada
                date_match = (data_inicio_selecionada is None and data_fim_selecionada is None) or \
                            (data_inicio_selecionada <= data_inicio <= data_fim_selecionada) or \
                            (data_inicio_selecionada <= data_fim <= data_fim_selecionada) or \
                            (data_inicio <= data_inicio_selecionada and data_fim >= data_fim_selecionada)

                if navio_match and comissao_match and date_match:
                    navios_em_comissao.append((navio, comissao, data_inicio, data_fim))

            if not navios_em_comissao:
                self.resultados_text.insert('end', "Nenhum navio está em comissão\n")
            else:
                for navio, comissao, data_inicio, data_fim in navios_em_comissao:
                    mensagem = f"{navio} está em comissão no período selecionado e a comissão {comissao} é do dia {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
                    self.resultados_text.insert('end', mensagem + '\n')



    

       



