# Projeto SQL — Análise de Funcionários e Salários no FreeSQL

## 1. Contexto do Projeto

Este projeto tem como objetivo realizar análises em SQL utilizando o **FreeSQL** e a base de dados **HR**, uma base própria disponibilizada no ambiente FreeSQL.

Foram desenvolvidas duas consultas principais:

- **query_01.sql**: análise da distribuição de salários por departamento e cargo.
- **query_02.sql**: análise de funcionários por região, incluindo informações de localização.

Após a execução das consultas no FreeSQL, os resultados da **query_01** e da **query_02** foram salvos em arquivos **CSV**. Essa etapa foi realizada para permitir a continuidade da análise em **Python**, possibilitando novas etapas de exploração, limpeza, visualização e modelagem dos dados com bibliotecas como `pandas`, `matplotlib`, `seaborn` e outras ferramentas analíticas.

As consultas utilizam a tabela `HR.EMPLOYEES` como base principal e realizam relacionamentos com tabelas dimensionais por meio de `LEFT JOIN`.

---

## 2. Ambiente Utilizado

- **Ferramenta:** FreeSQL
- **Base de dados:** HR
- **Linguagem:** SQL
- **Formato de saída:** CSV, para continuidade das análises em Python
- **Tabelas utilizadas:**
  - `HR.EMPLOYEES`
  - `HR.DEPARTMENTS`
  - `HR.JOBS`
  - `HR.LOCATIONS`
  - `HR.COUNTRIES`
  - `HR.REGIONS`

---

## 3. Relacionamento entre as Tabelas

A lógica das consultas foi baseada nos seguintes relacionamentos:

```sql
HR.EMPLOYEES.DEPARTMENT_ID = HR.DEPARTMENTS.DEPARTMENT_ID
HR.EMPLOYEES.JOB_ID        = HR.JOBS.JOB_ID
HR.DEPARTMENTS.LOCATION_ID = HR.LOCATIONS.LOCATION_ID
HR.LOCATIONS.COUNTRY_ID    = HR.COUNTRIES.COUNTRY_ID
HR.COUNTRIES.REGION_ID     = HR.REGIONS.REGION_ID
```

A tabela `HR.EMPLOYEES` foi utilizada como tabela principal, pois contém os funcionários, seus cargos, departamentos e salários. As demais tabelas foram relacionadas para enriquecer a análise com informações de departamento, cargo, localização, país e região.

---

# Query 01 — Distribuição de Salários por Departamento e Cargo

## 4. Pergunta de Negócio

**Como os salários estão distribuídos por departamento e cargo?**

A primeira consulta foi desenvolvida para analisar a distribuição salarial considerando o departamento e o cargo dos funcionários.

---

## 5. Objetivo da Query 01

A `query_01.sql` tem como objetivo apresentar uma visão consolidada por **departamento** e **cargo**, permitindo observar:

- quantidade de funcionários por departamento e cargo;
- menor faixa salarial cadastrada para o cargo;
- maior faixa salarial cadastrada para o cargo;
- distribuição dos cargos dentro dos departamentos.

---

## 6. Tabelas Utilizadas na Query 01

A consulta utiliza as seguintes tabelas:

### `HR.EMPLOYEES`

Tabela principal da consulta. Contém os dados dos funcionários, como:

- `EMPLOYEE_ID`
- `DEPARTMENT_ID`
- `JOB_ID`

### `HR.DEPARTMENTS`

Tabela utilizada para identificar o nome do departamento.

Campo utilizado:

- `DEPARTMENT_NAME`

### `HR.JOBS`

Tabela utilizada para identificar o cargo e a faixa salarial cadastrada para cada cargo.

Campos utilizados:

- `JOB_TITLE`
- `MIN_SALARY`
- `MAX_SALARY`

---

## 7. Processo Realizado na Query 01

A consulta realiza os seguintes passos:

1. Parte da tabela `HR.EMPLOYEES`, que contém os funcionários.
2. Faz um `LEFT JOIN` com `HR.DEPARTMENTS` para buscar o nome do departamento.
3. Faz um `LEFT JOIN` com `HR.JOBS` para buscar o cargo e a faixa salarial.
4. Agrupa os dados por departamento e cargo.
5. Calcula a quantidade de funcionários em cada grupo.
6. Calcula o menor e o maior salário de referência cadastrados na tabela de cargos.
7. Ordena o resultado por departamento e cargo.

---

## 8. Código da Query 01

```sql
-- ANALISAR A DISTRIBUIÇÃO DE SALÁRIOS POR DEPARTAMENTO E CARGO

SELECT
    d.DEPARTMENT_NAME AS departamento,
    j.JOB_TITLE AS cargo,
    COUNT(e.EMPLOYEE_ID) AS quantidade_funcionarios,
    MIN(j.MIN_SALARY) AS menor_salario,
    MAX(j.MAX_SALARY) AS maior_salario
FROM HR.EMPLOYEES e
LEFT JOIN HR.DEPARTMENTS d
    ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN HR.JOBS j
    ON e.JOB_ID = j.JOB_ID
GROUP BY
    d.DEPARTMENT_NAME,
    j.JOB_TITLE
ORDER BY
    d.DEPARTMENT_NAME,
    j.JOB_TITLE;
```

---

## 9. Explicação dos Campos da Query 01

| Campo                       | Descrição                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `departamento`            | Nome do departamento do funcionário.                                       |
| `cargo`                   | Nome do cargo ocupado pelo funcionário.                                    |
| `quantidade_funcionarios` | Quantidade de funcionários naquele departamento e cargo.                   |
| `menor_salario`           | Menor salário de referência cadastrado para o cargo na tabela`HR.JOBS`. |
| `maior_salario`           | Maior salário de referência cadastrado para o cargo na tabela`HR.JOBS`. |

---

## 10. Observação Técnica sobre Salário

Na `query_01.sql`, os campos utilizados para menor e maior salário são:

```sql
MIN(j.MIN_SALARY)
MAX(j.MAX_SALARY)
```

Esses campos vêm da tabela `HR.JOBS` e representam a **faixa salarial cadastrada para o cargo**, não necessariamente o salário real recebido por cada funcionário.

Para analisar o salário real dos funcionários, o ideal seria utilizar o campo:

```sql
e.SALARY
```

Uma versão complementar da análise poderia incluir:

```sql
MIN(e.SALARY) AS menor_salario_real,
MAX(e.SALARY) AS maior_salario_real,
ROUND(AVG(e.SALARY), 2) AS salario_medio_real
```

---

## 11. Leitura Gerencial da Query 01

A consulta permite entender como os funcionários estão distribuídos entre departamentos e cargos, além de apresentar a faixa salarial prevista para cada cargo.

Essa análise pode apoiar decisões relacionadas a:

- estrutura organizacional;
- distribuição de cargos;
- concentração de funcionários por área;
- comparação entre faixas salariais de diferentes cargos;
- avaliação inicial da composição salarial por departamento.

---

# Query 02 — Funcionários por Região com Informações de Localização

## 12. Pergunta de Negócio

**Como os funcionários estão distribuídos por região, considerando informações de localização, departamento e cargo?**

A segunda consulta foi desenvolvida para analisar os funcionários por região, trazendo informações detalhadas de localização e dados individuais dos empregados.

---

## 13. Objetivo da Query 02

A `query_02.sql` tem como objetivo listar os funcionários com suas respectivas informações de:

- ID do empregado;
- nome do funcionário;
- região;
- país;
- cidade;
- departamento;
- cargo;
- salário;
- quantidade de funcionários no mesmo agrupamento de região, país, cidade, departamento e cargo.

Além disso, a consulta aplica um filtro com `WHERE` para considerar apenas funcionários com salário maior que `1000` e menor que `3000`.

---

## 14. Tabelas Utilizadas na Query 02

A consulta utiliza todas as tabelas solicitadas no escopo do projeto:

### `HR.EMPLOYEES`

Tabela principal da análise.

Campos utilizados:

- `EMPLOYEE_ID`
- `FIRST_NAME`
- `LAST_NAME`
- `DEPARTMENT_ID`
- `JOB_ID`
- `SALARY`

### `HR.DEPARTMENTS`

Tabela usada para buscar o nome do departamento e conectar o departamento à localização.

Campos utilizados:

- `DEPARTMENT_ID`
- `DEPARTMENT_NAME`
- `LOCATION_ID`

### `HR.JOBS`

Tabela usada para buscar o nome do cargo.

Campo utilizado:

- `JOB_TITLE`

### `HR.LOCATIONS`

Tabela usada para buscar a cidade e conectar a localização ao país.

Campos utilizados:

- `LOCATION_ID`
- `CITY`
- `COUNTRY_ID`

### `HR.COUNTRIES`

Tabela usada para buscar o país e conectar o país à região.

Campos utilizados:

- `COUNTRY_ID`
- `COUNTRY_NAME`
- `REGION_ID`

### `HR.REGIONS`

Tabela usada para buscar o nome da região.

Campo utilizado:

- `REGION_NAME`

---

## 15. Processo Realizado na Query 02

A consulta realiza os seguintes passos:

1. Cria uma CTE chamada `RESULTADO_FUNCIONARIOS`.
2. Dentro da CTE, coleta as informações dos funcionários.
3. Relaciona os funcionários com departamentos, cargos, localizações, países e regiões.
4. Aplica um filtro com `WHERE` para trazer apenas funcionários com salário maior que `1000` e menor que `3000`.
5. No `SELECT` final, exibe as informações individuais dos funcionários.
6. Utiliza uma função de janela para calcular a quantidade de funcionários por grupo, sem perder o detalhe individual de cada funcionário.
7. Ordena o resultado por região, país, cidade, departamento, cargo e nome do funcionário.

---

## 16. Código da Query 02

```sql
-- COLETANDO AS INFORMAÇÕES DAS TABELAS EMPLOYEES, DEPARTMENTS, JOBS,
-- LOCATIONS, COUNTRIES E REGIONS E APLICANDO UM FILTRO DE SALÁRIOS
-- MAIOR QUE 1000 E MENOR QUE 3000

WITH RESULTADO_FUNCIONARIOS AS (
    SELECT
        E.EMPLOYEE_ID     AS ID_EMPREGADO,
        E.FIRST_NAME||' '|| E.LAST_NAME    AS NOME_FUNCIONARIO,
        R.REGION_NAME     AS REGIAO,
        C.COUNTRY_NAME    AS PAIS,
        L.CITY            AS CIDADE,
        D.DEPARTMENT_NAME AS DEPARTAMENTO,
        J.JOB_TITLE       AS CARGO,
        E.SALARY          AS SALARIO
    FROM
        HR.EMPLOYEES   E
        LEFT JOIN HR.DEPARTMENTS D ON E.DEPARTMENT_ID = D.DEPARTMENT_ID
        LEFT JOIN HR.JOBS        J ON E.JOB_ID = J.JOB_ID
        LEFT JOIN HR.LOCATIONS   L ON D.LOCATION_ID = L.LOCATION_ID
        LEFT JOIN HR.COUNTRIES   C ON L.COUNTRY_ID = C.COUNTRY_ID
        LEFT JOIN HR.REGIONS     R ON C.REGION_ID = R.REGION_ID
    WHERE
            E.SALARY > 1000
        AND E.SALARY < 3000
)
SELECT
    ID_EMPREGADO,
    NOME_FUNCIONARIO,
    REGIAO,
    PAIS,
    CIDADE,
    DEPARTAMENTO,
    CARGO,
    SALARIO,
    COUNT(ID_EMPREGADO)
    OVER(PARTITION BY REGIAO, PAIS, CIDADE, DEPARTAMENTO, CARGO) AS QUANTIDADE_FUNCIONARIOS
FROM
    RESULTADO_FUNCIONARIOS
ORDER BY
    REGIAO,
    PAIS,
    CIDADE,
    DEPARTAMENTO,
    CARGO,
    NOME_FUNCIONARIO;
```

---

## 17. Explicação da CTE

A CTE `RESULTADO_FUNCIONARIOS` funciona como uma consulta intermediária. Ela organiza os dados antes do `SELECT` final.

Essa estrutura melhora a legibilidade da consulta, pois separa a etapa de coleta e relacionamento das tabelas da etapa final de apresentação dos dados.

Trecho principal:

```sql
WITH RESULTADO_FUNCIONARIOS AS (
    SELECT
        ...
    FROM HR.EMPLOYEES E
    ...
)
```

---

## 18. Explicação do Filtro WHERE

A consulta aplica o seguinte filtro:

```sql
WHERE
        E.SALARY > 1000
    AND E.SALARY < 3000
```

Esse filtro seleciona apenas funcionários cuja remuneração está acima de `1000` e abaixo de `3000`.

Como as duas condições estão ligadas por `AND`, o funcionário precisa atender às duas regras ao mesmo tempo.

Também seria possível escrever a mesma lógica com `BETWEEN`, porém a regra atual é exclusiva, ou seja, não inclui exatamente `1000` nem exatamente `3000`.

---

## 19. Explicação da Função de Janela

A query utiliza a função:

```sql
COUNT(ID_EMPREGADO)
OVER(PARTITION BY REGIAO, PAIS, CIDADE, DEPARTAMENTO, CARGO)
```

Essa função calcula a quantidade de funcionários dentro do mesmo agrupamento de:

- região;
- país;
- cidade;
- departamento;
- cargo.

A vantagem dessa abordagem é que ela mantém o detalhe individual do funcionário, exibindo `ID_EMPREGADO` e `NOME_FUNCIONARIO`, e ao mesmo tempo apresenta a quantidade de funcionários no grupo ao qual ele pertence.

---

## 20. Explicação dos Campos da Query 02

| Campo                       | Descrição                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| `ID_EMPREGADO`            | Código identificador do funcionário.                                                      |
| `NOME_FUNCIONARIO`        | Nome completo do funcionário, formado por primeiro nome e sobrenome.                       |
| `REGIAO`                  | Região onde o funcionário está localizado.                                               |
| `PAIS`                    | País vinculado à localização do departamento.                                           |
| `CIDADE`                  | Cidade vinculada ao departamento do funcionário.                                           |
| `DEPARTAMENTO`            | Departamento onde o funcionário está alocado.                                             |
| `CARGO`                   | Cargo ocupado pelo funcionário.                                                            |
| `SALARIO`                 | Salário do funcionário.                                                                   |
| `QUANTIDADE_FUNCIONARIOS` | Quantidade de funcionários no mesmo grupo de região, país, cidade, departamento e cargo. |

---

## 21. Leitura Gerencial da Query 02

A consulta permite analisar a distribuição dos funcionários por localização geográfica, considerando região, país e cidade, além de detalhar o departamento e o cargo de cada funcionário.

Essa análise pode apoiar decisões relacionadas a:

- concentração de funcionários por região;
- distribuição geográfica da força de trabalho;
- análise de cargos por localização;
- avaliação de salários por região;
- identificação de departamentos presentes em cada localidade;
- análise de grupos de funcionários com salário dentro de uma faixa específica.

---

## 22. Diferença entre as Queries

| Consulta         | Tipo de análise                          | Nível de detalhe          | Principal objetivo                                                          |
| ---------------- | ----------------------------------------- | -------------------------- | --------------------------------------------------------------------------- |
| `query_01.sql` | Salários por departamento e cargo        | Consolidado                | Entender a distribuição salarial por departamento e cargo.                |
| `query_02.sql` | Funcionários por região e localização | Detalhado por funcionário | Identificar funcionários por região, país, cidade, departamento e cargo. |

---

## 23. Exportação dos Resultados para CSV e Continuidade em Python

Após a construção e validação das consultas no FreeSQL, os resultados obtidos nas duas queries foram exportados para arquivos no formato **CSV**.

Essa exportação foi uma etapa importante do projeto, pois permite que os dados consultados no banco sejam utilizados posteriormente em uma análise mais aprofundada com **Python**.

### Arquivos gerados

| Arquivo SQL      | Resultado exportado                                            | Finalidade do CSV                                                                                                                          |
| ---------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `query_01.sql` | Distribuição de salários por departamento e cargo           | Continuar a análise salarial em Python, criando estatísticas, gráficos e possíveis comparações entre departamentos e cargos.         |
| `query_02.sql` | Funcionários por região, localização, departamento e cargo | Continuar a análise geográfica dos funcionários em Python, permitindo visualizações por região, país, cidade, departamento e cargo. |

### Motivo da exportação para CSV

A exportação para CSV facilita a integração entre o ambiente SQL e o ambiente Python. Com isso, a análise deixa de depender apenas da consulta no banco de dados e passa a permitir novas etapas, como:

- leitura dos dados com `pandas;`
- analise gráfica com `seaborn e matplotlib;`
- verificação de tipos de dados;
- tratamento de valores ausentes;
- criação de gráficos exploratórios;
- análise estatística complementar;
- preparação dos dados para dashboards ou modelos analíticos.

Exemplo de leitura dos arquivos CSV em Python:

```python
import pandas as pd

df_query_01 = pd.read_csv('query_01.csv')
df_query_02 = pd.read_csv('query_02.csv')
```

Dessa forma, o fluxo do projeto fica organizado em duas etapas principais:

1. **FreeSQL:** construção das consultas, relacionamento das tabelas e extração dos dados.
2. **Python:** continuidade da análise exploratória, geração de gráficos, tratamento dos dados e aprofundamento das perguntas de negócio.

---

## 24. Conclusão

As duas consultas desenvolvidas permitem analisar informações importantes da base `HR` no FreeSQL.

A `query_01.sql` apresenta uma visão consolidada por departamento e cargo, permitindo observar a distribuição de funcionários e faixas salariais por função.

A `query_02.sql` amplia a análise ao incluir dados geográficos, como região, país e cidade, além de trazer o detalhe individual dos funcionários. A utilização da CTE e da função de janela melhora a organização do código e permite calcular a quantidade de funcionários por grupo sem perder o nível detalhado da análise.

De forma geral, o projeto demonstra o uso de `LEFT JOIN`, `WHERE`, `GROUP BY`, `ORDER BY`, CTE e função de janela para responder perguntas de negócio relacionadas a funcionários, salários, departamentos, cargos e localização.
