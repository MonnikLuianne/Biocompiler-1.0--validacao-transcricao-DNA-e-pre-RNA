import pandas as pd

def ler_arquivo(caminho):
    tabela = pd.read_csv(caminho)

    entradas = tabela["entrada"].tolist()

    return entradas


def validar_bases(dna):
    bases_validas = {"A", "T", "C", "G"}

    for base in dna:
        if base not in bases_validas:
            return False

    return True

def encontrar_start(dna):

    i = 0
    while i <= (len(dna)-3): #Para tentar validar a presença de A apenas até o antepenúltimo termo

        if dna[i] == 'A' and dna[i+1] == 'T' and dna[i+2] == 'G':
            return i

        i+=1
    return -1



if __name__ == "__main__":

    arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

    entradas = ler_arquivo(arquivo)

    for i, dna in enumerate(entradas,start = 1):

        resultado = validar_bases(dna)

        if resultado == False:
            print("BUG - base inválida")
            continue

        posicao_start = encontrar_start(dna)
        
        if posicao_start == -1:
            print(f"BUG - START Ausente")
            continue

        print(f"Entrada {i}: START encontrado na posição {posicao_start}")


