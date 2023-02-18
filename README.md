# 100-days-of-code-data-engineer
```diff
- Caso não tenha nada nesta branch, observe es outras. (GitFlow)
```

---
<p style="color:red;">100 Dias de código relacionados aos conhecimentos de engenharia de dados.</p>

---
## Objetivo:

- Uma breve demonstração das minhas habilidades sobre as competências da área de engenharia de dados.

---
## Problema proposto:

- 1: Criar 3 aplicações que realizem streaming de dados de formato diferente. (VELOCIDADE/VARIEDADE)
    - 1.1: Essas aplicações devem ser parametrizaveis, para que possa condicionar os dados. (SIMULAR UM AMBIENTE ou INCIDENTE) 
- 2: Escalar essa aplicação horizontalmente. (VOLUME)
- 3: Avaliar os dados coletados, e comparar. (VERACIDADE)
- 4: Criar ML para previsões. (VALOR)


---
## Contexto: (Sim eu que criei!)

 Uma empresa especializada em usinagem de precisão, que tem 5 filiais, em cada filial tem 2 tipos de equipamentos de torneamento(O numero de equipamentos pode váriari). 

 Um dos equipamentos emite um relatório em JSON e outro em XML e um outro em um arquivo de texto bugado(KKKKKKKK).

 Cada máquina emite um relatório da peça construida, com algumas informações sobre a peça.

 O tempo médio de cada produção de peça é de 3s no máx 5s. (Oh as idéia!)

A empresa quer diminuir o indice de falha em peças e identificar possiveis padrões  de falhas.

---

## Estrutura do repositório:

```
root
 |----[diario_de_operacoes]     >> Informações sobre cada dia de desenvolvimento
 |----[maquinas]                >> Aplicação que simula os equipamentos
 |----[cloud_externa]           >> Cloud Externa para simular as máqiunas
 |----[engenharia_de_dados]     >> Aqui o trabalho começa de verdade
 |----[ciencia_e_analise]       >> Ciencia de Dados, e ML
 |----[pacote_de_entrega]       >> Resultado do projeto.
```
