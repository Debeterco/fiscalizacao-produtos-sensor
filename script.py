import streamlit as st
import random
import time

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

# Lista de produtos para simular
nomes_produtos = [
    "Camisa Polo",
    "Calça Jeans",
    "Jaqueta",
    "Tênis Casual",
    "Blusa de Frio",
    "Mochila"
]

if st.button("Iniciar Simulação de Fiscalização"):
    produtos_loja = [Produto(nome) for nome in nomes_produtos]
    simular_fiscalizacao(produtos_loja)
else:
    st.write("Clique no botão acima para iniciar a fiscalização.")
