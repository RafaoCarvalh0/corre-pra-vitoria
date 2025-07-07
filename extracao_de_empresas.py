import pandas as pd

# 1. Ler e filtrar empresas de porte 05
empresas = pd.read_csv(
    'Empresas9.csv',
    sep=';',
    dtype=str,
    header=None,
    names=[
        'cnpj_basico',
        'razao_social',
        'natureza_juridica',
        'qualificacao_responsavel',
        'capital_social',
        'porte',
        'ente_federativo'
    ],
    encoding='latin1'
)
empresas_grandes = empresas[empresas['porte'] == '05']

# 2. Ler estabelecimentos
estabelecimentos = pd.read_csv(
    'Estabelecimentos9.csv',
    sep=';',
    dtype=str,
    header=None,
    names=[
        'cnpj_basico',
        'cnpj_ordem',
        'cnpj_dv',
        'identificador_matriz_filial',
        'nome_fantasia',
        'situacao_cadastral',
        'data_situacao_cadastral',
        'motivo_situacao_cadastral',
        'nome_cidade_exterior',
        'pais',
        'data_inicio_atividade',
        'cnae_fiscal_principal',
        'cnae_fiscal_secundaria',
        'tipo_logradouro',
        'logradouro',
        'numero',
        'complemento',
        'bairro',
        'cep',
        'uf',
        'municipio',
        'ddd_1',
        'telefone_1',
        'ddd_2',
        'telefone_2',
        'ddd_fax',
        'fax',
        'correio_eletronico',
        'situacao_especial',
        'data_situacao_especial'
    ],
    encoding='latin1'
)

# 3. Filtrar estabelecimentos pelo CNPJ das grandes empresas, UF = 'SP' e situacao_cadastral = '2'
filtro = (
    estabelecimentos['cnpj_basico'].isin(list(empresas_grandes['cnpj_basico'])) &
    (estabelecimentos['uf'] == 'SP') &
    (estabelecimentos['situacao_cadastral'] == '02')
)
estab_filtrados = estabelecimentos[filtro]

# 4. Salvar resultado (ajuste as colunas conforme desejar)
colunas_resultado = [
    'cnpj_basico',
    'identificador_matriz_filial',
    'nome_fantasia',
    'tipo_logradouro',
    'logradouro',
    'numero',
    'bairro',
    'cep',
    'uf',
    'municipio',
    'cnae_fiscal_principal',
    'cnae_fiscal_secundaria'
]
resultado = pd.DataFrame(estab_filtrados[colunas_resultado])
resultado.to_csv('grandes_empresas_sp_interior9.csv', index=False)