import streamlit as st
import pandas as pd
import base64
import os

# Importa as funções do BioCompiler
from biocompiler import (
    ler_arquivo,
    validar_bases,
    encontrar_start,
    encontrar_stop,
    deteccao_frameshift,
    deteccao_nonsense,
    transcrever_dna
)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="BioCompiler 1.0",
    page_icon="🧬",
    layout="wide"
)


# ============================================================
# CARREGAMENTO DA IMAGEM DE FUNDO
# ============================================================

imagem_fundo = "fundo_biocompiler.png"
imagem_base64 = ""

if os.path.exists(imagem_fundo):

    with open(imagem_fundo, "rb") as arquivo_imagem:

        imagem_base64 = base64.b64encode(
            arquivo_imagem.read()
        ).decode()

else:

    st.warning(
        "Imagem de fundo não encontrada. "
        "Verifique se o arquivo 'fundo_biocompiler.png' "
        "está na mesma pasta do app.py."
    )


# ============================================================
# ESTILO VISUAL
# ============================================================

if imagem_base64:

    st.markdown(
        f"""
        <style>

        /* ====================================================
           PLANO DE FUNDO
           ==================================================== */

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 20, 50, 0.10),
                    rgba(0, 20, 50, 0.10)
                ),
                url("data:image/png;base64,{imagem_base64}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}


        /* ====================================================
           ÁREA PRINCIPAL
           ==================================================== */

        .block-container {{
            background: transparent !important;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}


        /* ====================================================
           TÍTULOS
           ==================================================== */

        h1,
        h2,
        h3 {{
            color: white !important;
            font-weight: 800 !important;
            text-shadow:
                0 2px 5px rgba(0, 0, 0, 0.75);
        }}


        h1 {{
            text-align: center;
            font-size: 2.8rem !important;
        }}


        /* ====================================================
           TEXTOS
           ==================================================== */

        p,
        label {{
            color: white !important;
            text-shadow:
                0 1px 3px rgba(0, 0, 0, 0.75);
        }}


        /* ====================================================
           CARTÕES DE MÉTRICAS
           ==================================================== */

        div[data-testid="stMetric"] {{
            background:
                rgba(0, 0, 0, 0.30) !important;

            border:
                1px solid rgba(255, 255, 255, 0.30);

            border-radius: 14px;
            padding: 18px;

            box-shadow:
                0 4px 12px rgba(0, 0, 0, 0.25);
        }}


        div[data-testid="stMetricLabel"] {{
            color: white !important;
        }}


        div[data-testid="stMetricLabel"] p {{
            color: white !important;
        }}


        div[data-testid="stMetricValue"] {{
            color: white !important;
        }}


        /* ====================================================
           BOTÕES
           ==================================================== */

        div.stButton > button {{
            border-radius: 10px;
            font-size: 1.05rem;
            font-weight: 700;
            padding: 0.7rem 1rem;
        }}


        /* ====================================================
           TABELAS
           ==================================================== */

        div[data-testid="stDataFrame"] {{
            background:
                rgba(255, 255, 255, 0.92);

            border-radius: 10px;
            padding: 5px;
        }}


        /* ====================================================
           DETALHAMENTO
           ==================================================== */

        div[data-testid="stExpander"] {{
            background: rgba(0, 0, 0, 0.55) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 12px !important;
            margin-bottom: 10px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }}

        div[data-testid="stExpander"] summary {{
            background: rgba(0, 0, 0, 0.25) !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stExpander"] summary p {{
            color: white !important;
            font-weight: 700 !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
        }}

        div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
            background: rgba(0, 0, 0, 0.30) !important;
            border-radius: 0 0 12px 12px !important;
        }}

        div[data-testid="stExpander"] p {{
            color: white !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
        }}


        /* ====================================================
           ALERTAS
           ==================================================== */

        div[data-testid="stAlert"] {{
            border-radius: 10px;
        }}


        /* ====================================================
           DIVISORES
           ==================================================== */

        hr {{
            border-color:
                rgba(255, 255, 255, 0.30);
        }}


        /* ====================================================
           BARRA DE PROGRESSO
           ==================================================== */

        div[data-testid="stProgress"] > div > div {{
            background-color: #FFFFFF !important;
        }}


        div[data-testid="stProgress"] > div {{
            background-color: rgba(255, 255, 255, 0.25) !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FUNÇÃO PARA PROCESSAR UMA ENTRADA
# ============================================================

def processar_entrada(dna):

    # --------------------------------------------------------
    # 1. Validação das bases
    # --------------------------------------------------------

    if not validar_bases(dna):

        return {
            "Status": "ERRO",
            "Resposta": "BUG - base inválida",
            "START": "-",
            "STOP": "-",
            "Quadro": "-",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
        }


    # --------------------------------------------------------
    # 2. Procurar START
    # --------------------------------------------------------

    posicao_start = encontrar_start(dna)

    if posicao_start == -1:

        return {
            "Status": "ERRO",
            "Resposta": "BUG - START ausente",
            "START": "-",
            "STOP": "-",
            "Quadro": "-",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
        }


    # --------------------------------------------------------
    # 3. Procurar STOP no mesmo quadro de leitura
    # --------------------------------------------------------

    posicao_stop = encontrar_stop(
        dna,
        posicao_start
    )


    # --------------------------------------------------------
    # 4. Verificar frameshift quando não há STOP
    # --------------------------------------------------------

    if posicao_stop == -1:

        existe_frameshift = deteccao_frameshift(
            dna,
            posicao_start
        )

        if existe_frameshift:

            return {
                "Status": "ERRO",
                "Resposta": "BUG - frameshift",
                "START": "ATG",
                "STOP": "-",
                "Quadro": "ERRO",
                "Transcrição": "-",
                "Pré-RNA": "NÃO GERADO"
            }

        return {
            "Status": "ERRO",
            "Resposta": "BUG - STOP ausente",
            "START": "ATG",
            "STOP": "-",
            "Quadro": "OK",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
        }


    # --------------------------------------------------------
    # 5. Detectar nonsense / STOP prematuro
    # --------------------------------------------------------

    existe_nonsense = deteccao_nonsense(
        dna,
        posicao_stop
    )

    if existe_nonsense:

        return {
            "Status": "ERRO",
            "Resposta": "BUG - nonsense / STOP prematuro",
            "START": "ATG",
            "STOP": dna[posicao_stop:posicao_stop + 3],
            "Quadro": "OK",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
        }


    # --------------------------------------------------------
    # 6. Transcrição
    # --------------------------------------------------------

    pre_rna = transcrever_dna(
        dna,
        posicao_start,
        posicao_stop
    )

    stop = dna[
        posicao_stop:
        posicao_stop + 3
    ]


    # --------------------------------------------------------
    # 7. Sequência correta
    # --------------------------------------------------------

    return {
        "Status": "CORRETO",
        "Resposta": "CORRETO",
        "START": "ATG",
        "STOP": stop,
        "Quadro": "OK",
        "Transcrição": "OK",
        "Pré-RNA": pre_rna
    }


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
# FUNÇÃO PARA GERAR ARQUIVO DE EXPORTAÇÃO
# ============================================================

def gerar_arquivo_exportacao(resultados):

    linhas = []

    linhas.append(
        "linha;status;resultado;pre_mRNA"
    )

    for resultado in resultados:

        numero = resultado["Entrada"]
        status = resultado["Status"]
        resposta = resultado["Resposta"]
        pre_rna = resultado["Pré-RNA"]

        linhas.append(
            f"{numero};{status};{resposta};{pre_rna}"
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

st.header("📂 Entradas")

# O CSV já fica na pasta do projeto, junto com o app.py.
nome_arquivo = "BioCompiler_1_0_entrada_60_casos_NOVO.txt"

caminho_arquivo = os.path.join(
    os.path.dirname(__file__),
    nome_arquivo
)


try:

    entradas = ler_arquivo(caminho_arquivo)

except Exception as erro:

    st.error(
        f"Não foi possível carregar o arquivo de entradas: {erro}"
    )

    entradas = []


# ============================================================
# INFORMAÇÕES SOBRE AS ENTRADAS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Entradas carregadas",
        len(entradas)
    )


with col2:

    st.metric(
        "Formato",
        "TXT"
    )


st.divider()


# ============================================================
# EXECUÇÃO
# ============================================================

st.header("▶ Execução")


if st.button(
    "▶ Iniciar execução",
    type="primary",
    use_container_width=True
):

    if len(entradas) == 0:

        st.error(
            "Nenhuma entrada foi encontrada no CSV."
        )

    else:

        st.info(
            f"Processando {len(entradas)} entradas..."
        )


        # ----------------------------------------------------
        # Barra de progresso
        # ----------------------------------------------------

        barra = st.progress(0)

        resultados = []


        # ----------------------------------------------------
        # Processamento das entradas
        # ----------------------------------------------------

        for numero, dna in enumerate(
            entradas,
            start=1
        ):

            # Remove espaços acidentais nas extremidades.
            dna = str(dna).strip()

            resultado = processar_entrada(dna)


            resultados.append({

                "Entrada": numero,

                "DNA": dna,

                "Status": resultado["Status"],

                "Resposta": resultado["Resposta"],

                "START": resultado["START"],

                "STOP": resultado["STOP"],

                "Quadro": resultado["Quadro"],

                "Transcrição": resultado["Transcrição"],

                "Pré-RNA": resultado["Pré-RNA"]

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
        # DETALHAMENTO
        # ====================================================

        st.divider()

        st.header("🔬 Detalhamento")


        for resultado in resultados:

            numero = resultado["Entrada"]


            with st.expander(
                f"Entrada {numero} — {resultado['Resposta']}"
            ):

                st.write(
                    f"**ENTRADA:** {numero}"
                )

                st.write(
                    f"**STATUS:** {resultado['Status']}"
                )


                if resultado["Resposta"] == "CORRETO":

                    st.write(
                        "**Bases:** OK"
                    )

                    st.write(
                        "**START:** ATG - OK"
                    )

                    st.write(
                        "**Quadro de leitura:** OK"
                    )

                    st.write(
                        f"**STOP:** {resultado['STOP']} - OK"
                    )

                    st.write(
                        "**Transcrição:** OK"
                    )

                    st.write(
                        f"**pré-mRNA:** {resultado['Pré-RNA']}"
                    )

                else:

                    st.write(
                        f"**TIPO:** {resultado['Resposta']}"
                    )

                    st.write(
                        "**pré-mRNA:** NÃO GERADO"
                    )


        # ====================================================
        # RELATÓRIO DIAGNÓSTICO
        # ====================================================

        st.divider()

        st.header("📊 Relatório diagnóstico")


        diagnostico = gerar_diagnostico(
            resultados
        )


        # ----------------------------------------------------
        # Métricas
        # ----------------------------------------------------

        total = len(resultados)

        corretos = diagnostico["CORRETO"]

        bugs = total - corretos


        col1, col2, col3 = st.columns(3)


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


        # ----------------------------------------------------
        # Tabela do diagnóstico
        # ----------------------------------------------------

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
                diagnostico["CORRETO"],
                diagnostico["BUG - base inválida"],
                diagnostico["BUG - START ausente"],
                diagnostico["BUG - STOP ausente"],
                diagnostico["BUG - frameshift"],
                diagnostico["BUG - nonsense / STOP prematuro"]
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


        arquivo_resultados = gerar_arquivo_exportacao(
            resultados
        )


        st.download_button(
            label="📥 Exportar resultados",
            data=arquivo_resultados,
            file_name="resultados.txt",
            mime="text/plain",
            use_container_width=True
        )
