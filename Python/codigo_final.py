# ============================================================
# ETAPA 01 — IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================
# Bibliotecas utilizadas para manipulação de dados, cálculos
# estatísticos e criação de gráficos.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# ETAPA 02 — CARREGAMENTO DOS DATASETS
# ============================================================
# Leitura dos arquivos CSV gerados a partir das consultas SQL.

df1 = pd.read_csv(
    r'C:\mini_projeto_final\mini_projeto_final\csv_nao_processados\query_01.csv',
    sep=',',
    encoding='utf-8'
)

df2 = pd.read_csv(
    r'C:\mini_projeto_final\mini_projeto_final\csv_nao_processados\query_02_completa.csv',
    sep=',',
    encoding='utf-8'
)


# ============================================================
# ETAPA 03 — INSPEÇÃO INICIAL DOS DADOS
# ============================================================
# Visualização das primeiras linhas e das colunas dos datasets.

print(df1.head(50))
print(df2.head(50))

print(df1.columns)
print(df2.columns)


# ============================================================
# ETAPA 04 — PADRONIZAÇÃO DOS NOMES DAS COLUNAS
# ============================================================
# Remove espaços e converte os nomes das colunas para letras maiúsculas.

df1.columns = df1.columns.str.strip().str.upper()
df2.columns = df2.columns.str.strip().str.upper()


# ============================================================
# ETAPA 05 — PADRONIZAÇÃO DAS CHAVES DE RELACIONAMENTO
# ============================================================
# Padroniza os campos usados na junção entre os datasets.

for coluna in ['DEPARTAMENTO', 'CARGO']:
    df1[coluna] = df1[coluna].astype(str).str.strip().str.upper()
    df2[coluna] = df2[coluna].astype(str).str.strip().str.upper()


# ============================================================
# ETAPA 06 — SELEÇÃO DAS COLUNAS COMPLEMENTARES
# ============================================================
# Seleciona da query_01 apenas as colunas necessárias para complementar a query_02.

df3 = df1[
    [
        'DEPARTAMENTO',
        'CARGO',
        'MENOR_SALARIO',
        'MAIOR_SALARIO'
    ]
]


# ============================================================
# ETAPA 07 — JUNÇÃO DOS DATASETS
# ============================================================
# Realiza um LEFT JOIN para manter todos os registros da base principal.

df_final = pd.merge(
    df2,
    df3,
    how='left',
    on=['DEPARTAMENTO', 'CARGO']
)


# ============================================================
# ETAPA 08 — ORGANIZAÇÃO DAS COLUNAS FINAIS
# ============================================================
# Organiza as colunas em uma sequência lógica para análise.

df_final = df_final[
    [
        'ID_EMPREGADO',
        'NOME_FUNCIONARIO',
        'REGIAO',
        'PAIS',
        'CIDADE',
        'DEPARTAMENTO',
        'CARGO',
        'SALARIO',
        'QUANTIDADE_FUNCIONARIOS',
        'MENOR_SALARIO',
        'MAIOR_SALARIO'
    ]
]


# ============================================================
# ETAPA 09 — RENOMEAÇÃO DA COLUNA SALARIAL
# ============================================================
# Renomeia SALARIO para SALARIO_ATUAL, deixando o campo mais claro.

df_final.rename(columns={'SALARIO': 'SALARIO_ATUAL'}, inplace=True)


# ============================================================
# ETAPA 10 — CONVERSÃO DAS COLUNAS NUMÉRICAS
# ============================================================
# Garante que as colunas numéricas sejam tratadas corretamente como números.

colunas_numericas = [
    'ID_EMPREGADO',
    'SALARIO_ATUAL',
    'QUANTIDADE_FUNCIONARIOS',
    'MENOR_SALARIO',
    'MAIOR_SALARIO'
]

for coluna in colunas_numericas:
    df_final[coluna] = pd.to_numeric(df_final[coluna], errors='coerce')


# ============================================================
# ETAPA 11 — VERIFICAÇÃO DE VALORES NULOS
# ============================================================
# Identifica a quantidade de valores ausentes por coluna.

print(df_final.isna().sum())


# ============================================================
# ETAPA 12 — ANÁLISE DOS REGISTROS COM VALORES NULOS
# ============================================================
# Exibe as linhas que possuem pelo menos um campo sem informação.

valores_nulos = df_final[df_final.isnull().any(axis=1)]

print(valores_nulos)


# ============================================================
# ETAPA 13 — TRATAMENTO DE VALORES NULOS TEXTUAIS
# ============================================================
# Substitui valores nulos apenas nas colunas de texto.
# As colunas numéricas permanecem como NaN para não prejudicar os cálculos.

colunas_texto = [
    'NOME_FUNCIONARIO',
    'REGIAO',
    'PAIS',
    'CIDADE',
    'DEPARTAMENTO',
    'CARGO'
]

df_final[colunas_texto] = df_final[colunas_texto].fillna('SEM INFORMAÇÃO')


# ============================================================
# ETAPA 14 — VERIFICAÇÃO FINAL DA ESTRUTURA DOS DADOS
# ============================================================
# Confere os valores nulos, primeiras linhas e tipos de dados.

print(df_final.isna().sum())
print(df_final.head())
print(df_final.dtypes)


# ============================================================
# ETAPA 15 — ANÁLISE ESTATÍSTICA DO SALÁRIO ATUAL
# ============================================================
# Calcula média, mediana, valor mínimo e valor máximo dos salários.

media_salario = df_final['SALARIO_ATUAL'].mean()
mediana_salario = df_final['SALARIO_ATUAL'].median()
minimo_salario = df_final['SALARIO_ATUAL'].min()
maximo_salario = df_final['SALARIO_ATUAL'].max()

print(f'Média do salário atual: {media_salario:.2f}')
print(f'Mediana do salário atual: {mediana_salario:.2f}')
print(f'Valor mínimo do salário atual: {minimo_salario:.2f}')
print(f'Valor máximo do salário atual: {maximo_salario:.2f}')


# ============================================================
# ETAPA 16 — PREPARAÇÃO PARA ANÁLISE DE OUTLIERS
# ============================================================
# Seleciona a coluna salarial e remove valores nulos para análise estatística.

coluna = 'SALARIO_ATUAL'

salarios = df_final[coluna].dropna()


# ============================================================
# ETAPA 17 — CÁLCULO DO IQR
# ============================================================
# Calcula quartis, intervalo interquartil e limites para detectar outliers.

Q1 = salarios.quantile(0.25)
Q3 = salarios.quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR


# ============================================================
# ETAPA 18 — IDENTIFICAÇÃO DOS OUTLIERS
# ============================================================
# Filtra salários abaixo do limite inferior ou acima do limite superior.

outliers = salarios[
    (salarios < limite_inferior) |
    (salarios > limite_superior)
]

print(f'Q1: {Q1:.2f}')
print(f'Q3: {Q3:.2f}')
print(f'IQR: {IQR:.2f}')
print(f'Limite inferior: {limite_inferior:.2f}')
print(f'Limite superior: {limite_superior:.2f}')
print(f'Quantidade de outliers identificados: {len(outliers)}')

print(outliers)


# ============================================================
# ETAPA 19 — BOXPLOT DOS SALÁRIOS
# ============================================================
# Cria um boxplot para visualizar a distribuição salarial e os outliers.

plt.figure(figsize=(14, 8))

plt.boxplot(
    salarios,
    vert=False,
    patch_artist=True
)

plt.axvline(Q1, linestyle='--', label=f'Q1: {Q1:.2f}')
plt.axvline(Q3, linestyle='--', label=f'Q3: {Q3:.2f}')
plt.axvline(limite_inferior, linestyle=':', label=f'Limite Inferior: {limite_inferior:.2f}')
plt.axvline(limite_superior, linestyle=':', label=f'Limite Superior: {limite_superior:.2f}')

plt.title('Análise de Outliers no Salário Atual pelo Método IQR')
plt.xlabel('Salário Atual')
plt.legend()
plt.grid(axis='x', alpha=0.3)

plt.show()


# ============================================================
# ETAPA 20 — GRÁFICO DE BARRAS DA DISTRIBUIÇÃO SALARIAL
# ============================================================
# Cria faixas salariais e mostra a frequência de salários em cada faixa.

plt.figure(figsize=(14, 8))

frequencias, faixas = np.histogram(salarios, bins=30)

centro_faixas = (faixas[:-1] + faixas[1:]) / 2

largura_barra = faixas[1] - faixas[0]

plt.bar(
    centro_faixas,
    frequencias,
    width=largura_barra,
    edgecolor='black',
    alpha=0.7
)

plt.axvline(Q1, linestyle='--', linewidth=1, label=f'Q1: {Q1:.2f}')
plt.axvline(Q3, linestyle='--', linewidth=1, label=f'Q3: {Q3:.2f}')
plt.axvline(limite_inferior, linestyle=':', linewidth=1, label=f'Limite Inferior: {limite_inferior:.2f}')
plt.axvline(limite_superior, linestyle=':', linewidth=1, label=f'Limite Superior: {limite_superior:.2f}')

plt.title('Barplot da Distribuição do Salário Atual com Limites do IQR')
plt.xlabel('Salário Atual')
plt.ylabel('Frequência')

plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.show()


# ============================================================
# ETAPA 21 — EXPORTAÇÃO DA BASE FINAL
# ============================================================
# Salva o dataset tratado e consolidado em CSV para análises futuras.

df_final.to_csv(
    r'C:\mini_projeto_final\mini_projeto_final\processados\final.csv',
    index=False,
    encoding='utf-8'
)

print('Base final exportada com sucesso para o arquivo final.csv')