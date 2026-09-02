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

---
#📄 Descrição dos arquivos

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

#app.py
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

#fundo_biocompiler.png
Imagem utilizada como plano de fundo da interface.
Deve permanecer na mesma pasta do app.py.

# 🧬 Funcionamento do BioCompiler

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


