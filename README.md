# Mini projeto de análise de dados de varejo

**Aluno:** Ricardo José de Souza  
**Turma:** T9

1. Importar dados do Kaggle: [Kaggle — Base Varejo](https://www.kaggle.com/datasets/namespaiva/base-varejo/data) 
2. Criar o ambiente virtual (venv) 
3. Instalar através do pip install: pandas openpyxl e rich 
4. Importar bibliotecas Pandas, Rich e Numpy

O projeto prepara uma base de compras de varejo e apresenta um resumo de clientes, compras, produtos e datas usando Python, pandas e Rich.

## Arquivos do projeto

| Arquivo | Descrição |
| --- | --- |
| `Base_Varejo.csv` | Base de entrada usada pela etapa de limpeza. Contém colunas vazias e registros nulos ou duplicados. |
| `Base_varejo_original.csv` | Arquivo de saída da limpeza e base lida pelo programa de importação. Apesar do nome, este arquivo é sobrescrito pela limpeza. |
| `Limpeza_dados.py` | Valida os identificadores de compra, remove colunas inteiramente vazias, linhas com valores nulos e registros duplicados; salva o resultado em `Base_varejo_original.csv`. |
| `importacao_dados.py` | Carrega `Base_varejo_original.csv` com ; como separador e converte `DATA` para datetime. |
| `Resumo.py` | Calcula e exibe o resumo da base limpa. |
| `formatacao.py` | Fornece o console Rich e a formatação numérica no padrão brasileiro. |
| `requirements.txt` | Lista as dependências Python do projeto. |

## Requisitos e instalação

É necessário ter Python instalado. No PowerShell, na pasta do projeto, crie e ative um ambiente virtual e instale as dependências:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r .\requirements.txt
```

O arquivo de dependências chama-se `requirements.txt`.

## Como executar

### Limpe a base de entrada

```powershell
python .\Limpeza_dados.py
```

O script lê `Base_Varejo.csv` e sobrescreve `Base_varejo_original.csv` com a versão limpa. Mantenha `Base_Varejo.csv` disponível na pasta do projeto.

### Gere o resumo

```powershell
python .\Resumo.py
```

O programa lê a base limpa e apresenta os resultados no terminal.

### Também é possível validar a importação isoladamente

```powershell
python .\importacao_dados.py
```

## Dados analisados

Os arquivos CSV usam ponto e vírgula (;) como separador. As colunas principais são:

| Coluna | Conteúdo |
| --- | --- |
| `DATA` | Data do registro de compra |
| `CO_ID` | Identificador da compra |
| `CL_ID` | Identificador do cliente |
| `CL_GENERO` | Gênero informado do cliente |
| `CL_EC` | Código do estado civil |
| `CL_FHL` | Quantidade de filhos informada |
| `CL_SEG` | Segmento do cliente |
| `PR_ID` | Identificador/SKU do produto |
| `PR_CAT` | Categoria do produto |
| `PR_NOME` | Nome do produto |

No resumo, os códigos de `CL_EC` são tratados assim: 1 casado(a), 2 divorciado(a), 3 separado(a), 4 solteiro(a) e 5 viúvo(a).

## Indicadores do resumo

O `Resumo.py` apresenta:

- datas com mais registros de compra, incluindo empates;
- total de registros, compras distintas (`CO_ID`) e clientes distintos (`CL_ID`);
- clientes únicos por gênero, estado civil e segmento;
- média de filhos considerando o registro mais recente de cada cliente;
- categoria mais frequente, incluindo empates;
- produto mais frequente, contando registros por combinação de SKU (`PR_ID`) e nome (`PR_NOME`), com o nome, o SKU e a quantidade.

Como cada linha da base representa um item registrado, a contagem por data e a quantidade exibida para o produto mais frequente são contagens de linhas, não necessariamente de compras (`CO_ID`) distintas.

## Insights da análise

Os resultados abaixo foram calculados com a base limpa `Base_varejo_original.csv`:

- O segmento B concentra a maioria dos clientes: são 645 de 1.000 clientes (64,5%). Os segmentos C e A têm 271 (27,1%) e 84 (8,4%), respectivamente.
- Alimentos é a categoria predominante: 384.197 dos 733.447 registros de itens (aproximadamente 52,4%) pertencem a essa categoria.
- O produto com mais registros é Papinha Infantil: o SKU 51 aparece 3.322 vezes. Essa quantidade representa linhas de itens no arquivo, não compras distintas.
- A distribuição por gênero é relativamente equilibrada: 519 clientes (51,9%) são identificados como mulheres e 481 (48,1%) como homens.
- A média de filhos é de aproximadamente 1,14 por cliente: o cálculo usa o registro mais recente de cada um dos 1.000 clientes.

## Reflexão teórica: ETL e qualidade de dados

ETL é o processo de Extração, Transformação e Carga de dados. Ele organiza a passagem dos dados de sua origem até uma forma adequada para análise. Neste projeto, essas etapas aparecem da seguinte maneira:

- Extração (Extract): os dados são obtidos da base de varejo disponibilizada no Kaggle e lidos a partir do arquivo `Base_Varejo.csv`.
- Transformação (Transform): a rotina de limpeza valida que `CO_ID` seja numérico, inteiro e positivo, e que cada identificador corresponda a um único cliente e uma única data. Também remove colunas totalmente vazias, registros com valores nulos e linhas duplicadas. Na importação, `DATA` é convertida do formato dd/mm/aaaa para datetime.
- Carga (Load): os dados transformados são gravados em `Base_varejo_original.csv`, que depois é carregado por `importacao_dados.py` para gerar os indicadores apresentados por `Resumo.py`.

A limpeza contribui para a qualidade dos dados ao remover campos sem informação, evitar que linhas incompletas participem dos cálculos e reduzir a contagem repetida de registros idênticos. Essas ações melhoram aspectos como completude e unicidade da base usada na análise. Porém, qualidade não significa apenas remover dados: é necessário considerar se cada alteração preserva a informação relevante para o objetivo do estudo.

Por exemplo, `dropna()` remove uma linha se qualquer uma de suas colunas tiver valor ausente. Isso pode excluir registros que ainda seriam úteis para algumas métricas e, se os valores ausentes não ocorrerem ao acaso, pode enviesar os resultados. Da mesma forma, a remoção de duplicatas deve considerar o que caracteriza um registro repetido; duas linhas iguais podem ser uma duplicação indevida ou representar eventos legítimos, dependendo da origem dos dados. Por isso, é importante registrar quantas linhas foram removidas, avaliar a regra aplicada e, quando possível, manter uma cópia intacta dos dados de origem.

Neste projeto, a rotina exibe um relatório com os registros iniciais, removidos e finais, o que permite acompanhar o efeito da transformação. Ainda assim, a limpeza não comprova que todos os valores restantes estejam corretos ou consistentes com a realidade; essas dimensões exigiriam validações adicionais, como verificar formatos de data, códigos permitidos e relações entre identificadores. A análise depende, portanto, tanto do código quanto da compreensão da base e das decisões tomadas durante o tratamento.
