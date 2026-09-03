# 🧬 BioCompiler 1.0

## DNA Transcriber

O **BioCompiler 1.0** é um sistema desenvolvido em Python para **validação, análise e transcrição de sequências de DNA**.

O sistema foi desenvolvido utilizando **Python, Pandas e Streamlit**, possuindo uma interface gráfica para facilitar a execução e visualização dos resultados.

A aplicação recebe um conjunto de **60 sequências de DNA**, realiza uma sequência de verificações e classifica cada entrada de acordo com os possíveis problemas encontrados.

Quando uma entrada é considerada correta, o sistema realiza a transcrição da região correspondente de DNA para **Pré-mRNA**.

---

# 🎯 Objetivo do projeto

O objetivo do BioCompiler 1.0 é desenvolver uma aplicação capaz de analisar sequências de DNA e identificar possíveis problemas relacionados à sequência.

Para cada entrada, o sistema realiza as seguintes verificações:

1. Validação das bases nitrogenadas;
2. Identificação do códon START;
3. Detecção de frameshift;
4. Identificação do códon STOP;
5. Detecção de nonsense / STOP prematuro;
6. Classificação da entrada;
7. Transcrição para Pré-mRNA quando a entrada é considerada correta.

Além do processamento, o sistema disponibiliza uma interface gráfica para:

- executar as 60 entradas;
- acompanhar o progresso;
- visualizar os resultados;
- consultar o diagnóstico geral;
- visualizar o Pré-mRNA;
- exportar os resultados para um arquivo `.txt`.

------
### 📄 Descrição dos arquivos

# biocompiler.py
Contém a lógica principal do BioCompiler.
Entre as principais funções estão:
ler_arquivo()
validar_bases()
encontrar_start()
encontrar_stop()
deteccao_frameshift()
deteccao_nonsense()
transcrever_dna()

# app.py
Responsável pela interface gráfica do sistema utilizando Streamlit.
Principais responsabilidades:
configuração da página;
criação da interface;
carregamento das entradas;
execução dos casos;
apresentação dos resultados;
relatório diagnóstico;
exportação dos resultados;
organização visual da aplicação.

# fundo_biocompiler.png
Imagem utilizada como plano de fundo da interface.
Deve permanecer na mesma pasta do app.py.

# BioCompiler_1_0_entrada_60_casos_NOVO.txt
Contém as 60 entradas utilizadas pelo sistema.
Deve permanecer na mesma pasta do projeto.

### 🧬 Funcionamento do BioCompiler

O processamento de cada sequência segue uma ordem definida.

```text
                    SEQUÊNCIA DE DNA
                           │
                           ▼
                  ┌─────────────────┐
                  │ Bases válidas?  │
                  └─────────────────┘
                     │           │
                    NÃO         SIM
                     │           │
                     ▼           ▼
             BASE INVÁLIDA   ┌───────────────┐
                             │ Existe START? │
                             └───────────────┘
                                │         │
                               NÃO       SIM
                                │         │
                                ▼         ▼
                         START AUSENTE  ┌───────────────┐
                                       │  Frameshift?   │
                                       └───────────────┘
                                          │         │
                                         SIM       NÃO
                                          │         │
                                          ▼         ▼
                                    FRAMESHIFT   ┌──────────────┐
                                                 │ Existe STOP? │
                                                 └──────────────┘
                                                   │         │
                                                  NÃO       SIM
                                                   │         │
                                                   ▼         ▼
                                             STOP AUSENTE  ┌───────────────┐
                                                           │   Nonsense?   │
                                                           └───────────────┘
                                                              │        │
                                                             SIM      NÃO
                                                              │        │
                                                              ▼        ▼
                                                        NONSENSE     CORRETO
                                                                     │
                                                                     ▼
                                                                PRÉ-mRNA




```
## ▶️ Como executar o projeto

### 1. Clonar o repositório
git clone https://github.com/MonnikLuianne/Biocompiler-validacao-transcricao-DNA-e-pre-RNA.git
### 2. Acessar a pasta do projeto
cd Biocompiler-validacao-transcricao-DNA-e-pre-RNA
### 3. Criar o ambiente virtual
No Windows:
python -m venv .venv
### 4. Ativar o ambiente virtual
No Windows:
.venv\Scripts\activate
### 5. Instalar as dependências
pip install -r requirements.txt
### 6. Executar a aplicação
streamlit run app.py
Após executar o comando, o Streamlit abrirá a aplicação no navegador.
### 7. Utilizar o sistema
Na interface do BioCompiler:
Clique no botão "Iniciar processamento".
O sistema processará as 60 entradas presentes no arquivo BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv.
Os resultados de cada entrada serão apresentados na interface.
O sistema exibirá um diagnóstico com a quantidade de ocorrências de cada tipo de resultado.
Para as entradas classificadas como CORRETO, será apresentada a sequência de Pré-RNA.
Ao final do processamento, será possível exportar os resultados.
# 📄 Exportação dos resultados
O sistema possui uma opção para exportar os resultados do processamento.
Ao clicar no botão de exportação, será gerado o arquivo:
resultados_biocompiler.txt
O arquivo contém as informações obtidas durante o processamento das 60 entradas, incluindo:
Número da entrada;
Sequência de DNA;
Resultado do diagnóstico;
Posição do START;
Posição do STOP;
Sequência de Pré-RNA, quando aplicável.
O arquivo pode ser salvo pelo usuário e utilizado para consulta ou entrega dos resultados do processamento.

