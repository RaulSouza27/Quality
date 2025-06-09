import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import json
import os

ncs = []
proximo_id = 1
ARQUIVO_NCS = "ncs.json"

# Funções principais
def atualizar_lista():
    lista_ncs.delete(0, tk.END)
    for nc in ncs:
        texto = f"ID {nc['id']} | {nc['titulo']} | {nc['status']}"
        lista_ncs.insert(tk.END, texto)

def cadastrar_nc():
    global proximo_id
    titulo = simpledialog.askstring("Título", "Informe o título da NC:")
    descricao = simpledialog.askstring("Descrição", "Informe a descrição:")
    responsavel = simpledialog.askstring("Responsável", "Informe o responsável:")

    if not titulo or not descricao or not responsavel:
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
        return

    data = datetime.date.today().strftime("%d/%m/%Y")
    nc = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "data": data,
        "responsavel": responsavel,
        "status": "Aberta"
    }
    ncs.append(nc)
    proximo_id += 1
    atualizar_lista()
    salvar_ncs()
    messagebox.showinfo("Sucesso", "NC cadastrada com sucesso!")

def visualizar_detalhes():
    try:
        idx = lista_ncs.curselection()[0]
        nc = ncs[idx]
        texto = f"ID: {nc['id']}\nTítulo: {nc['titulo']}\nDescrição: {nc['descricao']}\nData: {nc['data']}\nResponsável: {nc['responsavel']}\nStatus: {nc['status']}"
        messagebox.showinfo("Detalhes da NC", texto)
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma NC da lista.")

def editar_nc():
    try:
        idx = lista_ncs.curselection()[0]
        nc = ncs[idx]
        novo_titulo = simpledialog.askstring("Editar Título", "Novo título:", initialvalue=nc['titulo']) or nc['titulo']
        nova_desc = simpledialog.askstring("Editar Descrição", "Nova descrição:", initialvalue=nc['descricao']) or nc['descricao']
        novo_resp = simpledialog.askstring("Editar Responsável", "Novo responsável:", initialvalue=nc['responsavel']) or nc['responsavel']
        novo_status = simpledialog.askstring("Editar Status", "Novo status:", initialvalue=nc['status']) or nc['status']

        nc['titulo'] = novo_titulo
        nc['descricao'] = nova_desc
        nc['responsavel'] = novo_resp
        nc['status'] = novo_status

        atualizar_lista()
        salvar_ncs()
        messagebox.showinfo("Sucesso", "NC atualizada com sucesso!")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma NC da lista.")

def excluir_nc():
    try:
        idx = lista_ncs.curselection()[0]
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir esta NC?"):
            del ncs[idx]
            atualizar_lista()
            salvar_ncs()
            messagebox.showinfo("Excluído", "NC removida com sucesso.")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma NC da lista.")

def salvar_ncs():
    with open(ARQUIVO_NCS, "w", encoding="utf-8") as f:
        json.dump(ncs, f, ensure_ascii=False, indent=2)

def carregar_ncs():
    global ncs, proximo_id
    if os.path.exists(ARQUIVO_NCS):
        with open(ARQUIVO_NCS, "r", encoding="utf-8") as f:
            ncs.extend(json.load(f))
        if ncs:
            proximo_id = max(nc["id"] for nc in ncs) + 1

# Interface Tkinter
janela = tk.Tk()
janela.title("Gerenciador de Não Conformidades")
janela.geometry("600x400")

frame = tk.Frame(janela)
frame.pack(pady=10)

lista_ncs = tk.Listbox(frame, width=80, height=15)
lista_ncs.pack()

btn_frame = tk.Frame(janela)
btn_frame.pack(pady=10)

btn_cadastrar = tk.Button(btn_frame, text="Cadastrar NC", command=cadastrar_nc)
btn_cadastrar.grid(row=0, column=0, padx=5)

btn_ver = tk.Button(btn_frame, text="Visualizar Detalhes", command=visualizar_detalhes)
btn_ver.grid(row=0, column=1, padx=5)

btn_editar = tk.Button(btn_frame, text="Editar NC", command=editar_nc)
btn_editar.grid(row=0, column=2, padx=5)

btn_excluir = tk.Button(btn_frame, text="Excluir NC", command=excluir_nc)
btn_excluir.grid(row=0, column=3, padx=5)

btn_sair = tk.Button(btn_frame, text="Sair", command=janela.quit)
btn_sair.grid(row=0, column=4, padx=5)

carregar_ncs()
atualizar_lista()
janela.mainloop()
