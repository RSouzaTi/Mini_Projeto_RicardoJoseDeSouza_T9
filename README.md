# Análise exploratória de dados de varejo

**Aluno:** Ricardo José de Souza  
**Turma:** T9  
**Tecnologias utilizadas:** Python, pandas e Rich

## Sobre o projeto

Este mini projeto aplica conceitos de análise exploratória a uma base de varejo. O trabalho foi organizado em módulos para leitura dos arquivos, limpeza dos dados, cálculo de indicadores e apresentação dos resultados no terminal.

O objetivo é compreender a estrutura da base, observar o efeito do tratamento de valores ausentes e duplicatas e identificar padrões entre clientes, categorias e produtos.

**Fonte dos dados:** [Base Varejo no Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data).

## Estrutura do repositório

| Arquivo | Finalidade |
| --- | --- |
| `Base_Varejo.csv` | Base de entrada disponível no repositório. |
| `Base_varejo_original.csv` | Arquivo de saída da limpeza. Apesar do nome, recebe os dados tratados e é sobrescrito a cada execução dessa etapa. |
| `importacao_dados.py` | Define os caminhos e lê a base de entrada com pandas. |
| `Limpeza_dados.py` | Remove colunas totalmente vazias, linhas com valores ausentes e linhas duplicadas; exibe as contagens antes e depois da limpeza e salva o resultado. |
| `Resumo.py` | Calcula os indicadores e exibe um painel no terminal. |
| `formatacao.py` | Disponibiliza o console Rich e uma função de formatação numérica no padrão brasileiro. |
| `requirements.txt` | Declara a dependência do pandas. O Rich precisa ser instalado separadamente no estado atual do projeto. |
| `README_RicardoJoseDeSouza_T9.md` | Contém instruções complementares de execução. |

## Preparação do ambiente

Na pasta do projeto, abra o terminal do PowerShell e execute:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install rich
```

O pandas realiza a leitura e a manipulação dos dados. O Rich organiza a apresentação dos indicadores no terminal. Os scripts atuais não exigem importação direta de NumPy nem instalação de openpyxl, pois trabalham com arquivos CSV.

## Execução

Execute os comandos a partir da pasta do projeto.

### 1. Conferir a leitura da base

```powershell
python .\importacao_dados.py
```

Essa etapa informa o número de registros carregados e mostra as cinco primeiras linhas.

### 2. Executar a limpeza

```powershell
python .\Limpeza_dados.py
```

A rotina aplica as seguintes operações, nesta ordem:

1. Remove colunas em que todos os valores são ausentes.
2. Remove linhas que tenham pelo menos um valor ausente nas colunas restantes.
3. Remove linhas inteiramente duplicadas e reorganiza o índice.
4. Exibe a quantidade de registros iniciais, removidos e finais.
5. Salva a tabela tratada em `Base_varejo_original.csv`, usando ponto e vírgula como separador.

### 3. Apresentar o resumo

```powershell
python .\Resumo.py
```

O programa calcula os indicadores e apresenta um painel com Rich.

**Fluxo atual:** a função `importar_dados()` lê a base de entrada indicada em `CAMINHO_CSV`. Portanto, executar a limpeza não faz o resumo passar automaticamente a usar `Base_varejo_original.csv`. Essa ligação entre as etapas ainda precisa ser ajustada no código para que o resumo represente a saída da limpeza.

### Compatibilidade dos nomes de arquivos

Os imports dos scripts usam `Importacao_dados` e `Formatacao`, enquanto os arquivos publicados se chamam `importacao_dados.py` e `formatacao.py`. O caminho da base no código também usa `Base_varejo.csv`, enquanto o repositório contém `Base_Varejo.csv`.

Essas diferenças podem impedir a execução em sistemas que distinguem letras maiúsculas de minúsculas. Os nomes nos imports e nos caminhos precisam corresponder exatamente aos arquivos publicados.

## Dados analisados

Os arquivos CSV usam ponto e vírgula (`;`) como separador.

| Coluna | Significado |
| --- | --- |
| `DATA` | Data do registro de compra |
| `CO_ID` | Identificador da compra |
| `CL_ID` | Identificador do cliente |
| `CL_GENERO` | Gênero informado do cliente |
| `CL_EC` | Código do estado civil |
| `CL_FHL` | Quantidade de filhos informada |
| `CL_SEG` | Segmento do cliente |
| `PR_ID` | Identificador do produto ou SKU |
| `PR_CAT` | Categoria do produto |
| `PR_NOME` | Nome do produto |

O resumo interpreta os códigos de estado civil como: 1 para casado(a), 2 para divorciado(a), 3 para separado(a), 4 para solteiro(a) e 5 para viúvo(a). Esse mapeamento está definido no código e deve ser confirmado com o dicionário da base.

## Indicadores calculados

O módulo `Resumo.py` calcula:

- Datas com maior número de registros, incluindo empates.
- Total de registros, compras distintas e clientes distintos.
- Clientes únicos por gênero, estado civil e segmento.
- Média de filhos, considerando o registro mais recente de cada cliente.
- Categorias mais frequentes, incluindo empates.
- Produtos mais frequentes, agrupados pela combinação de SKU e nome.

Para selecionar o registro mais recente de cada cliente, o resumo converte temporariamente `DATA` com `pd.to_datetime(..., dayfirst=True)`, ordena os registros e mantém o último por `CL_ID`. A função de importação não converte a coluna de data.

**Interpretação das contagens:** uma compra pode aparecer em várias linhas por conter diferentes produtos. Assim, contar linhas por data ou produto não equivale a contar compras distintas. Embora o painel use as expressões “mais compras” e “unidades” em alguns rótulos, esses indicadores são contagens de registros.

A base não contém preços nem uma coluna explícita de quantidade. Portanto, o projeto não calcula faturamento ou volume físico vendido.

## Resultados registrados na análise

Os valores abaixo foram registrados anteriormente para a base tratada. Para reproduzi-los pelo comando de resumo, é necessário garantir que ele leia a mesma versão da base limpa.

1. **O segmento B reúne a maior parcela dos clientes:** 645 de 1.000 clientes (64,5%). Os segmentos C e A representam 271 (27,1%) e 84 (8,4%), respectivamente.
2. **Alimentos é a categoria mais frequente:** 384.197 dos 733.447 registros de itens, aproximadamente 52,4%.
3. **Papinha Infantil é o produto com mais registros:** o SKU 51 aparece 3.322 vezes. Esse total representa ocorrências no arquivo.
4. **A distribuição de clientes por gênero é próxima:** 519 clientes possuem código F (51,9%) e 481 possuem código M (48,1%).
5. **A média de filhos é de aproximadamente 1,14 por cliente**, considerando o registro mais recente de cada cliente. No painel atual, a função de formatação usa zero casas decimais por padrão, o que arredonda a média exibida.

## Reflexão sobre ETL e qualidade dos dados

ETL significa **Extração, Transformação e Carga**. Neste projeto, a extração corresponde à leitura do CSV com pandas; a transformação remove colunas vazias, registros incompletos e duplicatas; e a carga grava a tabela tratada em outro arquivo CSV.

Separar essas etapas facilita a compreensão do processo e permite acompanhar quantos registros foram removidos. Entretanto, uma base com menos nulos e duplicatas não está necessariamente correta em todos os aspectos.

A remoção de nulos com `dropna()` foi a estratégia adotada no código. Ela simplifica a análise, mas pode descartar registros úteis e introduzir viés quando a ausência de informação está relacionada ao perfil dos clientes ou das compras. Uma evolução do projeto seria avaliar cada coluna antes de decidir entre excluir, preencher ou preservar valores ausentes.

A remoção de linhas idênticas também exige uma hipótese: elas são tratadas como duplicações indevidas. Sem um identificador do item ou uma coluna de quantidade, duas linhas iguais podem representar ocorrências legítimas. Por isso, essa decisão precisa ser validada com a origem dos dados.

O arquivo de entrada deve ser preservado. Já `Base_varejo_original.csv`, apesar do nome, é uma saída de processamento e não deve ser tratado como uma cópia original imutável.

## Limitações e próximos ajustes

- Conectar o resumo à base limpa e padronizar maiúsculas e minúsculas nos nomes dos arquivos, imports e caminhos.
- Incluir Rich no `requirements.txt` e ajustar a exibição da média para duas casas decimais.
- Acrescentar validações de identificadores de compra e sua relação com clientes e datas. Essas verificações ainda não são realizadas pela classe de limpeza.
- Completar as estatísticas de filhos com mediana, moda, desvio padrão, mínimo, máximo, contagem e quartis.
- Avaliar categorias vazias, datas inválidas e valores ausentes por coluna antes da exclusão.
- Conferir novamente os indicadores depois de integrar as etapas, registrando qual versão da base foi utilizada.
