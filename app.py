import streamlit as st
import pandas as pd
import base64
import os

<<<<<<< HEAD
# Importa as funções do BioCompiler
=======
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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
<<<<<<< HEAD
            background-color: rgba(255, 255, 255, 0.25) !important;
=======

            background-color:
                rgba(255, 255, 255, 0.25) !important;

>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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
    # 1. Verificar bases
    # --------------------------------------------------------

    if not validar_bases(dna):

        return {
            "Status": "ERRO",
            "Resposta": "BUG - base inválida",
            "START": "-",
            "STOP": "-",
<<<<<<< HEAD
            "Quadro": "-",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
=======
            "Pré-mRNA": "-"
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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
<<<<<<< HEAD
            "Quadro": "-",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
=======
            "Pré-mRNA": "-"
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
        }


    # --------------------------------------------------------
<<<<<<< HEAD
    # 3. Procurar STOP no mesmo quadro de leitura
=======
    # 3. Verificar frameshift
    # --------------------------------------------------------

    existe_frameshift = deteccao_frameshift(
        dna,
        posicao_start
    )

    if existe_frameshift:

        return {
            "Resposta": "BUG - frameshift",
            "START": posicao_start,
            "STOP": "-",
            "Pré-mRNA": "-"
        }


    # --------------------------------------------------------
    # 4. Procurar STOP
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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
<<<<<<< HEAD
            "Quadro": "OK",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
=======
            "Pré-mRNA": "-"
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
        }


    # --------------------------------------------------------
<<<<<<< HEAD
    # 5. Detectar nonsense / STOP prematuro
=======
    # 5. Verificar nonsense / STOP prematuro
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
    # --------------------------------------------------------

    existe_nonsense = deteccao_nonsense(
        dna,
        posicao_stop
    )

    if existe_nonsense:

        return {
<<<<<<< HEAD
            "Status": "ERRO",
            "Resposta": "BUG - nonsense / STOP prematuro",
            "START": "ATG",
            "STOP": dna[posicao_stop:posicao_stop + 3],
            "Quadro": "OK",
            "Transcrição": "-",
            "Pré-RNA": "NÃO GERADO"
=======
            "Resposta":
                "BUG - nonsense / STOP prematuro",

            "START": posicao_start,

            "STOP": posicao_stop,

            "Pré-mRNA": "-"
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
        }


    # --------------------------------------------------------
<<<<<<< HEAD
    # 6. Transcrição
=======
    # 6. Entrada correta
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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


    return {
        "Status": "CORRETO",
        "Resposta": "CORRETO",
<<<<<<< HEAD
        "START": "ATG",
        "STOP": stop,
        "Quadro": "OK",
        "Transcrição": "OK",
        "Pré-RNA": pre_rna
=======

        "START": posicao_start,

        "STOP": posicao_stop,

        "Pré-mRNA": pre_rna
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
    }


# ============================================================
# FUNÇÃO PARA PROCESSAR TODAS AS ENTRADAS
# ============================================================

def processar_entradas(entradas):

    resultados = []


    for numero, dna in enumerate(
        entradas,
        start=1
    ):

        resultado = processar_entrada(dna)


        resultados.append({

            "Entrada": numero,

            "DNA": dna,

            "Resposta":
                resultado["Resposta"],

            "START":
                resultado["START"],

            "STOP":
                resultado["STOP"],

            "Pré-mRNA":
                resultado["Pré-mRNA"]

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
# FUNÇÃO PARA GERAR ARQUIVO DE EXPORTAÇÃO
# ============================================================

def gerar_arquivo_exportacao(resultados):

    linhas = []

    linhas.append(
        "linha;status;resultado;pre_mRNA"
    )

    for resultado in resultados:

        numero = resultado["Entrada"]
<<<<<<< HEAD
        status = resultado["Status"]
        resposta = resultado["Resposta"]
        pre_rna = resultado["Pré-RNA"]

=======

        resposta = resultado["Resposta"]


        # ----------------------------------------------------
        # Resposta
        # ----------------------------------------------------

>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
        linhas.append(
            f"{numero};{status};{resposta};{pre_rna}"
        )

<<<<<<< HEAD
=======

        # ----------------------------------------------------
        # Pré-mRNA somente para entradas corretas
        # ----------------------------------------------------

        if resposta == "CORRETO":

            pre_rna = resultado["Pré-mRNA"]

            linhas.append(
                f"Pré-mRNA: {pre_rna}"
            )


        linhas.append("")

>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2

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

<<<<<<< HEAD
st.header("📂 Entradas")

# O CSV já fica na pasta do projeto, junto com o app.py.
nome_arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

caminho_arquivo = os.path.join(
    os.path.dirname(__file__),
    nome_arquivo
=======
arquivo = (
    "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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

<<<<<<< HEAD
=======
st.header("📂 Entradas")


>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Entradas carregadas",
        len(entradas)
    )


with col2:

    st.metric(
        "Formato",
        "CSV"
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

<<<<<<< HEAD
                "Status": resultado["Status"],

                "Resposta": resultado["Resposta"],
=======
                "Resposta":
                    resultado["Resposta"],
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2

                "START":
                    resultado["START"],

                "STOP":
                    resultado["STOP"],

<<<<<<< HEAD
                "Quadro": resultado["Quadro"],

                "Transcrição": resultado["Transcrição"],

                "Pré-RNA": resultado["Pré-RNA"]
=======
                "Pré-mRNA":
                    resultado["Pré-mRNA"]
>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2

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

        st.header(
            "📋 Resultados da execução"
        )


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

        st.header(
            "📊 Relatório diagnóstico"
        )


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
<<<<<<< HEAD
                diagnostico["BUG - base inválida"],
                diagnostico["BUG - START ausente"],
                diagnostico["BUG - STOP ausente"],
                diagnostico["BUG - frameshift"],
                diagnostico["BUG - nonsense / STOP prematuro"]
=======

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

>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
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

        st.header(
            "📥 Exportação"
        )


        arquivo_resultados = gerar_arquivo_exportacao(
            resultados
        )


        st.download_button(
            label="📥 Exportar resultados",
            data=arquivo_resultados,
            file_name="resultados.txt",
            mime="text/plain",
            use_container_width=True
<<<<<<< HEAD
=======

>>>>>>> 6ada605f4dfb4caf587046688405b90480118fc2
        )
