# 📘 Tecnologias Inteligentes Aplicadas à Saúde


## 🗒️ Anotações de Aula

### 01/09/26
Aula sobre PYCARET 
  Não é compativel com a versao mais atual do python. Utilizar ate a versão 2025/07 no google colab.
  Pycatrt particiona em dois grupos, seperando as amostrar que tem somente uma unica unidade das demais, ficando somente com amostrar com 2 ou mais.

  Acuracia x F1 score
   amostra -> treinamento -> teste e treinamento -> acuracia e f1 score

Metrica F1 score, junção da precisao com o recall, considerada a ideal.

Utilização do docker para rodar o PYCARET
  criar um dockerfile 
    colocar a versao do python
    pycaret e jupter 


Realizar a atividade, no github para apresentar para o professor dia 15/09.
da para utilizar o modelo feito em aula 5_comparativo_modelos mudar somente as fetures e a base de dados. pode utilizar o pycaret.  tias/3_predicao_previsao_codigos_exemplos
/5_comparativo_modelos.py
Link da aula sobre PYCARET:
https://github.com/b3rnard0p/ConhecimentoTeorico/tree/main/PyCaret
---
### 28/08/26

O que essas metricas analisam, explicar cada uma delas.

  Accuracy_score :

  classificarion_report:

  confusion_matrix:

  f1_score:


Escala likert 0 a 5, pois alguns algoritmos não conseguem ler palavras como "Abaixo" "normal" aí é utilizado a escala Likert, Deixar a coluna com os dados padrões e adicionar outra com a escala Likert.


Normalizador/normazitador, retirar o padrão que tem somente uma classifcação da lista Likert tipo 1,1,1,1,1 ou 5,5,5,5,5. 

vicio de uma tabela OverFiting 

---
### 18/08/26
  Podemos utilizar modelos treinados ou modelos matematicos para reconhecimento ( predicao previsao) de padroes 

Modelos treinados 
  -amostra 
      -> conjuntos      
        1 lista  [] dicionario lista
        2 tupla { } dicinario de tupla

      ->entrada   [n] -> atributos, caracteristicas propriedades
          X       [n]
        feature   [n] -> Resultado BINÁRIO

  classificar ou categorizar ou etiquetar
---
### 11/08/26
Fases de predição
  1- Entender o problema
  2- Fonte de Dados/amostras para treinar
  3- ETL - Limpeza dos dados => Pandas
  4- Aplicar diferentes modelos para identificar o adequado 
  
Utilizamos o Google Colab para realização da atividade


predição: classificação categorização etiquetação referente aos modelos 
Previsão: series temporais => tempo continuo => projeção
    -mineração - KDD

---
### 04/08/26

 Saúde: 

Diagnóstico 
  - reconhecer padrões -> volume de dados -> algoritmos de aprendizado de máquina 

Monitoramento ou Sensoreamento e Atuação 
    - automação 

Predição e Previsão 
  - reconhecer padrões -> volume de dados -> algoritmos de mineração 

 
redes neurais -> aprendizagem => reconhecer padroes  
RNA p 
ML 
MD mineração dados  
Sistema multiagentes => automação  

 ---
