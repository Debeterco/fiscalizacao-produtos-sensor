import streamlit as st
import sqlite3
import hashlib
import random
import time

# --- Banco de dados SQLite ---

conn = sqlite3.connect("usuarios.db", check_same_thread=False)
c = conn.cursor()

def criar_tabela():
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

def adicionar_usuario(username, password):
    try:
        c.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verificar_usuario(username, password):
    c.execute('SELECT password FROM usuarios WHERE username = ?', (username,))
    resultado = c.fetchone()
    if resultado:
        senha_hash = resultado[0]
        return senha_hash == password
    return False

# --- Função para hashear senha ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Classe Produto e simulação ---

class Produto:
    def __init__(self, nome):
        self.nome = nome
        self.sensor_ativo = random.choice([True, False])
        self.pago = random.choice([True, False])
        self.furtado = False

    def verificar_sensor(self):
        if not self.pago:
            return f"🔴 ALARME! Produto '{self.nome}' NÃO está pago! FURTO DETECTADO! Sensor APITOU!"
        else:
            if self.sensor_ativo:
                return f"🟢 Produto '{self.nome}' está pago e com sensor ativo. Fiscalização OK."
            else:
                return f"🟠 Produto '{self.nome}' está pago, mas o sensor está DESATIVADO. Atenção!"

    def tentar_furto(self):
        if self.pago:
            return False
        if not self.sensor_ativo:
            chance_furto_oculto = 0.3
            if random.random() < chance_furto_oculto:
                self.furtado = True
                return True
        return False

def simular_fiscalizacao(produtos):
    st.write("### Iniciando fiscalização dos produtos...\n")
    furtos_detectados = 0
    furtos_ocultos = 0

    for produto in produtos:
        st.write(f"🔍 Verificando produto: **{produto.nome}**...")
        time.sleep(1.5)

        resultado = produto.verificar_sensor()
        st.write(resultado)

        furtou = produto.tentar_furto()
        if furtou:
            st.error(f"⚠️ ALERTA DE FURTO OCULTO! O produto '{produto.nome}' foi furtado sem ser detectado pelo sensor!")
            furtos_ocultos += 1
        else:
            if not produto.pago:
                furtos_detectados += 1
                st.warning("Produto não pago já detectado como furto!")
            else:
                st.success("Nenhum furto detectado neste produto.")

        st.write("---")
        time.sleep(1)

    st.write("## Fiscalização concluída.")
    st.write(f"**Furtos detectados pelo sensor:** {furtos_detectados}")
    st.write(f"**Furtos ocultos (sensor desligado):** {furtos_ocultos}")

# --- Tela de cadastro ---

def cadastro():
    st.title("📋 Cadastro")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    password_conf = st.text_input("Confirme a senha", type="password")
    if st.button("Cadastrar"):
        if password != password_conf:
            st.error("As senhas não coincidem.")
        elif len(username) < 3:
            st.error("Usuário deve ter ao menos 3 caracteres.")
        elif len(password) < 6:
            st.error("Senha deve ter ao menos 6 caracteres.")
        else:
            senha_hash = hash_password(password)
            sucesso = adicionar_usuario(username, senha_hash)
            if sucesso:
                st.success("Usuário cadastrado com sucesso! Faça login.")
            else:
                st.error("Usuário já existe.")

# --- Tela de login ---

def login():
    st.title("🔐 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        senha_hash = hash_password(password)
        if verificar_usuario(username, senha_hash):
            st.session_state['login'] = True
            st.session_state['usuario'] = username
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")

def logout():
    st.session_state['login'] = False
    st.session_state['usuario'] = None
    st.experimental_rerun()

# --- App principal ---

nomes_produtos = [
    "Camisa Polo",
    "Calça Jeans",
    "Jaqueta",
    "Tênis Casual",
    "Blusa de Frio",
    "Mochila"
]

def main():
    criar_tabela()
    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['usuario'] = None
    menu = ["Login", "Cadastro"]
    if not st.session_state['login']:
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Login":
            login()
        elif choice == "Cadastro":
            cadastro()
    else:
        st.sidebar.write(f"👤 Usuário: {st.session_state['usuario']}")
        if st.sidebar.button("Sair"):
            logout()

        st.title("Simulador Fiscalização de Produto")
        if st.button("Iniciar Simulação de Fiscalização"):
            produtos_loja = [Produto(nome) for nome in nomes_produtos]
            with st.spinner("Fiscalizando produtos..."):
                simular_fiscalizacao(produtos_loja)
        else:
            st.write("Clique no botão acima para iniciar a fiscalização.")

if __name__ == "__main__":
    main()
