import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import datetime
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ARQ_NCS = "ncs.json"
ARQ_CFG = "config.json"

# Configurações padrão
DEFAULT_CFG = {
    "unidades": ["KG", "L", "PEÇ"],
    "defeitos": [
        "Aspecto do produto ou MP", "Avarias em baldes", "Avarias em caixas",
        "Avarias em latas", "Avarias em sacarias Transferência", "Avarias no strech",
        "Consistência na mistura", "Contaminação", "Cor despadronizada",
        "Desempenho pós cura", "Desvio de peso ou quantidade",
        "Embalagem com defeito Fornecedor", "Falha de informação do datador"
    ],
    "cores_defeitos": {
        "ASPECTO DO PRODUTO OU MP": "#FFB6B6",
        "AVARIAS EM BALDES": "#FFD580",
        "AVARIAS EM CAIXAS": "#FFFACD",
        "AVARIAS EM LATAS": "#B6FFB6",
        "AVARIAS EM SACARIAS TRANSFERÊNCIA": "#B6E0FF",
        "AVARIAS NO STRECH": "#B6B6FF",
        "CONSISTÊNCIA NA MISTURA": "#E0B6FF",
        "CONTAMINAÇÃO": "#FFB6E0",
        "COR DESPADRONIZADA": "#FFDEB6",
        "DESEMPENHO PÓS CURA": "#B6FFD5",
        "DESVIO DE PESO OU QUANTIDADE": "#B6FFF6",
        "EMBALAGEM COM DEFEITO FORNECEDOR": "#E0FFB6",
        "FALHA DE INFORMAÇÃO DO DATADOR": "#FFB6C1"
    },
    "produtos": [
        {"nome": "PRODUTO INTERNO", "codigo": "0001X0001"},
        {"nome": "PRODUTO EXTERNO", "codigo": "0001X0002"},
        {"nome": "PRODUTO FLEXÍVEL", "codigo": "0001X0003"},
        {"nome": "PRODUTO COLORIDO 1", "codigo": "0002X0001"},
        {"nome": "PRODUTO COLORIDO 2", "codigo": "0002X0002"},
        {"nome": "PRODUTO COLORIDO 3", "codigo": "0002X0003"}
    ]
}

def carregar_cfg():
    if os.path.exists(ARQ_CFG):
        with open(ARQ_CFG, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        salvar_cfg(DEFAULT_CFG)
        return DEFAULT_CFG.copy()

def salvar_cfg(cfg):
    with open(ARQ_CFG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def carregar_ncs():
    if os.path.exists(ARQ_NCS):
        with open(ARQ_NCS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_ncs(ncs):
    with open(ARQ_NCS, "w", encoding="utf-8") as f:
        json.dump(ncs, f, ensure_ascii=False, indent=2)

def descricao_resumida(descricao):
    return (descricao[:40] + "...") if len(descricao) > 43 else descricao

def gerar_numero_registro(ncs):
    ano = datetime.date.today().year
    seq = sum(str(nc["numero_registro"]).startswith(str(ano)) for nc in ncs) + 1
    return f"{ano}-{seq:04d}"

class PainelNCApp:
    VERSAO = "v2.0"

    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Não Conformidades")
        self.cfg = carregar_cfg()
        self.ncs = carregar_ncs()
        self.frames = {}
        self.topbars = {}
        self.criar_frames()
        self.mostrar_frame("menu")

    def criar_topbar(self, parent):
        frame_top = tk.Frame(parent)
        frame_top.pack(fill="x", side="top", anchor="nw")
        self.lbl_topbar = tk.Label(
            frame_top,
            text="",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.lbl_topbar.pack(side="left", padx=8, pady=2)
        self.atualizar_topbar(self.lbl_topbar)
        return frame_top

    def atualizar_topbar(self, label):
        agora = datetime.datetime.now()
        label.config(
            text=f"Versão {self.VERSAO} | {agora.strftime('%d/%m/%Y %H:%M:%S')}"
        )
        label.after(1000, lambda: self.atualizar_topbar(label))

    def criar_frames(self):
        self.frames["menu"] = self.criar_menu()
        self.frames["painel"] = self.criar_painel_nc()
        self.frames["config"] = self.criar_configuracoes()
        self.frames["sobre"] = self.criar_sobre()

    def mostrar_frame(self, nome):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nome].pack(fill="both", expand=True)

    def criar_menu(self):
        frame = tk.Frame(self.root, padx=40, pady=40)
        self.criar_topbar(frame)
        tk.Label(frame, text="SEJA BEM-VINDO AO GERENCIADOR DE NÃO CONFORMIDADES", font=("Arial", 18, "bold")).pack(pady=(20, 10))
        tk.Label(frame, text="MENU PRINCIPAL", font=("Arial", 15, "bold")).pack(pady=10)
        tk.Button(frame, text="PAINEL DE NÃO CONFORMIDADES", font=("Arial", 13, "bold"),
                  width=35, height=2, bg="#4CAF50", fg="white",
                  command=lambda: self.mostrar_frame("painel")).pack(pady=10)
        tk.Button(frame, text="CONFIGURAÇÕES", font=("Arial", 13, "bold"),
                  width=35, height=2, bg="#2196F3", fg="white",
                  command=lambda: self.mostrar_frame("config")).pack(pady=10)
        tk.Button(frame, text="SOBRE", font=("Arial", 13, "bold"),
                  width=35, height=2, bg="#FFC107", fg="black",
                  command=lambda: self.mostrar_frame("sobre")).pack(pady=10)
        tk.Button(frame, text="SAIR DO PROGRAMA", font=("Arial", 13, "bold"),
                  width=35, height=2, bg="#F44336", fg="white",
                  command=self.root.destroy).pack(pady=10)
        return frame

    def criar_painel_nc(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        self.criar_topbar(frame)
        tk.Label(frame, text="PAINEL DE NÃO CONFORMIDADES", font=("Arial", 15, "bold")).pack(pady=10)

        # Frame para tabela ocupar toda a largura
        frame_table = tk.Frame(frame)
        frame_table.pack(fill="both", expand=True)

        colunas = (
            "numero_registro", "data_ocorrencia", "codigo_produto", "produto",
            "total_reprovado", "unidade", "defeito", "descricao_resumida",
            "data_producao", "acao_imediata", "responsavel_acao", "status"
        )
        headers = [
            "Nº Registro", "Data Ocorrência", "Código Produto", "Produto",
            "Total Reprovado", "Unidade", "Defeito", "Descrição Resumida",
            "Data Produção", "Ação Imediata", "Responsável", "Status"
        ]
        self.tree = ttk.Treeview(frame_table, columns=colunas, show="headings", height=16)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        for col, header in zip(colunas, headers):
            self.tree.heading(col, text=header, anchor="w")
            self.tree.column(col, minwidth=80, width=120, anchor="w", stretch=True)
        for defeito, cor in self.cfg["cores_defeitos"].items():
            self.tree.tag_configure(defeito, background=cor)
        self.atualizar_tree()

        # Botões centralizados na parte inferior
        frame_btn = tk.Frame(frame)
        frame_btn.pack(side="bottom", pady=20, fill="x")
        for i in range(5):
            frame_btn.grid_columnconfigure(i, weight=1)
        tk.Button(frame_btn, text="REGISTRAR NOVA", font=("Arial", 11, "bold"),
                  bg="#4CAF50", fg="white", width=18, command=self.nova_nc).grid(row=0, column=0, padx=10, sticky="ew")
        tk.Button(frame_btn, text="EDITAR", font=("Arial", 11, "bold"),
                  bg="#2196F3", fg="white", width=12, command=self.editar_nc).grid(row=0, column=1, padx=10, sticky="ew")
        tk.Button(frame_btn, text="EXCLUIR", font=("Arial", 11, "bold"),
                  bg="#F44336", fg="white", width=12, command=self.excluir_nc).grid(row=0, column=2, padx=10, sticky="ew")
        tk.Button(frame_btn, text="VOLTAR", font=("Arial", 11, "bold"),
                  bg="#757575", fg="white", width=12, command=lambda: self.mostrar_frame("menu")).grid(row=0, column=3, padx=10, sticky="ew")
        tk.Button(frame_btn, text="EXCLUIR TUDO", font=("Arial", 11, "bold"),
                  bg="#B71C1C", fg="white", width=14, command=self.excluir_tudo).grid(row=0, column=4, padx=10, sticky="ew")
        tk.Button(frame_btn, text="GRÁFICO POR DEFEITO", font=("Arial", 11, "bold"),
                  bg="#FF9800", fg="white", width=18, command=self.mostrar_grafico_defeitos).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        tk.Button(frame_btn, text="GRÁFICO POR STATUS", font=("Arial", 11, "bold"),
                  bg="#009688", fg="white", width=18, command=self.mostrar_grafico_status).grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # Tornar o frame principal adaptável
        frame.pack(fill="both", expand=True)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame_table.pack(fill="both", expand=True)
        frame_btn.pack(fill="x", side="bottom")

        return frame

    def atualizar_tree(self):
        self.tree.delete(*self.tree.get_children())
        ncs_ordenadas = sorted(self.ncs, key=lambda nc: nc["numero_registro"])
        for nc in ncs_ordenadas:
            valores = tuple(str(nc.get(col, "")) for col in self.tree["columns"])
            tag = nc.get("defeito", "").upper()
            tag = tag if tag in self.cfg["cores_defeitos"] else ""
            self.tree.insert("", tk.END, values=valores, tags=(tag,))

    def nova_nc(self):
        self.form_nc()

    def editar_nc(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma NC para editar.")
            return
        numero = self.tree.item(selecionado[0])['values'][0]
        for i, nc in enumerate(self.ncs):
            if str(nc.get("numero_registro", "")) == numero:
                self.form_nc(nc, i)
                break

    def excluir_nc(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma NC para excluir.")
            return
        numero = self.tree.item(selecionado[0])['values'][0]
        for i, nc in enumerate(self.ncs):
            if str(nc.get("numero_registro", "")) == numero:
                if messagebox.askyesno("Confirmação", "Deseja realmente excluir esta NC?"):
                    del self.ncs[i]
                    salvar_ncs(self.ncs)
                    self.atualizar_tree()
                    messagebox.showinfo("Sucesso", "NC excluída com sucesso!")
                break

    def excluir_tudo(self):
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir TODAS as NCs?"):
            self.ncs.clear()
            salvar_ncs(self.ncs)
            self.atualizar_tree()
            messagebox.showinfo("Sucesso", "Todas as NCs foram excluídas!")

    def form_nc(self, nc_editar=None, idx_editar=None):
        # Forçar tema padrão para evitar bugs de navegação no calendário
        style = ttk.Style()
        style.theme_use('default')

        top = tk.Toplevel(self.root)
        top.title("Editar NC" if nc_editar else "Cadastrar NC")
        top.grab_set()
        top.resizable(False, False)
        cfg = self.cfg
        produtos = [p["nome"] for p in cfg["produtos"]]
        prod_cod = {p["nome"]: p["codigo"] for p in cfg["produtos"]}
        frame = tk.Frame(top, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        # Campos
        tk.Label(frame, text="Data da Ocorrência:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        cal_data = DateEntry(frame, date_pattern="dd/MM/yyyy", font=("Arial", 11), selectmode="day", showothermonthdays=True)
        cal_data.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Produto:", font=("Arial", 11)).grid(row=0, column=2, sticky="e", pady=5, padx=5)
        cb_produto = ttk.Combobox(frame, values=produtos, state="readonly", font=("Arial", 11))
        cb_produto.grid(row=0, column=3, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Código do Produto:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
        entry_codigo = tk.Entry(frame, state="readonly", font=("Arial", 11))
        entry_codigo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        def atualizar_codigo_produto(event=None):
            produto = cb_produto.get()
            codigo = prod_cod.get(produto, "")
            entry_codigo.config(state="normal")
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, codigo)
            entry_codigo.config(state="readonly")
        cb_produto.bind("<<ComboboxSelected>>", atualizar_codigo_produto)
        tk.Label(frame, text="Total Reprovado:", font=("Arial", 11)).grid(row=1, column=2, sticky="e", pady=5, padx=5)
        entry_total = tk.Entry(frame, font=("Arial", 11))
        entry_total.grid(row=1, column=3, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Unidade de Medida:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
        cb_unidade = ttk.Combobox(frame, values=cfg["unidades"], state="readonly", font=("Arial", 11))
        cb_unidade.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Defeito:", font=("Arial", 11)).grid(row=2, column=2, sticky="e", pady=5, padx=5)
        defeitos_maiusculo = [d.upper() for d in cfg["defeitos"]]
        cb_defeito = ttk.Combobox(frame, values=defeitos_maiusculo, state="readonly", font=("Arial", 11))
        cb_defeito.grid(row=2, column=3, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Descrição (máx 400):", font=("Arial", 11)).grid(row=3, column=0, sticky="ne", pady=5, padx=5)
        txt_descricao = tk.Text(frame, width=40, height=4, font=("Arial", 11))
        txt_descricao.grid(row=3, column=1, columnspan=3, sticky="ew", pady=5, padx=5)
        lbl_contador = tk.Label(frame, text="400 restantes", font=("Arial", 11))
        lbl_contador.grid(row=4, column=1, sticky="w", pady=2, padx=5)
        def atualizar_contador(event=None):
            restante = 400 - len(txt_descricao.get("1.0", "end-1c"))
            lbl_contador.config(text=f"{restante} restantes")
        txt_descricao.bind("<KeyRelease>", atualizar_contador)
        tk.Label(frame, text="Data de Produção:", font=("Arial", 11)).grid(row=5, column=0, sticky="e", pady=5, padx=5)
        # CORREÇÃO: usar selectmode="day", showothermonthdays=True, e year, month, day explícitos
        cal_data_prod = DateEntry(
            frame, date_pattern="dd/MM/yyyy", font=("Arial", 11),
            selectmode="day", showothermonthdays=True
        )
        cal_data_prod.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Ação Imediata:", font=("Arial", 11)).grid(row=6, column=0, sticky="e", pady=5, padx=5)
        opcoes_acao = ["UTILIZAR", "RETRABALHAR", "DESCARTAR", "AGUARDANDO DISPOSIÇÃO"]
        cb_acao = ttk.Combobox(frame, values=opcoes_acao, state="readonly", font=("Arial", 11))
        cb_acao.grid(row=6, column=1, columnspan=3, sticky="ew", pady=5, padx=5)
        tk.Label(frame, text="Responsável pela Ação:", font=("Arial", 11)).grid(row=7, column=0, sticky="e", pady=5, padx=5)
        entry_resp = tk.Entry(frame, width=40, font=("Arial", 11))
        entry_resp.grid(row=7, column=1, columnspan=3, sticky="ew", pady=5, padx=5)
        # Botões
        frame_botoes = tk.Frame(frame)
        frame_botoes.grid(row=8, column=0, columnspan=4, pady=15)
        def salvar():
            if not entry_total.get().isdigit():
                messagebox.showwarning("Aviso", "Total reprovado deve ser um número!")
                return
            descricao = txt_descricao.get("1.0", "end-1c").strip().upper()
            if not descricao:
                messagebox.showwarning("Aviso", "Descrição deve ser preenchida!")
                return
            if len(descricao) > 400:
                messagebox.showwarning("Aviso", "Descrição excede 400 caracteres!")
                return
            nc = {
                "numero_registro": nc_editar["numero_registro"] if nc_editar else gerar_numero_registro(self.ncs),
                "data_ocorrencia": cal_data.get(),
                "codigo_produto": entry_codigo.get(),
                "produto": cb_produto.get(),
                "total_reprovado": int(entry_total.get()),
                "unidade": cb_unidade.get(),
                "defeito": cb_defeito.get(),
                "descricao": descricao,
                "descricao_resumida": descricao_resumida(descricao),
                "data_producao": cal_data_prod.get(),
                "acao_imediata": cb_acao.get(),
                "responsavel_acao": entry_resp.get(),
                "status": nc_editar["status"] if nc_editar else "Aberta"
            }
            if nc_editar:
                self.ncs[idx_editar] = nc
                messagebox.showinfo("Sucesso", "NC editada com sucesso!")
            else:
                self.ncs.append(nc)
                messagebox.showinfo("Sucesso", "NC cadastrada com sucesso!")
            salvar_ncs(self.ncs)
            self.atualizar_tree()
            top.destroy()
        def cancelar():
            top.destroy()
        tk.Button(frame_botoes, text="SALVAR", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  width=20, command=salvar).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="CANCELAR", bg="#F44336", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=cancelar).pack(side="left", padx=10)
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        # Preencher campos se edição
        if nc_editar:
            cal_data.set_date(datetime.datetime.strptime(nc_editar["data_ocorrencia"], "%d/%m/%Y"))
            cb_produto.set(nc_editar["produto"])
            entry_codigo.config(state="normal")
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, nc_editar["codigo_produto"])
            entry_codigo.config(state="readonly")
            entry_total.insert(0, str(nc_editar["total_reprovado"]))
            cb_unidade.set(nc_editar["unidade"])
            cb_defeito.set(nc_editar["defeito"].upper())
            txt_descricao.insert("1.0", nc_editar["descricao"])
            lbl_contador.config(text=f"{400 - len(nc_editar['descricao'])} restantes")
            cal_data_prod.set_date(datetime.datetime.strptime(nc_editar["data_producao"], "%d/%m/%Y"))
            cb_acao.set(nc_editar.get("acao_imediata") or "")
            entry_resp.insert(0, nc_editar["responsavel_acao"])

    def criar_configuracoes(self):
        frame = tk.Frame(self.root, padx=30, pady=30)
        self.criar_topbar(frame)
        tk.Label(frame, text="CONFIGURAÇÕES", font=("Arial", 15, "bold")).pack(pady=10)
        # Unidades
        self.cfg_vars = {}
        def criar_lista_editavel(label, chave):
            tk.Label(frame, text=label, font=("Arial", 11, "bold")).pack(anchor="w", pady=5)
            var = tk.StringVar(value=self.cfg[chave])
            listbox = tk.Listbox(frame, listvariable=var, height=5, selectmode="single", font=("Arial", 11))
            listbox.pack(fill="x", pady=2)
            self.cfg_vars[chave] = (var, listbox)
            btns = tk.Frame(frame)
            btns.pack(fill="x")
            tk.Button(btns, text="Adicionar", width=10, command=lambda: self.adicionar_item(chave)).pack(side="left", padx=2)
            tk.Button(btns, text="Modificar", width=10, command=lambda: self.modificar_item(chave)).pack(side="left", padx=2)
            tk.Button(btns, text="Remover", width=10, command=lambda: self.remover_item(chave)).pack(side="left", padx=2)
        criar_lista_editavel("Unidades de Medida:", "unidades")
        criar_lista_editavel("Defeitos:", "defeitos")
        # Produtos
        tk.Label(frame, text="Produtos (associados ao código):", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)
        self.prod_var = tk.StringVar(value=[f"{p['nome']} - {p['codigo']}" for p in self.cfg["produtos"]])
        self.prod_listbox = tk.Listbox(frame, listvariable=self.prod_var, height=5, selectmode="single", font=("Arial", 11))
        self.prod_listbox.pack(fill="x", pady=2)
        prod_btns = tk.Frame(frame)
        prod_btns.pack(fill="x")
        tk.Button(prod_btns, text="Adicionar", width=10, command=self.adicionar_produto).pack(side="left", padx=2)
        tk.Button(prod_btns, text="Modificar", width=10, command=self.modificar_produto).pack(side="left", padx=2)
        tk.Button(prod_btns, text="Remover", width=10, command=self.remover_produto).pack(side="left", padx=2)
        # Botões SALVAR e VOLTAR lado a lado
        frame_botoes = tk.Frame(frame)
        frame_botoes.pack(pady=10)
        tk.Button(frame_botoes, text="SALVAR CONFIGURAÇÕES", font=("Arial", 11, "bold"),
                  bg="#4CAF50", fg="white", width=25, command=self.salvar_configuracoes).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="VOLTAR", font=("Arial", 11, "bold"),
                  bg="#757575", fg="white", width=15, command=lambda: self.mostrar_frame("menu")).pack(side="left", padx=10)
        return frame

    def modificar_item(self, chave):
        listbox = self.cfg_vars[chave][1]
        idx = listbox.curselection()
        if idx:
            valor_atual = self.cfg[chave][idx[0]]
            novo_valor = simpledialog.askstring("Modificar", f"Novo valor para {chave}:", initialvalue=valor_atual)
            if novo_valor:
                self.cfg[chave][idx[0]] = novo_valor
                self.cfg_vars[chave][0].set(self.cfg[chave])

    def modificar_produto(self):
        idx = self.prod_listbox.curselection()
        if idx:
            produto = self.cfg["produtos"][idx[0]]
            novo_nome = simpledialog.askstring("Modificar Produto", "Novo nome do produto:", initialvalue=produto["nome"])
            novo_codigo = simpledialog.askstring("Modificar Produto", "Novo código do produto:", initialvalue=produto["codigo"])
            if novo_nome and novo_codigo:
                self.cfg["produtos"][idx[0]] = {"nome": novo_nome, "codigo": novo_codigo}
                self.prod_var.set([f"{p['nome']} - {p['codigo']}" for p in self.cfg["produtos"]])

    def adicionar_produto(self):
        novo_nome = simpledialog.askstring("Adicionar Produto", "Nome do produto:")
        if not novo_nome:
            return
        novo_codigo = simpledialog.askstring("Adicionar Produto", "Código do produto:")
        if not novo_codigo:
            return
        self.cfg["produtos"].append({"nome": novo_nome, "codigo": novo_codigo})
        self.prod_var.set([f"{p['nome']} - {p['codigo']}" for p in self.cfg["produtos"]])

    def remover_produto(self):
        idx = self.prod_listbox.curselection()
        if idx:
            if messagebox.askyesno("Remover Produto", "Deseja remover o produto selecionado?"):
                del self.cfg["produtos"][idx[0]]
                self.prod_var.set([f"{p['nome']} - {p['codigo']}" for p in self.cfg["produtos"]])

    def salvar_configuracoes(self):
        salvar_cfg(self.cfg)
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
        self.mostrar_frame("menu")

    def criar_sobre(self):
        frame = tk.Frame(self.root, padx=40, pady=40)
        self.criar_topbar(frame)
        tk.Label(frame, text="SOBRE", font=("Arial", 15, "bold")).pack(pady=10)
        tk.Label(frame, text="Painel de Não Conformidades\nDesenvolvido por Vicente\n2025", font=("Arial", 12)).pack(pady=10)
        tk.Button(frame, text="VOLTAR", font=("Arial", 11, "bold"),
                  bg="#757575", fg="white", width=15, command=lambda: self.mostrar_frame("menu")).pack(pady=10)
        return frame

    def mostrar_grafico_defeitos(self):
        contagem = {}
        for nc in self.ncs:
            defeito = nc.get("defeito", "N/A")
            contagem[defeito] = contagem.get(defeito, 0) + 1
        if not contagem:
            messagebox.showinfo("Gráfico", "Nenhum registro para exibir.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(contagem.keys(), contagem.values(), color="#2196F3")
        ax.set_title("Total de Registros por Defeito")
        ax.set_ylabel("Quantidade")
        ax.set_xlabel("Defeito")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        self._exibir_grafico(fig)

    def mostrar_grafico_status(self):
        contagem = {}
        for nc in self.ncs:
            status = nc.get("status", "N/A")
            contagem[status] = contagem.get(status, 0) + 1
        if not contagem:
            messagebox.showinfo("Gráfico", "Nenhum registro para exibir.")
            return
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(contagem.values(), labels=contagem.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Total de Registros por Status")
        plt.tight_layout()
        self._exibir_grafico(fig)

    def _exibir_grafico(self, fig):
        win = tk.Toplevel(self.root)
        win.title("Gráfico")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        tk.Button(win, text="Fechar", command=win.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Painel de Não Conformidades")
    root.geometry("1200x650")
    root.minsize(900, 500)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = PainelNCApp(root)
    root.mainloop()