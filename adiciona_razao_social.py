import csv
import os

# Arquivos de entrada e saída
ARQ_TODAS = 'todas_grandes_empresas_sp_interior_v2.csv'
ARQ_SAIDA = 'todas_grandes_empresas_sp_interior_v2_com_razao_social.csv'

# Primeiro, carrega todos os CNPJs do arquivo todas_grandes_empresas_sp_interior_v2.csv
print("Carregando CNPJs do arquivo todas_grandes_empresas_sp_interior_v2.csv...")
cnpjs_necessarios = set()
with open(ARQ_TODAS, encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Pula o cabeçalho
    for row in reader:
        if row:
            cnpj = row[0].strip().replace('"', '')
            cnpjs_necessarios.add(cnpj)

print(f"Total de CNPJs únicos encontrados: {len(cnpjs_necessarios)}")

# Agora lê todos os arquivos Empresas1.csv até Empresas9.csv
mapa_razao_social = {}
for n in range(0, 10):
    arquivo_empresas = f'Empresas{n}.csv'
    if os.path.exists(arquivo_empresas):
        print(f"Processando {arquivo_empresas}...")
        with open(arquivo_empresas, encoding='latin1') as f:
            reader = csv.reader(f, delimiter=';')
            for i, row in enumerate(reader):
                if len(row) >= 2:
                    cnpj = row[0].strip().replace('"', '')
                    if cnpj in cnpjs_necessarios:
                        razao = row[1].strip().replace('"', '')
                        mapa_razao_social[cnpj] = razao
                        if len(mapa_razao_social) <= 10:  # Mostra as primeiras 10 entradas para debug
                            print(f"  CNPJ encontrado: {cnpj} -> Razão: {razao}")
    else:
        print(f"Arquivo {arquivo_empresas} não encontrado, pulando...")

print(f"Total de empresas filtradas e carregadas: {len(mapa_razao_social)}")

# Verifica se o arquivo de saída já existe
arquivo_existe = os.path.exists(ARQ_SAIDA)

# Lê todas_grandes_empresas_sp_interior_v2.csv, adiciona a coluna e escreve o novo arquivo
print("Processando arquivo todas_grandes_empresas_sp_interior_v2.csv...")
with open(ARQ_TODAS, encoding='utf-8') as fin, open(ARQ_SAIDA, 'a', encoding='utf-8', newline='') as fout:
    reader = csv.reader(fin)
    writer = csv.writer(fout)
    
    # Se o arquivo não existe, escreve o cabeçalho
    if not arquivo_existe:
        header = next(reader)
        header.append('razao_social')
        writer.writerow(header)
        print("Cabeçalho escrito no arquivo de saída")
    else:
        # Se o arquivo já existe, pula o cabeçalho
        next(reader)
        print("Arquivo de saída já existe, pulando cabeçalho")
    
    correspondencias_encontradas = 0
    for i, row in enumerate(reader):
        if row:
            cnpj = row[0].strip().replace('"', '')
            razao = mapa_razao_social.get(cnpj, '')
            if razao:
                correspondencias_encontradas += 1
                if correspondencias_encontradas <= 10:  # Mostra as primeiras 10 correspondências
                    print(f"Correspondência encontrada: {cnpj} -> {razao}")
            row.append(razao)
            writer.writerow(row)
    
    print(f"Total de correspondências encontradas: {correspondencias_encontradas}")
    print(f"Total de linhas processadas: {i+1}")
    print(f"Arquivo de saída: {ARQ_SAIDA}") 