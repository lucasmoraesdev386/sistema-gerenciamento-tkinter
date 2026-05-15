import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Conexão com o banco de dados
def conectar_db():
    conn = sqlite3.connect('clientes.db')
    return conn

# Criar tabela
def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            data_cadastro TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Adicionar cliente
def adicionar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    
    if not nome:
        messagebox.showwarning("Atenção", "O nome é obrigatório!")
        return
    
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, data_cadastro)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, data_atual))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        limpar_campos()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

# Limpar campos
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

# Atualizar Treeview
def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

# Interface Gráfica
root = tk.Tk()
root.title("Sistema de Gerenciamento - Lucas Moraes")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(root, text="Sistema de Gerenciamento de Clientes", 
                  font=("Arial", 18, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

# Frame dos campos
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Nome:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome = tk.Entry(frame, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Email:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_email = tk.Entry(frame, width=40)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Telefone:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_telefone = tk.Entry(frame, width=40)
entry_telefone.grid(row=2, column=1, padx=5, pady=5)

# Botões
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Cadastrar Cliente", command=adicionar_cliente, 
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=20).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos, 
          bg="#2196F3", fg="white", font=("Arial", 10), width=15).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Atualizar Lista", command=atualizar_tabela, 
          bg="#FFC107", fg="black", font=("Arial", 10), width=15).grid(row=0, column=2, padx=10)

# Tabela
tree = ttk.Treeview(root, columns=("ID", "Nome", "Email", "Telefone", "Data"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Telefone", text="Telefone")
tree.heading("Data", text="Data de Cadastro")

tree.column("ID", width=50)
tree.column("Nome", width=200)
tree.column("Email", width=200)
tree.column("Telefone", width=120)
tree.column("Data", width=150)

tree.pack(pady=20, padx=20, fill="both", expand=True)

# Inicializar
criar_tabela()
atualizar_tabela()

root.mainloop()