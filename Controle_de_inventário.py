import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

USERS_FILE = 'users.json'
INVENTORY_FILE = 'inventory.json'

FONT = ("Arial", 10)
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#4CAF50"
BTN_TEXT_COLOR = "#ffffff"

def load_json(filepath):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump({}, f)
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def garantir_admin():
    users = load_json(USERS_FILE)
    if "admin" not in users:
        users["admin"] = {
            "senha": "admin",
            "data_registro": datetime.now().strftime("%d/%m/%Y"),
            "admin": True,
            "aprovado": True
        }
    else:
        users["admin"]["admin"] = True
        users["admin"]["aprovado"] = True
    save_json(USERS_FILE, users)

garantir_admin()

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def create_button(master, text, command):
    btn = tk.Button(master, text=text, command=command, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT)
    btn.pack(pady=5, fill='x', padx=10)
    return btn

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f'{width}x{height}+{x}+{y}')

def verificar_admin(usuario):
    users = load_json(USERS_FILE)
    return users.get(usuario, {}).get("admin", False)

def ver_estoque(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    inventory = load_json(INVENTORY_FILE)
    tk.Label(frame, text="Estoque Atual:", bg=BG_COLOR, font=FONT).pack(pady=5)
    text_area = tk.Text(frame, font=FONT, bg='white', wrap='word', height=15)
    text_area.pack(fill='both', expand=True)
    texto = "\n".join([f"{item} - {dados['quantidade']}" for item, dados in inventory.items()]) or "Estoque vazio."
    text_area.insert('1.0', texto)
    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def ver_historico(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    inventory = load_json(INVENTORY_FILE)
    tk.Label(frame, text="Histórico:", bg=BG_COLOR, font=FONT).pack(pady=5)
    text_area = tk.Text(frame, font=FONT, bg='white', wrap='word', height=15)
    text_area.pack(fill='both', expand=True)
    texto = ""
    for item, dados in inventory.items():
        texto += f"\nItem: {item}\n"
        for h in dados.get("historico", []):
            texto += f"  - {h['data']} | {h['usuario']} | {h['acao']} | {h['quantidade']}\n"
    text_area.insert('1.0', texto or "Nenhum histórico disponível.")
    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def ver_registros(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    if not verificar_admin(usuario):
        messagebox.showerror("Erro", "Acesso restrito a administradores.")
        interface_principal(usuario, frame.master)
        return
    users = load_json(USERS_FILE)
    tk.Label(frame, text="Usuários Registrados:", bg=BG_COLOR, font=FONT).pack(pady=5)
    text_area = tk.Text(frame, font=FONT, bg='white', wrap='word', height=15)
    text_area.pack(fill='both', expand=True)
    texto = "\n".join([f"Usuário: {u}, Aprovado: {d.get('aprovado', False)}, Registro: {d['data_registro']}" for u, d in users.items()])
    text_area.insert('1.0', texto or "Nenhum registro disponível.")
    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def acompanhar_solicitacoes(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    if not verificar_admin(usuario):
        messagebox.showerror("Erro", "Acesso restrito a administradores.")
        interface_principal(usuario, frame.master)
        return
    users = load_json(USERS_FILE)
    pendentes = {u: d for u, d in users.items() if not d.get("aprovado", False) and u != "admin"}
    tk.Label(frame, text="Solicitações Pendentes:", bg=BG_COLOR, font=FONT).pack(pady=5)
    if not pendentes:
        tk.Label(frame, text="Nenhuma solicitação pendente.", bg=BG_COLOR, font=FONT).pack()
    for usuario_pendente in pendentes:
        def aprovar(u=usuario_pendente):
            users[u]["aprovado"] = True
            save_json(USERS_FILE, users)
            messagebox.showinfo("Aprovado", f"Usuário '{u}' foi aprovado.")
            acompanhar_solicitacoes(frame, usuario)
        tk.Button(frame, text=f"Aprovar {usuario_pendente}", command=aprovar, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT).pack(pady=2, fill='x')
    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def retirar_item(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    inventory = load_json(INVENTORY_FILE)
    if not inventory:
        tk.Label(frame, text="Estoque vazio.", bg=BG_COLOR, font=FONT).pack()
        create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))
        return
    tk.Label(frame, text="Selecione o item:", bg=BG_COLOR, font=FONT).pack(pady=5)
    selected_item = tk.StringVar()
    quantidade_var = tk.StringVar()

    def selecionar(item):
        selected_item.set(item)
        quantidade_entry.config(state='normal')
        confirmar_btn.config(state='normal')

    for item in inventory:
        tk.Button(frame, text=f"{item} - {inventory[item]['quantidade']}", 
                  bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT, 
                  command=lambda i=item: selecionar(i)).pack(fill='x', pady=2)

    quantidade_entry = tk.Entry(frame, textvariable=quantidade_var, font=FONT, state='disabled')
    quantidade_entry.pack(pady=5)

    tk.Label(frame, text="Data:", bg=BG_COLOR, font=FONT).pack(pady=5)
    dia = ttk.Spinbox(frame, from_=1, to=31, width=3, font=FONT)
    dia.pack(side='left', padx=(10, 2))
    mes = ttk.Spinbox(frame, from_=1, to=12, width=3, font=FONT)
    mes.pack(side='left', padx=2)
    ano = ttk.Spinbox(frame, from_=2020, to=2100, width=5, font=FONT)
    ano.pack(side='left', padx=2)

    def confirmar():
        nome = selected_item.get()
        if not nome:
            messagebox.showerror("Erro", "Nenhum item selecionado.")
            return
        try:
            quantidade = int(quantidade_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return
        if quantidade <= 0 or quantidade > inventory[nome]['quantidade']:
            messagebox.showerror("Erro", "Quantidade inválida ou insuficiente.")
            return
        data = f"{int(dia.get()):02}/{int(mes.get()):02}/{ano.get()}"
        if not validar_data(data):
            messagebox.showerror("Erro", "Formato de data inválido.")
            return
        inventory[nome]['quantidade'] -= quantidade
        inventory[nome]['historico'].append({
            "acao": "retirada",
            "quantidade": quantidade,
            "usuario": usuario,
            "data": data
        })
        save_json(INVENTORY_FILE, inventory)
        messagebox.showinfo("Sucesso", "Item retirado.")
        retirar_item(frame, usuario)

    confirmar_btn = tk.Button(frame, text="Confirmar", command=confirmar, bg=BTN_COLOR,
                              fg=BTN_TEXT_COLOR, font=FONT, state='disabled')
    confirmar_btn.pack(pady=10)

    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def adicionar_item(frame, usuario):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="Adicionar Item:", bg=BG_COLOR, font=FONT).pack(pady=5)
    nome_var = tk.StringVar()
    qtd_var = tk.StringVar()
    tk.Entry(frame, textvariable=nome_var, font=FONT).pack(pady=5)
    tk.Entry(frame, textvariable=qtd_var, font=FONT).pack(pady=5)

    def adicionar():
        nome = nome_var.get()
        try:
            qtd = int(qtd_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return
        inventory = load_json(INVENTORY_FILE)
        if nome in inventory:
            inventory[nome]['quantidade'] += qtd
        else:
            inventory[nome] = {'quantidade': qtd, 'historico': []}
        save_json(INVENTORY_FILE, inventory)
        messagebox.showinfo("Sucesso", "Item adicionado.")

    create_button(frame, "Adicionar", adicionar)
    create_button(frame, "Voltar", lambda: interface_principal(usuario, frame.master))

def interface_principal(usuario, root=None):
    if root:
        root.destroy()
    root = tk.Tk()
    root.title(f"Bem-vindo, {usuario}")
    center_window(root, 240, 400)
    root.configure(bg=BG_COLOR)
    tk.Label(root, text="Menu Principal", bg=BG_COLOR, font=("Arial", 12, "bold")).pack(pady=10)
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(fill='both', expand=True)
    create_button(root, "Ver Estoque", lambda: ver_estoque(frame, usuario))
    create_button(root, "Ver Histórico", lambda: ver_historico(frame, usuario))
    create_button(root, "Ver Registros", lambda: ver_registros(frame, usuario))
    create_button(root, "Aprovar Usuários", lambda: acompanhar_solicitacoes(frame, usuario))
    create_button(root, "Retirar Item", lambda: retirar_item(frame, usuario))
    create_button(root, "Adicionar Item", lambda: adicionar_item(frame, usuario))
    create_button(root, "Sair", root.destroy)
    root.mainloop()

def registrar_usuario(janela):
    for widget in janela.winfo_children():
        widget.destroy()
    tk.Label(janela, text="Registrar Usuário", bg=BG_COLOR, font=FONT).pack(pady=5)
    usuario_var = tk.StringVar()
    senha_var = tk.StringVar()
    tk.Entry(janela, textvariable=usuario_var, font=FONT).pack(pady=5)
    tk.Entry(janela, textvariable=senha_var, show='*', font=FONT).pack(pady=5)
    def registrar():
        usuarios = load_json(USERS_FILE)
        usuario = usuario_var.get()
        if usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
            return
        usuarios[usuario] = {
            "senha": senha_var.get(),
            "data_registro": datetime.now().strftime("%d/%m/%Y"),
            "admin": False,
            "aprovado": False
        }
        save_json(USERS_FILE, usuarios)
        messagebox.showinfo("Sucesso", "Usuário registrado. Aguarde aprovação.")
        login()
        janela.destroy()
    create_button(janela, "Registrar", registrar)
    create_button(janela, "Voltar", lambda: (janela.destroy(), login()))

def autenticar_usuario(janela):
    for widget in janela.winfo_children():
        widget.destroy()
    tk.Label(janela, text="Login", bg=BG_COLOR, font=FONT).pack(pady=5)
    usuario_var = tk.StringVar()
    senha_var = tk.StringVar()
    tk.Entry(janela, textvariable=usuario_var, font=FONT).pack(pady=5)
    tk.Entry(janela, textvariable=senha_var, show='*', font=FONT).pack(pady=5)
    def autenticar():
        usuarios = load_json(USERS_FILE)
        usuario = usuario_var.get()
        senha = senha_var.get()
        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            if not usuarios[usuario].get("aprovado", False):
                messagebox.showwarning("Aguardando aprovação", "Seu cadastro ainda não foi aprovado por um administrador.")
                return
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy()
            interface_principal(usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    create_button(janela, "Entrar", autenticar)
    create_button(janela, "Voltar", lambda: (janela.destroy(), login()))

def login():
    janela = tk.Tk()
    janela.title("Controle de Estoque")
    center_window(janela, 240, 360)
    janela.configure(bg=BG_COLOR)
    create_button(janela, "Entrar", lambda: autenticar_usuario(janela))
    create_button(janela, "Registrar", lambda: registrar_usuario(janela))
    create_button(janela, "Fechar", janela.destroy)
    janela.mainloop()

if __name__ == "__main__":
    login()
