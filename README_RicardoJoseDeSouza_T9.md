# Instruções de execução

**Aluno:** Ricardo José de Souza  
**Turma:** T9

Na pasta do projeto, instale as dependências e execute nesta ordem:

```powershell
python -m pip install -r requirements.txt
python importacao_dados.py
python Limpeza_dados.py
python Resumo.py
```

A limpeza gera `Base_varejo_original.csv`; o resumo lê essa saída.
Consulte `README.md` para conhecer as regras e `resultados/relatorio.txt`
para os indicadores e todas as estatísticas de filhos.
