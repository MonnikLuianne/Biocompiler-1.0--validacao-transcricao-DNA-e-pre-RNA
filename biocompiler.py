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

        i+=3
    return -1

def encontrar_stop(dna,posicao_start):

    i = posicao_start + 3
    while i <= (len(dna)-3):
        if (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'A') or (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'G') or (dna[i] == 'T' and dna[i+1] == 'G' and dna[i+2] == 'A'):
            return i

        i+=3
    return -1

def deteccao_frameshift(dna,posicao_start):

    codons_parada = {"TAA", "TGA", "TAG"}

    ultimo_codon = dna[-3:] #Pega as 3 últimas bases da sequência

    if ultimo_codon not in codons_parada: #Se as últimas 3 bases não formam um STOP, não vou usar esse critério para dizer que tem frameshift
        return False

    posicao_stop_final = len(dna) - 3

    if (posicao_stop_final - posicao_start) % 3 != 0:
        return True

    return False

def deteccao_nonsense(dna,posicao_start):

    i = posicao_start + 3

    ultimo_codon = dna[-3:]

    posicao_stop_final = len(dna) - 3

    codons_parada = {"TAA", "TGA", "TAG"}

    if ultimo_codon in codons_parada:
        while i < posicao_stop_final:
            if (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'A') or (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'G') or (dna[i] == 'T' and dna[i+1] == 'G' and dna[i+2] == 'A'):
                return True
            i+=3
        return False

    return False

def transcrever_dna(dna, posicao_start, posicao_stop):

    i = posicao_start
    pre_rna = ""

    while i <= posicao_stop + 2:

        if dna[i] == 'T':
            pre_rna += 'U'
        else:
            pre_rna += dna[i]

        i += 1

    return pre_rna

            
if __name__ == "__main__":

    arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

    entradas = ler_arquivo(arquivo)

    for i, dna in enumerate(entradas,start = 1):

        resultado = validar_bases(dna)

        if resultado == False:
            print(f"Entrada {i}: BUG - base inválida")
            continue

        posicao_start = encontrar_start(dna)
        
        if posicao_start == -1:
            print(f"Entrada {i}: BUG - START Ausente")
            continue

        print(f"Entrada {i}: START encontrado na posição {posicao_start}")

        existe_frameshift = deteccao_frameshift(dna,posicao_start)
            
        if existe_frameshift:
            print(f"Entrada {i}: BUG - frameshift")
            continue
        
        posicao_stop = encontrar_stop(dna,posicao_start)

        if posicao_stop == -1:
            print(f"Entrada {i}: BUG - STOP Ausente")
            continue

        existe_nonsense = deteccao_nonsense(dna,posicao_start)

        if existe_nonsense:
            print(f"Entrada {i}: BUG - nonsense / STOP prematuro")
            continue

        print(f"Entrada {i}: CORRETO")
