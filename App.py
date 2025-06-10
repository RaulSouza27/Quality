import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import datetime
import json
import os

ncs = []
ARQUIVO_NCS = "ncs.json"

CODIGOS_PRODUTO = [
    "0001X0001", "0001X0002", "0001X0003",
    "0002X0001", "0002X0002", "0002X0003"
]
PRODUTOS = [
    "PRODUTO INTERNO", "PRODUTO EXTERNO", "PRODUTO FLEXÍVEL",
    "PRODUTO COLORIDO 1", "PRODUTO COLORIDO 2", "PRODUTO COLORIDO 3"
]
UNIDADES = ["KG", "L", "PEÇ"]
DEFEITOS = [
    "Aspecto do produto ou MP", "Avarias em baldes", "Avarias em caixas",
    "Avarias em latas", "Avarias em sacarias Transferência", "Avarias no strech",
    "Consistência na mistura", "Contaminação", "Cor despadronizada",
    "Desempenho pós cura", "Desvio de peso ou quantidade",
    "Embalagem com defeito Fornecedor", "Falha de informação do datador"
]

PRODUTO_CODIGO = dict(zip(PRODUTOS, CODIGOS_PRODUTO))

CORES_DEFEITOS = {
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
}

def descricao_resumida(descricao):
    return (descricao[:40] + "...") if len(descricao) > 43 else descricao

def gerar_numero_registro():
    ano = datetime.date.today().year
    seq = sum(str(nc["numero_registro"]).startswith(str(ano)) for nc in ncs) + 1
    return f"{ano}-{seq:04d}"

colunas = (
    "numero_registro", "data_ocorrencia", "codigo_produto", "produto",
    "total_reprovado", "unidade", "defeito", "descricao_resumida",
    "data_producao", "acao_imediata", "responsavel_acao", "status"
)

tree = None

def criar_treeview(frame):
    global tree
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 11))
    style.configure("Treeview", font=("Arial", 11), rowheight=28)
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=12)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    headers = [
        "Nº Registro", "Data Ocorrência", "Código Produto", "Produto",
        "Total Reprovado", "Unidade", "Defeito", "Descrição Resumida",
        "Data Produção", "Ação Imediata", "Responsável", "Status"
    ]
    for col, header in zip(colunas, headers):
        tree.heading(col, text=header, anchor="w")
        tree.column(col, minwidth=80, width=120, anchor="w")
    for defeito, cor in CORES_DEFEITOS.items():
        tree.tag_configure(defeito, background=cor)

def atualizar_lista():
    if tree:
        tree.delete(*tree.get_children())
        for nc in ncs:
            defeito = str(nc.get("defeito", "")).upper()
            valores = tuple(str(nc.get(col, "")).upper() for col in colunas)
            tag = defeito if defeito in CORES_DEFEITOS else ""
            tree.insert("", tk.END, values=valores, tags=(tag,))

def salvar_ncs():
    with open(ARQUIVO_NCS, "w", encoding="utf-8") as f:
        json.dump(ncs, f, ensure_ascii=False, indent=2)

def carregar_ncs():
    if os.path.exists(ARQUIVO_NCS):
        with open(ARQUIVO_NCS, "r", encoding="utf-8") as f:
            ncs.clear()
            ncs.extend(json.load(f))

def cadastrar_nc(nc_editar=None, idx_editar=None):
    def atualizar_codigo_produto(event=None):
        produto = cb_produto.get()
        codigo = PRODUTO_CODIGO.get(produto, "")
        entry_codigo.config(state="normal")
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)
        entry_codigo.config(state="readonly")

    def limpar_campos():
        cal_data.set_date(datetime.date.today())
        cb_produto.set("")
        entry_codigo.config(state="normal")
        entry_codigo.delete(0, tk.END)
        entry_codigo.config(state="readonly")
        entry_total.delete(0, tk.END)
        cb_unidade.set("")
        cb_defeito.set("")
        txt_descricao.delete("1.0", tk.END)
        lbl_contador.config(text="400 restantes")
        cal_data_prod.set_date(datetime.date.today())
        entry_acao.delete(0, tk.END)
        entry_resp.delete(0, tk.END)

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
            "numero_registro": nc_editar["numero_registro"] if nc_editar else gerar_numero_registro(),
            "data_ocorrencia": cal_data.get(),
            "codigo_produto": entry_codigo.get(),
            "produto": cb_produto.get(),
            "total_reprovado": int(entry_total.get()),
            "unidade": cb_unidade.get(),
            "defeito": cb_defeito.get(),
            "descricao": descricao,
            "descricao_resumida": descricao_resumida(descricao),
            "data_producao": cal_data_prod.get(),
            "acao_imediata": entry_acao.get(),
            "responsavel_acao": entry_resp.get(),
            "status": nc_editar["status"] if nc_editar else "Aberta"
        }
        if nc_editar:
            ncs[idx_editar] = nc
            messagebox.showinfo("Sucesso", "NC editada com sucesso!")
        else:
            ncs.append(nc)
            messagebox.showinfo("Sucesso", "NC cadastrada com sucesso!")
        atualizar_lista()
        salvar_ncs()
        top.destroy()

    def cancelar():
        top.destroy()

    top = tk.Toplevel(janela)
    top.title("Editar NC" if nc_editar else "Cadastrar NC")
    top.grab_set()
    top.resizable(False, False)

    frame_form = tk.Frame(top, padx=20, pady=20)
    frame_form.pack(fill="both", expand=True)

    tk.Label(frame_form, text="Data da Ocorrência:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    cal_data = DateEntry(frame_form, date_pattern="dd/MM/yyyy", font=("Arial", 11))
    cal_data.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Produto:", font=("Arial", 11)).grid(row=0, column=2, sticky="e", pady=5, padx=5)
    cb_produto = ttk.Combobox(frame_form, values=PRODUTOS, state="readonly", font=("Arial", 11))
    cb_produto.grid(row=0, column=3, sticky="ew", pady=5, padx=5)
    cb_produto.bind("<<ComboboxSelected>>", atualizar_codigo_produto)

    tk.Label(frame_form, text="Código do Produto:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_codigo = tk.Entry(frame_form, state="readonly", font=("Arial", 11))
    entry_codigo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Total Reprovado:", font=("Arial", 11)).grid(row=1, column=2, sticky="e", pady=5, padx=5)
    entry_total = tk.Entry(frame_form, font=("Arial", 11))
    entry_total.grid(row=1, column=3, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Unidade de Medida:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    cb_unidade = ttk.Combobox(frame_form, values=UNIDADES, state="readonly", font=("Arial", 11))
    cb_unidade.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Defeito:", font=("Arial", 11)).grid(row=2, column=2, sticky="e", pady=5, padx=5)
    defeitos_maiusculo = [d.upper() for d in DEFEITOS]
    cb_defeito = ttk.Combobox(frame_form, values=defeitos_maiusculo, state="readonly", font=("Arial", 11))
    cb_defeito.grid(row=2, column=3, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Descrição (máx 400):", font=("Arial", 11)).grid(row=3, column=0, sticky="ne", pady=5, padx=5)
    txt_descricao = tk.Text(frame_form, width=40, height=4, font=("Arial", 11))
    txt_descricao.grid(row=3, column=1, columnspan=3, sticky="ew", pady=5, padx=5)
    lbl_contador = tk.Label(frame_form, text="400 restantes", font=("Arial", 11))
    lbl_contador.grid(row=4, column=1, sticky="w", pady=2, padx=5)

    def atualizar_contador(event=None):
        restante = 400 - len(txt_descricao.get("1.0", "end-1c"))
        lbl_contador.config(text=f"{restante} restantes")
    txt_descricao.bind("<KeyRelease>", atualizar_contador)

    tk.Label(frame_form, text="Data de Produção:", font=("Arial", 11)).grid(row=5, column=0, sticky="e", pady=5, padx=5)
    cal_data_prod = DateEntry(frame_form, date_pattern="dd/MM/yyyy", font=("Arial", 11))
    cal_data_prod.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Ação Imediata:", font=("Arial", 11)).grid(row=6, column=0, sticky="e", pady=5, padx=5)
    entry_acao = tk.Entry(frame_form, width=40, font=("Arial", 11))
    entry_acao.grid(row=6, column=1, columnspan=3, sticky="ew", pady=5, padx=5)

    tk.Label(frame_form, text="Responsável pela Ação:", font=("Arial", 11)).grid(row=7, column=0, sticky="e", pady=5, padx=5)
    entry_resp = tk.Entry(frame_form, width=40, font=("Arial", 11))
    entry_resp.grid(row=7, column=1, columnspan=3, sticky="ew", pady=5, padx=5)

    frame_botoes = tk.Frame(frame_form)
    frame_botoes.grid(row=8, column=0, columnspan=4, pady=15)

    btn_salvar = tk.Button(frame_botoes, text="SALVAR ALTERAÇÕES" if nc_editar else "SALVAR NÃO CONFORMIDADE",
                           bg="#2196F3" if nc_editar else "#4CAF50", fg="white", font=("Arial", 11, "bold"),
                           width=25, command=salvar)
    btn_salvar.pack(side="left", padx=10)

    btn_limpar = tk.Button(frame_botoes, text="LIMPAR", bg="#eeeeee", fg="#444444", font=("Arial", 11, "bold"), width=15, command=limpar_campos)
    btn_limpar.pack(side="left", padx=10)

    btn_cancelar = tk.Button(frame_botoes, text="CANCELAR", bg="#F44336", fg="white", font=("Arial", 11, "bold"), width=15, command=cancelar)
    btn_cancelar.pack(side="left", padx=10)

    for i in range(4):
        frame_form.columnconfigure(i, weight=1)

    # Se for edição, preencha os campos
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
        entry_acao.insert(0, nc_editar["acao_imediata"])
        entry_resp.insert(0, nc_editar["responsavel_acao"])

def visualizar_geral():
    for widget in janela.winfo_children():
        widget.destroy()
    frame = tk.Frame(janela, padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    colunas_visao = ("numero_registro", "data_ocorrencia", "produto", "defeito", "total_reprovado", "status")
    headers = [
        "NÚMERO DE REGISTRO", "DATA DE OCORRÊNCIA", "PRODUTO", "DEFEITO", "TOTAL DA NÃO CONFORMIDADE", "STATUS"
    ]

    tree_visao = ttk.Treeview(frame, columns=colunas_visao, show="headings", height=15)
    tree_visao.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree_visao.yview)
    tree_visao.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for col, header in zip(colunas_visao, headers):
        tree_visao.heading(col, text=header, anchor="w")
        tree_visao.column(col, minwidth=80, width=150, anchor="w")

    def atualizar_visao():
        tree_visao.delete(*tree_visao.get_children())
        for nc in ncs:
            valores = (
                str(nc.get("numero_registro", "")).upper(),
                str(nc.get("data_ocorrencia", "")).upper(),
                str(nc.get("produto", "")).upper(),
                str(nc.get("defeito", "")).upper(),
                str(nc.get("total_reprovado", "")).upper(),
                str(nc.get("status", "")).upper()
            )
            tree_visao.insert("", tk.END, values=valores)

    def acao_novo():
        cadastrar_nc()
        atualizar_visao()

    def acao_editar():
        selecionado = tree_visao.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma NC para editar.")
            return
        numero = tree_visao.item(selecionado[0])['values'][0]
        for i, nc in enumerate(ncs):
            if str(nc.get("numero_registro", "")).upper() == numero:
                editar_nc_idx(i)
                break
        atualizar_visao()

    def acao_excluir():
        selecionado = tree_visao.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma NC para excluir.")
            return
        numero = tree_visao.item(selecionado[0])['values'][0]
        for i, nc in enumerate(ncs):
            if str(nc.get("numero_registro", "")).upper() == numero:
                if messagebox.askyesno("Confirmação", "Deseja realmente excluir esta NC?"):
                    del ncs[i]
                    salvar_ncs()
                    atualizar_visao()
                    messagebox.showinfo("Sucesso", "NC excluída com sucesso!")
                break

    def acao_limpar():
        if messagebox.askyesno("Confirmação", "Deseja realmente apagar TODAS as não conformidades?"):
            ncs.clear()
            salvar_ncs()
            atualizar_visao()
            messagebox.showinfo("Sucesso", "Todas as não conformidades foram removidas.")

    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    btn_novo = tk.Button(frame_botoes, text="CRIAR NOVO REGISTRO", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=22, command=acao_novo)
    btn_novo.grid(row=0, column=0, padx=10, pady=5)

    btn_editar = tk.Button(frame_botoes, text="EDITAR", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", width=15, command=acao_editar)
    btn_editar.grid(row=0, column=1, padx=10, pady=5)

    btn_excluir = tk.Button(frame_botoes, text="EXCLUIR", font=("Arial", 11, "bold"), bg="#F44336", fg="white", width=15, command=acao_excluir)
    btn_excluir.grid(row=0, column=2, padx=10, pady=5)

    btn_limpar = tk.Button(frame_botoes, text="LIMPAR", font=("Arial", 11, "bold"), bg="#eeeeee", fg="#444444", width=15, command=acao_limpar)
    btn_limpar.grid(row=0, column=3, padx=10, pady=5)

    btn_fechar = tk.Button(frame_botoes, text="FECHAR", font=("Arial", 11, "bold"), bg="#757575", fg="white", width=15, command=janela.destroy)
    btn_fechar.grid(row=0, column=4, padx=10, pady=5)

    atualizar_visao()

def editar_nc_idx(idx):
    cadastrar_nc(ncs[idx], idx)

# --- No final do arquivo, troque por:
if __name__ == "__main__":
    carregar_ncs()
    # Crie a janela principal
    janela = tk.Tk()
    janela.title("Visualização Geral de Não Conformidades")
    janela.geometry("950x550")
    # Chame a visualização geral (sem argumentos)
    visualizar_geral()
    janela.mainloop()
