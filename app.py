import streamlit as st
import pandas as pd


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="BioCompiler 1.0",
    page_icon="🧬",
    layout="wide"
)


# ============================================================
# FUNÇÃO PARA PROCESSAR UMA ENTRADA
# ============================================================

def processar_entrada(dna):
    """
    Processamento provisório.

    Atualmente verifica apenas se as bases são válidas.
    A lógica completa será conectada ao biocompiler.py
    quando a Pessoa A finalizar o processamento.
    """

    bases_validas = {"A", "T", "C", "G"}

    for base in dna:
        if base not in bases_validas:
            return "BUG - base inválida"

    return "CORRETO"


# ============================================================
# FUNÇÃO PARA PROCESSAR TODAS AS ENTRADAS
# ============================================================

def processar_entradas(entradas):
    resultados = []

    for numero, dna in enumerate(entradas, start=1):

        resposta = processar_entrada(dna)

        resultados.append({
            "Entrada": numero,
            "DNA": dna,
            "Resposta": resposta
        })

    return resultados


# ============================================================
# FUNÇÃO PARA GERAR O RELATÓRIO DIAGNÓSTICO
# ============================================================

def gerar_diagnostico(resultados):

    diagnosticos = {
        "CORRETO": 0,
        "BUG - base inválida": 0,
        "BUG - START ausente": 0,
        "BUG - STOP ausente": 0,
        "BUG - frameshift": 0,
        "BUG - nonsense / STOP prematuro": 0
    }

    for resultado in resultados:

        resposta = resultado["Resposta"]

        if resposta in diagnosticos:
            diagnosticos[resposta] += 1

    return diagnosticos


# ============================================================
# FUNÇÃO PARA GERAR O ARQUIVO DE EXPORTAÇÃO
# ============================================================

def gerar_arquivo_exportacao(resultados):

    linhas = []

    for resultado in resultados:

        numero = resultado["Entrada"]
        resposta = resultado["Resposta"]

        linhas.append(
            f"Entrada {numero}: {resposta}"
        )

    return "\n".join(linhas)


# ============================================================
# CABEÇALHO
# ============================================================

st.title("🧬 BioCompiler 1.0")
st.subheader("DNA Transcriber")

st.write(
    "Sistema para validação e transcrição de sequências de DNA."
)

st.divider()


# ============================================================
# CARREGAMENTO DAS ENTRADAS
# ============================================================

arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

try:

    tabela = pd.read_csv(arquivo)

    entradas = tabela["entrada"].tolist()

except Exception as erro:

    st.error(
        f"Não foi possível carregar o arquivo de entradas: {erro}"
    )

    entradas = []


# ============================================================
# INFORMAÇÕES
# ============================================================

st.header("📂 Entradas")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Entradas carregadas",
        len(entradas)
    )

with col2:

    st.metric(
        "Entradas esperadas",
        60
    )


st.divider()


# ============================================================
# BOTÃO INICIAR
# ============================================================

st.header("▶ Execução")

if st.button(
    "▶ Iniciar execução",
    type="primary",
    use_container_width=True
):

    if len(entradas) == 0:

        st.error(
            "Nenhuma entrada foi encontrada."
        )

    else:

        st.info(
            f"Processando {len(entradas)} entradas..."
        )

        # Barra de progresso
        barra = st.progress(0)

        resultados = []

        # Processamento
        for numero, dna in enumerate(
            entradas,
            start=1
        ):

            resposta = processar_entrada(dna)

            resultados.append({
                "Entrada": numero,
                "DNA": dna,
                "Resposta": resposta
            })

            barra.progress(
                numero / len(entradas)
            )


        st.success(
            "Execução concluída!"
        )


        # ====================================================
        # RESULTADOS
        # ====================================================

        st.divider()

        st.header("📋 Resultados da execução")

        df_resultados = pd.DataFrame(
            resultados
        )

        st.dataframe(
            df_resultados,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # RELATÓRIO DIAGNÓSTICO
        # ====================================================

        st.divider()

        st.header("📊 Relatório diagnóstico")

        diagnostico = gerar_diagnostico(
            resultados
        )


        # Métricas principais
        col1, col2, col3 = st.columns(3)

        total = len(resultados)

        corretos = diagnostico[
            "CORRETO"
        ]

        bugs = total - corretos


        with col1:

            st.metric(
                "Total",
                total
            )


        with col2:

            st.metric(
                "CORRETOS",
                corretos
            )


        with col3:

            st.metric(
                "BUGS",
                bugs
            )


        # Tabela do diagnóstico

        dados_diagnostico = {

            "Caso": [
                "1 — Entrada correta",
                "2 — Base inválida",
                "3 — START ausente",
                "4 — STOP ausente",
                "5 — Frameshift",
                "6 — Nonsense"
            ],

            "Resposta": [
                "CORRETO",
                "BUG - base inválida",
                "BUG - START ausente",
                "BUG - STOP ausente",
                "BUG - frameshift",
                "BUG - nonsense / STOP prematuro"
            ],

            "Quantidade": [
                diagnostico[
                    "CORRETO"
                ],

                diagnostico[
                    "BUG - base inválida"
                ],

                diagnostico[
                    "BUG - START ausente"
                ],

                diagnostico[
                    "BUG - STOP ausente"
                ],

                diagnostico[
                    "BUG - frameshift"
                ],

                diagnostico[
                    "BUG - nonsense / STOP prematuro"
                ]
            ]
        }


        df_diagnostico = pd.DataFrame(
            dados_diagnostico
        )


        st.dataframe(
            df_diagnostico,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # EXPORTAÇÃO
        # ====================================================

        st.divider()

        st.header("📥 Exportação")

        arquivo_resultados = (
            gerar_arquivo_exportacao(
                resultados
            )
        )


        st.download_button(
            label="📥 Exportar resultados",
            data=arquivo_resultados,
            file_name="resultados_biocompiler.txt",
            mime="text/plain",
            use_container_width=True
        )