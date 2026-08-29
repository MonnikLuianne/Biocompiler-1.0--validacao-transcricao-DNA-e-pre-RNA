import pandas as pd

def ler_arquivo(caminho):
    tabela = pd.read_csv(caminho)

    entradas = tabela["entrada"].tolist()

    return entradas

arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

entradas = ler_arquivo(arquivo)

def validar_bases(dna):
    bases_validas = {"A", "T", "C", "G"}

    for base in dna:
        if base not in bases_validas:
            return False

    return True

for i, dna in enumerate(entradas,start = 1):

    resultado = validar_bases(dna)
    print(f"Entrada{i}:{resultado}")

    