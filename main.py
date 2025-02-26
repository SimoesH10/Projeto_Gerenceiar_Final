from flask import Flask, render_template, request
import gestaoDB

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/paginaCadastro")
def paginaCadastro():
    return render_template("cadastro.html")

@app.route("/paginaLogin")
def paginaLogin():
    return render_template("login.html")

@app.route("/paginaAgendamento")
def paginaAgendamento():
    return render_template("agendamento.html")

@app.route("/paginaGerenciarHorarios")
def paginaGerenciarHorarios():
    return render_template("gerenciar_horarios.html")

@app.route("/visualizarAgendamentos")
def paginavisualizarAgendamento():
    return render_template("visualizarAgendamentos.html")

@app.route("/paginaRecuperarSenha")
def paginaRecuperarSenha():
    return render_template("recuperacao.html")

# Criar banco de dados e tabelas
gestaoDB.criarTabela()

# Página principal (home)
@app.route("/")
def principal():
    return render_template("home.html")


# Rota para cadastrar um novo usuário
@app.route("/cadastrarUsuario", methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nomeUsuario')
    login = request.form.get('loginUsuario')
    senha = str(request.form.get('senhaUsuario'))
    if gestaoDB.verificarUsuario(login) == False:
        gestaoDB.inserirUsuario(nome, login, senha)
        mensagem = "Usuário cadastrado com sucesso!"
        return render_template("home.html", mensagem=mensagem)
    else:
        mensagem = "Usuário já existe."
        return render_template("home.html", mensagem=mensagem)

# Rota para login
@app.route("/autenticarUsuario", methods=['POST'])
def autenticar():
    login = request.form.get("loginUsuario")
    senha = str(request.form.get("senhaUsuario"))
    
    logado = gestaoDB.login(login, senha)

    if logado:
        return render_template("logado.html")
    else:    
        mensagem = "Usuário ou senha incorretos."
        return render_template("home.html", mensagem=mensagem)

# Rota para agendar horário
@app.route("/agendarHorario", methods=['POST'])
def agendarHorario():
    usuario_id = request.form.get("usuario_id")
    data_hora = request.form.get("data_hora")

    if gestaoDB.verificarHorario(data_hora):
        mensagem = "Horário já agendado."
    else:
        gestaoDB.inserirHorario(usuario_id, data_hora)
        mensagem = "Horário agendado com sucesso!"
        return render_template("logado.html", mensagem=mensagem)


# Página de gerenciamento de horários
@app.route("/gerenciarHorarios")
def gerenciarHorarios():
    horarios = gestaoDB.listarHorarios()
    return render_template("gerenciar_horarios.html", horarios=horarios)

# Página de recuperação de senha
@app.route("/recuperarSenha", methods=['POST'])
def recuperarSenha():
    nome = request.form.get("nomeUsuario")
    login = request.form.get("loginUsuario")
   
    encontrado = False
    senha = "vazio"

    if gestaoDB.verificarUsuario(login):
        encontrado = True

    if encontrado:
        senha = str(gestaoDB.recuperarSenhaBD(nome, login))
        mensagem = f"Sua senha: {senha}"
        return render_template("recuperacao.html", mensagem=mensagem)
    else:    
        mensagem = "Usuário não encontrado."
        return render_template("recuperacao.html", mensagem=mensagem)


app.run(debug=True)
