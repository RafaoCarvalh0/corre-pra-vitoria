import pandas as pd
import glob

def juntar_csvs():
    """
    Junta todos os arquivos CSV do diretório atual em um único arquivo,
    como se fosse uma única planilha.
    """
    
    # Lista todos os arquivos CSV no diretório atual
    arquivos_csv = glob.glob('*.csv')
    
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado no diretório atual.")
        return
    
    print(f"Encontrados {len(arquivos_csv)} arquivos CSV:")
    for arquivo in arquivos_csv:
        print(f"  - {arquivo}")
    
    # Lista para armazenar todos os DataFrames
    dataframes = []
    
    # Lê cada arquivo CSV
    for arquivo in arquivos_csv:
        try:
            print(f"Lendo {arquivo}...")
            
            # Tenta diferentes encodings
            for encoding in ['utf-8', 'latin1', 'cp1252']:
                try:
                    # Primeiro tenta com ponto e vírgula
                    df = pd.read_csv(arquivo, sep=';', encoding=encoding, dtype=str)
                    print(f"  ✓ Lido com encoding {encoding} e separador ';'")
                    break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    try:
                        # Se falhar, tenta com vírgula
                        df = pd.read_csv(arquivo, sep=',', encoding=encoding, dtype=str)
                        print(f"  ✓ Lido com encoding {encoding} e separador ','")
                        break
                    except:
                        continue
            else:
                print(f"  ✗ Erro ao ler {arquivo} - encoding não suportado")
                continue
            
            dataframes.append(df)
            
        except Exception as e:
            print(f"  ✗ Erro ao processar {arquivo}: {str(e)}")
            continue
    
    if not dataframes:
        print("Nenhum arquivo CSV foi lido com sucesso.")
        return
    
    # Junta todos os DataFrames
    print("\nJuntando todos os arquivos...")
    df_final = pd.concat(dataframes, ignore_index=True)
    
    # Salva o arquivo final
    nome_arquivo_final = 'todas_grandes_empresas_sp_interior.csv'
    df_final.to_csv(nome_arquivo_final, sep=',', index=False, encoding='utf-8', quoting=0)
    
    print(f"\n✓ Arquivo final criado: {nome_arquivo_final}")
    print(f"✓ Total de linhas: {len(df_final)}")
    print(f"✓ Total de colunas: {len(df_final.columns)}")
    print(f"✓ Colunas: {list(df_final.columns)}")

if __name__ == "__main__":
    juntar_csvs() 