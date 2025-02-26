import sqlite3 as sqlite

# Função para criar as tabelas de usuários e horários
def criarTabela():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    # Criar tabela de usuários
    cursor.execute('''	
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    # Criar tabela de horários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

# Função para inserir usuário
def inserirUsuario(nome, login, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, login, senha) VALUES (?, ?, ?)
    ''', (nome, login, senha))
    conn.commit()
    conn.close()

# Função para listar todos os usuários
def listarUsuarios():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
    dados = cursor.fetchall()
    usuarios = []
    for dado in dados:
        usuarios.append(dado)
    conn.close()
    return usuarios

# Função para autenticação de login
def login(login, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha))
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False

# Função para verificar se o usuário já existe
def verificarUsuario(login):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login=?", [login])
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False

# Função para recuperar a senha
def recuperarSenhaBD(nome, login):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE nome=? AND login=?", (nome, login))
    senha = cursor.fetchone()
    conn.close()
    return senha

# Função para inserir horário
def inserirHorario(usuario_id, data_hora):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO horarios (usuario_id, data_hora) VALUES (?, ?)
    ''', (usuario_id, data_hora))
    conn.commit()
    conn.close()

# Função para listar horários
def listarHorarios():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horarios ORDER BY data_hora ASC')
    dados = cursor.fetchall()
    horarios = []
    for dado in dados:
        horarios.append(dado)
    conn.close()
    return horarios

# Função para verificar se o horário já está agendado
def verificarHorario(data_hora):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM horarios WHERE data_hora=?", [data_hora])
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False