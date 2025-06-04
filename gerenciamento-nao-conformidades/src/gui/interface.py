from tkinter import Tk, Frame, Label, Button, Listbox, Scrollbar, Entry, StringVar, messagebox

class Interface:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciamento de Não Conformidades")

        self.frame = Frame(master)
        self.frame.pack()

        self.label = Label(self.frame, text="Lista de Não Conformidades")
        self.label.pack()

        self.listbox = Listbox(self.frame, width=50)
        self.listbox.pack(side="left")

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.button_frame = Frame(master)
        self.button_frame.pack()

        self.view_button = Button(self.button_frame, text="Visualizar", command=self.visualizar)
        self.view_button.pack(side="left")

        self.edit_button = Button(self.button_frame, text="Editar", command=self.editar)
        self.edit_button.pack(side="left")

        self.delete_button = Button(self.button_frame, text="Excluir", command=self.excluir)
        self.delete_button.pack(side="left")

        self.entry_var = StringVar()
        self.entry = Entry(master, textvariable=self.entry_var)
        self.entry.pack()

        self.add_button = Button(master, text="Adicionar Registro", command=self.adicionar)
        self.add_button.pack()

    def visualizar(self):
        selected = self.listbox.curselection()
        if selected:
            messagebox.showinfo("Visualizar", f"Visualizando: {self.listbox.get(selected)}")
        else:
            messagebox.showwarning("Aviso", "Selecione um registro para visualizar.")

    def editar(self):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected)
            self.listbox.insert(selected, self.entry_var.get())
            self.entry_var.set("")
        else:
            messagebox.showwarning("Aviso", "Selecione um registro para editar.")

    def excluir(self):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected)
        else:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir.")

    def adicionar(self):
        registro = self.entry_var.get()
        if registro:
            self.listbox.insert("end", registro)
            self.entry_var.set("")
        else:
            messagebox.showwarning("Aviso", "Digite um registro para adicionar.")

if __name__ == "__main__":
    root = Tk()
    interface = Interface(root)
    root.mainloop()