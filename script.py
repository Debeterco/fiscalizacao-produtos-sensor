import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Simulador Antifurto", layout="centered")

# Emoji por produto
icones = {
    "camisa": "👕",
    "calça": "👖",
    "jaqueta": "🧥",
    "tênis": "👟",
    "blusa": "🧣",
    "mochila": "🎒"
}

def icone_produto(nome):
    for chave, emoji in icones.items():
        if chave in nome.lower():
            return emoji
    return "📦"

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

class Produto:
    def __init__(self, nome):
        self.nome = nome
        self.pago = random.choice([True, False])
        self.furtado = False

    def verificar_sensor(self):
        falha_sensor = random.random() < 0.05  # 5% de chance de falha

        if not self.pago:
            if not falha_sensor:
                self.furtado = True
                return f"🔴 ALARME! Produto '{self.nome}' NÃO está pago! Sensor APITOU! FURTO DETECTADO!"
            else:
                self.furtado = True
                return f"🔕 Produto '{self.nome}' NÃO está pago, mas o sensor FALHOU. FURTO NÃO DETECTADO!"
        else:
            return f"🟢 Produto '{self.nome}' está pago. OK."

def simular_fiscalizacao(produtos):
    st.write("### Iniciando fiscalização dos produtos...\n")
    furtos_detectados = 0
    furtos_ocultos = 0
    dados = []
    progress_bar = st.progress(0)

    for i, produto in enumerate(produtos):
        st.write(f"🔍 Verificando: **{icone_produto(produto.nome)} {produto.nome}**")
        time.sleep(1)

        resultado = produto.verificar_sensor()
        st.write(resultado)

        if not produto.pago:
            if produto.furtado:
                if "FALHOU" in resultado:
                    furtos_ocultos += 1
                    st.error(f"🚨 FURTO OCULTO! '{produto.nome}' passou sem ser detectado.")
                else:
                    furtos_detectados += 1
                    st.warning("⚠️ Produto não pago DETECTADO como furto.")
        else:
            st.success("✅ Produto OK, sem problemas.")

        dados.append({
            "Produto": produto.nome,
            "Pago": "Sim" if produto.pago else "Não",
            "Furtado": "Sim" if produto.furtado else "Não"
        })

        st.write("---")
        progress_bar.progress((i + 1) / len(produtos))

    st.write("## ✅ Fiscalização concluída!")
    st.write(f"**Furtos detectados (sensor funcionou):** `{furtos_detectados}`")
    st.write(f"**Furtos ocultos (sensor falhou):** `{furtos_ocultos}`")

    df_resultado = pd.DataFrame(dados)
    st.dataframe(df_resultado)

    st.session_state.historico.append({
        "Total Produtos": len(produtos),
        "Detectados": furtos_detectados,
        "Ocultos": furtos_ocultos
    })

    return df_resultado

# Interface
st.title("🛒 Simulador de Fiscalização Antifurto (com falha de sensor)")

num_produtos = st.slider("Quantidade de produtos a simular:", 1, 10, 6)
nomes = [st.text_input(f"Nome do produto {i+1}", f"Produto {i+1}") for i in range(num_produtos)]

if st.button("▶️ Iniciar Simulação"):
    lista = [Produto(nome) for nome in nomes]
    simular_fiscalizacao(lista)

if st.checkbox("📊 Mostrar histórico de simulações anteriores"):
    st.write(pd.DataFrame(st.session_state.historico))
