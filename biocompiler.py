import pandas as pd

def ler_arquivo(caminho):
    if caminho.endswith(".csv"):
        tabela = pd.read_csv(caminho)
        entradas = tabela["entrada"].tolist()

    else:
        with open(caminho,"r",encoding="utf-8") as arquivo:
            entradas = []

            for linha in arquivo:
                entradas.append(linha.strip())

    return entradas


def validar_bases(dna):
    bases_validas = {"A", "T", "C", "G"}

    for base in dna:
        if base not in bases_validas:
            return False

    return True

def encontrar_start(dna):

    i = 0
    while i <= (len(dna)-3): #Para tentar validar a presença de A apenas até a última posição que ainda dá pra colocar um códon

        if dna[i] == 'A' and dna[i+1] == 'T' and dna[i+2] == 'G':
            return i

        i+=1
    return -1

def encontrar_stop(dna,posicao_start):

    i = posicao_start + 3
    while i <= (len(dna)-3):
        if (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'A') or (dna[i] == 'T' and dna[i+1] == 'A' and dna[i+2] == 'G') or (dna[i] == 'T' and dna[i+1] == 'G' and dna[i+2] == 'A'):
            return i

        i+=3
    return -1

def deteccao_frameshift(dna,posicao_start):

    tamanho_regiao = len(dna) - posicao_start

    if tamanho_regiao % 3 != 0:
        return True

    return False

def deteccao_nonsense(dna,posicao_stop):

    codons_parada = {"TAA","TAG","TGA"}

    i = posicao_stop + 3

    while i <= len(dna) - 3:
        codon = dna[i:i+3]
        if codon in codons_parada:
            return True
        i+=3
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

def exibir_resultado(numero_entrada, resultado, pre_rna=None, stop=None):

    print("======================================")
    print(f"ENTRADA: {numero_entrada}")

    if resultado == "CORRETO":
        print("STATUS: CORRETO")
        print("Bases: OK")
        print("START: ATG - OK")
        print("Quadro de leitura: OK")
        print(f"STOP: {stop} - OK")
        print("Transcrição: OK")
        print(f"pré-mRNA: {pre_rna}")

    else:
        print("STATUS: ERRO")
        print(f"TIPO: {resultado}")
        print("pré-mRNA: NÃO GERADO")

    print("--------------------------------------")

def salvar_resultados(resultados):

    with open("resultados.txt", "w", encoding="utf-8") as arquivo:

        arquivo.write("linha;status;resultado;pre_mRNA\n")

        for resultado in resultados:
            arquivo.write(resultado + "\n")


            
if __name__ == "__main__":

    arquivo = "BioCompiler_1_0_60_casos_alunos_SEM RESPOSTAS.csv"

    entradas = ler_arquivo(arquivo)

    resultados = []

    for i, dna in enumerate(entradas,start = 1):

        resultado = validar_bases(dna)

        if resultado == False:
            diagnostico = "BUG - base inválida"
            exibir_resultado(i,diagnostico)
            resultados.append(f"{i};ERRO;{diagnostico};NÃO GERADO")
            continue

        posicao_start = encontrar_start(dna)
        
        if posicao_start == -1:
            diagnostico = "BUG - START ausente"
            exibir_resultado(i,diagnostico)
            resultados.append(f"{i};ERRO;{diagnostico};NÃO GERADO")
            continue

        posicao_stop = encontrar_stop(dna,posicao_start)

        if posicao_stop == -1:
            existe_frameshift = deteccao_frameshift(dna,posicao_start)
                
            if existe_frameshift:
                diagnostico = "BUG - frameshift"
                exibir_resultado(i,diagnostico)
                resultados.append(f"{i};ERRO;{diagnostico};NÃO GERADO")
                continue
        
            diagnostico = "BUG - STOP ausente"
            exibir_resultado(i,diagnostico)
            resultados.append(f"{i};ERRO;{diagnostico};NÃO GERADO")
            continue

        existe_nonsense = deteccao_nonsense(dna,posicao_stop)

        if existe_nonsense:
            diagnostico = "BUG - nonsense / STOP prematuro"
            exibir_resultado(i,diagnostico)
            resultados.append(f"{i};ERRO;{diagnostico};NÃO GERADO")
            continue

        pre_rna = transcrever_dna(dna,posicao_start,posicao_stop)
        stop = dna[posicao_stop:posicao_stop + 3]
        exibir_resultado(i,"CORRETO",pre_rna,stop)
        resultados.append(f"{i};OK;CORRETO;{pre_rna}")

    salvar_resultados(resultados)
