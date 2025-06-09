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

PRODUTO_CODIGO = {
    "PRODUTO INTERNO": "0001X0001",
    "PRODUTO EXTERNO": "0001X0002",
    "PRODUTO FLEXÍVEL": "0001X0003",
    "PRODUTO COLORIDO 1": "0002X0001",
    "PRODUTO COLORIDO 2": "0002X0002",
    "PRODUTO COLORIDO 3": "0002X0003"
}

def gerar_numero_registro():
    ano = datetime.date.today().year
    registros_ano = [nc for nc in ncs if str(nc["numero_registro"]).startswith(str(ano))]
    seq = len(registros_ano) + 1
    return f"{ano}-{seq:04d}"

colunas = (
    "numero_registro", "data_ocorrencia", "codigo_produto", "produto",
    "total_reprovado", "unidade", "defeito", "descricao",
    "data_producao", "acao_imediata", "responsavel_acao", "status"
)

tree = None

def criar_treeview(frame):
    global tree
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=28)
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=12)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # Barra de rolagem
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Defina os cabeçalhos
    headers = [
        "Nº Registro", "Data Ocorrência", "Código Produto", "Produto",
        "Total Reprovado", "Unidade", "Defeito", "Descrição",
        "Data Produção", "Ação Imediata", "Responsável", "Status"
    ]
    for col, header in zip(colunas, headers):
        tree.heading(col, text=header)
        tree.column(col, minwidth=80, width=120, anchor="center")

def atualizar_lista():
    if tree is not None:
        tree.delete(*tree.get_children())
        for nc in ncs:
            valores = (
                str(nc.get("numero_registro", "")).upper(),
                str(nc.get("data_ocorrencia", "")).upper(),
                str(nc.get("codigo_produto", "")).upper(),
                str(nc.get("produto", "")).upper(),
                str(nc.get("total_reprovado", "")).upper(),
                str(nc.get("unidade", "")).upper(),
                str(nc.get("defeito", "")).upper(),
                str(nc.get("descricao", "")).upper(),
                str(nc.get("data_producao", "")).upper(),
                str(nc.get("acao_imediata", "")).upper(),
                str(nc.get("responsavel_acao", "")).upper(),
                str(nc.get("status", "")).upper()
            )
            tree.insert("", tk.END, values=valores)

def cadastrar_nc():
    def atualizar_codigo_produto(event=None):
        produto = cb_produto.get()
        codigo = PRODUTO_CODIGO.get(produto, "")
        entry_codigo.config(state="normal")
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)
        entry_codigo.config(state="readonly")

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
            "numero_registro": gerar_numero_registro(),
            "data_ocorrencia": cal_data.get(),
            "codigo_produto": entry_codigo.get(),
            "produto": cb_produto.get(),
            "total_reprovado": int(entry_total.get()),
            "unidade": cb_unidade.get(),
            "defeito": cb_defeito.get(),
            "descricao": descricao,
            "data_producao": cal_data_prod.get() + " - " + entry_hora_prod.get(),
            "acao_imediata": entry_acao.get(),
            "responsavel_acao": entry_resp.get(),
            "status": "Aberta"
        }
        ncs.append(nc)
        atualizar_lista()
        salvar_ncs()
        top.destroy()
        messagebox.showinfo("Sucesso", "NC cadastrada com sucesso!")

    top = tk.Toplevel(janela)
    top.title("Cadastrar NC")
    top.grab_set()
    top.resizable(False, False)

    frame_form = tk.Frame(top, padx=10, pady=10)
    frame_form.pack()

    tk.Label(frame_form, text="Data da Ocorrência:").grid(row=0, column=0, sticky="e")
    cal_data = DateEntry(frame_form, date_pattern="dd/MM/yyyy")
    cal_data.grid(row=0, column=1)

    tk.Label(frame_form, text="Produto:").grid(row=1, column=0, sticky="e")
    cb_produto = ttk.Combobox(frame_form, values=PRODUTOS, state="readonly")
    cb_produto.grid(row=1, column=1)
    cb_produto.bind("<<ComboboxSelected>>", atualizar_codigo_produto)

    tk.Label(frame_form, text="Código do Produto:").grid(row=2, column=0, sticky="e")
    entry_codigo = tk.Entry(frame_form, state="readonly")
    entry_codigo.grid(row=2, column=1)

    tk.Label(frame_form, text="Total Reprovado:").grid(row=3, column=0, sticky="e")
    entry_total = tk.Entry(frame_form)
    entry_total.grid(row=3, column=1)

    tk.Label(frame_form, text="Unidade de Medida:").grid(row=4, column=0, sticky="e")
    cb_unidade = ttk.Combobox(frame_form, values=UNIDADES, state="readonly")
    cb_unidade.grid(row=4, column=1)

    tk.Label(frame_form, text="Defeito:").grid(row=5, column=0, sticky="e")
    defeitos_maiusculo = [d.upper() for d in DEFEITOS]
    cb_defeito = ttk.Combobox(frame_form, values=defeitos_maiusculo, state="readonly")
    cb_defeito.grid(row=5, column=1)

    tk.Label(frame_form, text="Descrição (máx 400):").grid(row=6, column=0, sticky="ne")
    txt_descricao = tk.Text(frame_form, width=40, height=4)
    txt_descricao.grid(row=6, column=1)
    lbl_contador = tk.Label(frame_form, text="400 restantes")
    lbl_contador.grid(row=7, column=1, sticky="w")

    def atualizar_contador(event=None):
        restante = 400 - len(txt_descricao.get("1.0", "end-1c"))
        lbl_contador.config(text=f"{restante} restantes")
    txt_descricao.bind("<KeyRelease>", atualizar_contador)

    tk.Label(frame_form, text="Data de Produção:").grid(row=8, column=0, sticky="e")
    cal_data_prod = DateEntry(frame_form, date_pattern="dd/MM/yyyy")
    cal_data_prod.grid(row=8, column=1, sticky="w")
    tk.Label(frame_form, text="Hora (HH:MM):").grid(row=8, column=1, sticky="e")
    entry_hora_prod = tk.Entry(frame_form, width=8)
    entry_hora_prod.grid(row=8, column=1, sticky="e", padx=(90,0))

    tk.Label(frame_form, text="Ação Imediata:").grid(row=9, column=0, sticky="e")
    entry_acao = tk.Entry(frame_form, width=40)
    entry_acao.grid(row=9, column=1)

    tk.Label(frame_form, text="Responsável pela Ação:").grid(row=10, column=0, sticky="e")
    entry_resp = tk.Entry(frame_form, width=40)
    entry_resp.grid(row=10, column=1)

    btn_salvar = tk.Button(frame_form, text="Salvar", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=salvar)
    btn_salvar.grid(row=11, column=1, pady=10)

def salvar_ncs():
    with open(ARQUIVO_NCS, "w", encoding="utf-8") as f:
        json.dump(ncs, f, ensure_ascii=False, indent=2)

def carregar_ncs():
    if os.path.exists(ARQUIVO_NCS):
        with open(ARQUIVO_NCS, "r", encoding="utf-8") as f:
            ncs.clear()
            ncs.extend(json.load(f))

def excluir_nc():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma NC para excluir.")
        return
    idx = tree.index(selecionado[0])
    resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir esta NC?")
    if resposta:
        del ncs[idx]
        atualizar_lista()
        salvar_ncs()
        messagebox.showinfo("Sucesso", "NC excluída com sucesso!")

def editar_nc():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma NC para editar.")
        return
    idx = tree.index(selecionado[0])
    nc = ncs[idx]

    def atualizar_codigo_produto(event=None):
        produto = cb_produto.get()
        codigo = PRODUTO_CODIGO.get(produto, "")
        entry_codigo.config(state="normal")
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)
        entry_codigo.config(state="readonly")

    def salvar_edicao():
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
        nc["data_ocorrencia"] = cal_data.get()
        nc["produto"] = cb_produto.get()
        nc["codigo_produto"] = entry_codigo.get()
        nc["total_reprovado"] = int(entry_total.get())
        nc["unidade"] = cb_unidade.get()
        nc["defeito"] = cb_defeito.get()
        nc["descricao"] = descricao
        nc["data_producao"] = cal_data_prod.get() + " - " + entry_hora_prod.get()
        nc["acao_imediata"] = entry_acao.get()
        nc["responsavel_acao"] = entry_resp.get()
        atualizar_lista()
        salvar_ncs()
        top.destroy()
        messagebox.showinfo("Sucesso", "NC editada com sucesso!")

    top = tk.Toplevel(janela)
    top.title("Editar NC")
    top.grab_set()
    top.resizable(False, False)

    frame_form = tk.Frame(top, padx=10, pady=10)
    frame_form.pack()

    tk.Label(frame_form, text="Data da Ocorrência:").grid(row=0, column=0, sticky="e")
    cal_data = DateEntry(frame_form, date_pattern="dd/MM/yyyy")
    cal_data.set_date(datetime.datetime.strptime(nc["data_ocorrencia"], "%d/%m/%Y"))
    cal_data.grid(row=0, column=1)

    tk.Label(frame_form, text="Produto:").grid(row=1, column=0, sticky="e")
    cb_produto = ttk.Combobox(frame_form, values=PRODUTOS, state="readonly")
    cb_produto.set(nc["produto"])
    cb_produto.grid(row=1, column=1)
    cb_produto.bind("<<ComboboxSelected>>", atualizar_codigo_produto)

    tk.Label(frame_form, text="Código do Produto:").grid(row=2, column=0, sticky="e")
    entry_codigo = tk.Entry(frame_form, state="readonly")
    entry_codigo.grid(row=2, column=1)
    entry_codigo.config(state="normal")
    entry_codigo.delete(0, tk.END)
    entry_codigo.insert(0, nc["codigo_produto"])
    entry_codigo.config(state="readonly")

    tk.Label(frame_form, text="Total Reprovado:").grid(row=3, column=0, sticky="e")
    entry_total = tk.Entry(frame_form)
    entry_total.insert(0, str(nc["total_reprovado"]))
    entry_total.grid(row=3, column=1)

    tk.Label(frame_form, text="Unidade de Medida:").grid(row=4, column=0, sticky="e")
    cb_unidade = ttk.Combobox(frame_form, values=UNIDADES, state="readonly")
    cb_unidade.set(nc["unidade"])
    cb_unidade.grid(row=4, column=1)

    tk.Label(frame_form, text="Defeito:").grid(row=5, column=0, sticky="e")
    defeitos_maiusculo = [d.upper() for d in DEFEITOS]
    cb_defeito = ttk.Combobox(frame_form, values=defeitos_maiusculo, state="readonly")
    cb_defeito.set(nc["defeito"].upper())
    cb_defeito.grid(row=5, column=1)

    tk.Label(frame_form, text="Descrição (máx 400):").grid(row=6, column=0, sticky="ne")
    txt_descricao = tk.Text(frame_form, width=40, height=4)
    txt_descricao.insert("1.0", nc["descricao"])
    txt_descricao.grid(row=6, column=1)
    lbl_contador = tk.Label(frame_form, text=f"{400 - len(nc['descricao'])} restantes")
    lbl_contador.grid(row=7, column=1, sticky="w")

    def atualizar_contador(event=None):
        restante = 400 - len(txt_descricao.get("1.0", "end-1c"))
        lbl_contador.config(text=f"{restante} restantes")
    txt_descricao.bind("<KeyRelease>", atualizar_contador)

    tk.Label(frame_form, text="Data de Produção:").grid(row=8, column=0, sticky="e")
    cal_data_prod = DateEntry(frame_form, date_pattern="dd/MM/yyyy")
    data_prod = nc["data_producao"].split(" - ")[0]
    cal_data_prod.set_date(datetime.datetime.strptime(data_prod, "%d/%m/%Y"))
    cal_data_prod.grid(row=8, column=1, sticky="w")
    tk.Label(frame_form, text="Hora (HH:MM):").grid(row=8, column=1, sticky="e")
    entry_hora_prod = tk.Entry(frame_form, width=8)
    hora_prod = nc["data_producao"].split(" - ")[1] if " - " in nc["data_producao"] else ""
    entry_hora_prod.insert(0, hora_prod)
    entry_hora_prod.grid(row=8, column=1, sticky="e", padx=(90,0))

    tk.Label(frame_form, text="Ação Imediata:").grid(row=9, column=0, sticky="e")
    entry_acao = tk.Entry(frame_form, width=40)
    entry_acao.insert(0, nc["acao_imediata"])
    entry_acao.grid(row=9, column=1)

    tk.Label(frame_form, text="Responsável pela Ação:").grid(row=10, column=0, sticky="e")
    entry_resp = tk.Entry(frame_form, width=40)
    entry_resp.insert(0, nc["responsavel_acao"])
    entry_resp.grid(row=10, column=1)

    btn_salvar = tk.Button(frame_form, text="Salvar", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=salvar_edicao)
    btn_salvar.grid(row=11, column=1, pady=10)

# Interface Tkinter
janela = tk.Tk()
janela.title("Gerenciador de Não Conformidades")
janela.geometry("1350x650")
janela.configure(bg="#f0f0f0")

# Título
lbl_titulo = tk.Label(janela, text="GERENCIAMENTO DE NÃO CONFORMIDADES", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#003366")
lbl_titulo.pack(pady=10)

# Frame para tabela
frame_tabela = tk.LabelFrame(janela, text="Registros", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 13, "bold"), fg="#003366")
frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

criar_treeview(frame_tabela)

# Frame para botões
frame_botoes = tk.Frame(janela, bg="#f0f0f0")
frame_botoes.pack(pady=10)

btn_novo = tk.Button(frame_botoes, text="CRIAR NOVA NÃO CONFORMIDADE", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=28, command=cadastrar_nc)
btn_novo.grid(row=0, column=0, padx=10, pady=5)

btn_editar = tk.Button(frame_botoes, text="EDITAR NÃO CONFORMIDADE", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", width=28, command=editar_nc)
btn_editar.grid(row=0, column=1, padx=10, pady=5)

btn_excluir = tk.Button(frame_botoes, text="EXCLUIR NÃO CONFORMIDADE", font=("Arial", 11, "bold"), bg="#F44336", fg="white", width=28, command=excluir_nc)
btn_excluir.grid(row=0, column=2, padx=10, pady=5)

btn_sair = tk.Button(frame_botoes, text="SAIR DO PROGRAMA", font=("Arial", 11, "bold"), bg="#757575", fg="white", width=28, command=janela.quit)
btn_sair.grid(row=0, column=3, padx=10, pady=5)

# 10 registros de exemplo para teste
ncs = [
    {
        "numero_registro": f"2025-000{i+1}",
        "data_ocorrencia": f"0{i+1}/06/2025",
        "codigo_produto": CODIGOS_PRODUTO[i % len(CODIGOS_PRODUTO)],
        "produto": PRODUTOS[i % len(PRODUTOS)],
        "total_reprovado": 10 + i,
        "unidade": UNIDADES[i % len(UNIDADES)],
        "defeito": DEFEITOS[i % len(DEFEITOS)],
        "descricao": f"Descrição de teste {i+1}",
        "data_producao": f"0{i+1}/06/2025 - 08:0{i}",
        "acao_imediata": f"Ação {i+1}",
        "responsavel_acao": f"Responsável {i+1}",
        "status": "Aberta" if i % 2 == 0 else "Fechada"
    } for i in range(10)
]

salvar_ncs()
carregar_ncs()
atualizar_lista()
janela.mainloop()
