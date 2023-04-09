
# -*- coding: iso-8859-1 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from inserir_comissoes_tab import InserirComissoesTab
from AdicionarComissoes import AdicionarComissoesTab
from PesquisarNavio import PesquisarNavio
from ComissoesTab import ComissoesTab
from AdicionarNavios import AdicionarNaviosTab
from DatabaseNavios import DatabaseNavios
import os
from tkinter import Label, E
from Database import Database
from DatabaseComissoes import DatabaseComissoes  # Adicionar esta linha



# verifica se o arquivo do banco de dados já existe
if not os.path.isfile('database.db'):
            db = Database('database.db')
            print('Banco de dados criado com sucesso!')
else:
            db = Database('database.db')



    



class MainWindow:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = tk.Tk()
        self.root.geometry("1280x800")
        self.root.title("TigerSystem")
        self.db = Database('database.db')  # Mantenha apenas esta instância do banco de dados
        #.database = Database('database.db')
        self.comissoesdb = DatabaseComissoes('comissoesdb.db')  # Cria uma nova instância da database comissões
        self.naviosdb = DatabaseNavios('naviosdb.db')  # Cria uma nova instância da database navios
        self.tab_control = ttk.Notebook(self.root)
        self.create_tabs()
        self.comissoes_adicionadas = []
        # Altere o ícone da janela principal
        self.root.iconbitmap('@tiger.xbm')



    def set_window_icon(self, window):
        window.iconbitmap('@tiger.xbm')
    

    def abrir_janela_edicao_comissao(self, item_id, navio, comissoes, data_inicio, data_fim, observacoes):
        janela_edicao = tk.Toplevel(self.root)  # Modificado de self.window para self.root
        janela_edicao.title('Editar Comissão')

        # Definir o ícone para a janela de edição de comissão
        self.set_window_icon(janela_edicao)


        # Inicialize os objetos do banco de dados
        db_navios = DatabaseNavios("naviosdb.db")
        db_comissoes = DatabaseComissoes("comissoesdb.db")

        # Obtenha a lista de navios e comissoes
        navios = [navio[1] for navio in self.naviosdb.get_navios()]
        comissoes_list = [comissao[1] for comissao in self.comissoesdb.get_comissoes()]

        def convert_item_id_to_int(item_id):
            return int(item_id[1:])


        # Crie os labels e os campos de entrada para editar as informações
        Label(janela_edicao, text="Navio:").grid(row=0, column=0, padx=10, pady=(20, 0), sticky=E)
        navio_entry = ttk.Combobox(janela_edicao, values=navios, state="readonly")
        navio_entry.grid(row=0, column=1, padx=10, pady=(20, 0))
        navio_entry.set(navio)

        Label(janela_edicao, text="Comissões:").grid(row=1, column=0, padx=10, pady=(10, 0), sticky=E)
        comissoes_entry = ttk.Combobox(janela_edicao, values=comissoes_list, state="readonly")
        comissoes_entry.grid(row=1, column=1, padx=10, pady=(10, 0))
        comissoes_entry.set(comissoes)

        data_inicio_label = ttk.Label(janela_edicao, text="Data de Início:")
        data_inicio_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="w")
        data_inicio_entry = DateEntry(janela_edicao, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        data_inicio_entry.grid(row=2, column=1, padx=10, pady=10)
        data_inicio_entry.set_date(data_inicio)

        data_fim_label = ttk.Label(janela_edicao, text="Data de Término:")
        data_fim_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="w")
        data_fim_entry = DateEntry(janela_edicao, width=30, locale='pt_BR', date_pattern='dd/MM/yyyy')
        data_fim_entry.grid(row=3, column=1, padx=10, pady=10)
        data_fim_entry.set_date(data_fim)

        observacoes_label = ttk.Label(janela_edicao, text="Observações:")
        observacoes_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="w")
        observacoes_entry = ttk.Entry(janela_edicao, width=30)
        observacoes_entry.grid(row=4, column=1, padx=10, pady=10)
        observacoes_entry.insert(0, observacoes)

        def salvar_edicao():
            item_id_int = convert_item_id_to_int(item_id)
    
            # Atualize o banco de dados com as informações editadas
            self.db.update_comissao(
                item_id_int,
                navio_entry.get(),
                comissoes_entry.get(),
                data_inicio_entry.get(),
                data_fim_entry.get(),
                observacoes_entry.get()
            )

            # Atualize a Treeview com as informações editadas
            self.comissoes_tab.treeview.item(
                item_id,
                values=(
                    navio_entry.get(),
                    comissoes_entry.get(),
                    data_inicio_entry.get(),
                    data_fim_entry.get(),
                    observacoes_entry.get()
                )
            )

            janela_edicao.destroy()


           
        # Crie o botão 'Salvar' e associe-o à função salvar_edicao
        salvar_button = ttk.Button(janela_edicao, text="Salvar", command=salvar_edicao)
        salvar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0), ipadx=60)

        janela_edicao.mainloop()

        


    def create_widgets(self):
        self.create_tabs()
        self.root.protocol("WM_DELETE_WINDOW", self.save_comissoes)

    

    
    def create_tabs(self):

        

        # Aba 3 - Comissões
        tab3 = ComissoesTab(self.tab_control, self)  # Corrigido: passar self como o segundo argumento
        self.tab_control.add(tab3.frame, text='Comissões')
        self.comissoes_tab = tab3  # Adicione esta linha para criar o atributo comissoes_tab


        # Aba 1 - Pesquisar Navios
        tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab1, text='Pesquisar Navios')

        # Adicionar objeto PesquisarNavio à aba Pesquisar Navios
        self.pesquisar_navio_tab = PesquisarNavio(tab1, self.comissoes_tab.treeview, self.root, self.naviosdb, self.comissoesdb)
        self.pesquisar_navio_tab.frame.grid(row=0, column=0, sticky='nsew')  # Adicione esta linha
                       
        #Aba 5 - Adicionar Navios
        # Adicione a nova aba Adicionar Navios
        tab5 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab5, text='Adicionar Navios')   
        
        # Adicionar objeto AdicionarNaviosTab à aba Adicionar Navios
        self.adicionar_navios_tab = AdicionarNaviosTab(tab5, self)
        self.adicionar_navios_tab.frame.pack()  # Adicione esta linha

         # Aba 2 - Inserir Comissões
        tab2 = InserirComissoesTab(self.tab_control, self, tab3)
        self.tab_control.add(tab2.frame, text='Inserir Comissões')                           

        
        # Aba 4 - Adicionar Comissões
        tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab4, text='Adicionar Comissões')

        # Adicionar objeto AdicionarComissoesTab à aba Adicionar Comissões
        self.adicionar_comissoes_tab = AdicionarComissoesTab(tab4, self)
        self.adicionar_comissoes_tab.frame.pack()

        # Aba Sobre
        tab_sobre = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_sobre, text='Sobre')

        sobre_texto = "Programa desenvolvido pelo CC BRUNO SIQUEIRA.\nVersão 0.5"
        sobre_label = tk.Label(tab_sobre, text=sobre_texto, wraplength=400, justify=tk.CENTER)
        sobre_label.pack(padx=10, pady=(50, 0))
        

        # Mostra as abas
        self.tab_control.pack(expand=1, fill='both')
     
        
    def save_navios(self):
            self.naviosdb.save_navios(self.adicionar_navios_tab.get_navios())
                                                                        


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
    
