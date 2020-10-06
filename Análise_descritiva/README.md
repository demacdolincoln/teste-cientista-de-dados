o  dataset é bem plural em relação a diversidade de dados, desde séries temporais a textos realmente muito interessantes para NLP. Pensando em duas frentes principais: uma análise mais quantitativa/estatística com base em informações objetivas como categorias, dados nutricionais e data de publicação e outra frente mais voltada para NLP utilizando informações dos textos das receitas, descrição, ingredientes, etc.

## 1. A Questão das séries temporais

({ver notebook})[https://github.com/demacdolincoln/teste-cientista-de-dados/blob/master/An%C3%A1lise_descritiva/Regress%C3%A3o.ipynb]

Trabalhar com dados implica necessariamente numa atualização periódica dos modelos treinados, isso ocorre porque no mundo real tudo sempre está em transformação, desse modo temos 2 alternativas: tornar o aprendizado dos algoritmos contínuo ou medir a qualidade dos resultados em relação a blocos de dados separados em função do tempo para entender até onde estar defasado realmente prejudica os resultados.

No caso de receitas, estamos lidando com hábitos alimentares que variam tanto ao longo dos anos quanto ao longo de meses, muito especialmente pelas estações do ano e datas comemorativas, além de períodos de safra e diversos outros fatores que tendem a ser cíclicos e que fogem ao dataset em questão. Por isso vou me ater à questão das séries temporais e em como o algoritmo tende a ficar defasado ao longo do tempo.

Primeiro imaginei que seria possível relacionar de alguma forma a quantidade de gorduras, sódio, proteínas e calorias com as categorias relacionadas às receitas, mas estou enganado e/ou o treinamento prejudicou essa correlação já que o SciKit Learn tem poucos algoritmos com suporte a multi target e random forest não é muito próprio para lidar com NLP em compração com algoritmos como o LSTM mas por motivo de força maior não pude implementar com o pytorch ou tensorflow, devido a baixíssima correlação, dispensei como features.

{isso pode ser melhor compreendido observando o notebook neste [commit](https://github.com/demacdolincoln/teste-cientista-de-dados/blob/9deaf0ed030bd955243be299e1c016f65f118500/An%C3%A1lise_descritiva/Regress%C3%A3o.ipynb)}

Desde o início o objetivo não é fazer uma regressão com grande assertividade mas que mostrasse a defasagem do treinamento ao longo do tempo, utilizando apenas calorias, gorduras, e proteínas para estimar a quantidade de sódio, resolvi não fazer a previsão da quantidade de calorias ou gorduras porque essas duas são muito bem correlacionadas, além dos motivos óbvios o primeiro heatmap do notebook em que a regressão foi construída evidencia isso.


## 2. Por que preferir o texto das receitas e não os ingredientes ou descrição ou até mesmo as categorias?

Porque só o passo a passo da receita explica diretamente a receita e pode fazer referências ao seu contexto sem o viés consciente do usuário, bem diferente da descrição que pode dizer apenas que é um prato delicioso e das categorias, que tem como valor mais frequente algo que não diz nada "Bon apetit".

A utilidade vai bem além do simples sistema de recomendação (a representação dos dados em si já constitui um sistema de recomendação, faltando apenas implementar a similaridade de cossenos). representar os dados espacialmente significa poder encontrar padrões fora das categorias determinadas explicitamente.

Para isso primeiro é preciso seguir algumas etapas:

1. vetorização do vocabulário - neste caso eu preferiria usar o fasttext do que até mesmo o BERT, o motivo disso é que o fasttext é treinado com "sub"palavras, o que é bem adequado para contextos em que a escrita não é toda certinha, sendo mais tolerante para erros de digitação, palavras incompletas e até palavras fora do vocabulário. É inegável a perda de qualidade na representação semântica em relação a outros métodos, porém a tolerância se torna um fator bastante relevante para esse contexto, completamente diferente do que seria num contexto voltado para reportagens ou produção acadêmica por exemplo.

![](https://imgur.com/a/y55449W.png)

_^--  visualização do treinamento com o fasttext com o gensim --^_

2. aprendizado auto-supervisionado - similar a uma classificação mas sem o objetivo de classificar, apenas aprender um padrão, nesse caso poderia usar as categorias ou um conjunto de dados que nesse ponto seriam tabulares: calorias, gorduras, sódio, proteínas e avaliação. Para esta etapa seria bem mais simples implementar usando alguma framework voltada para deep learning como o pytorch ou keras, a rede neural teria pelo menos uma camada recorrent ou de atenção, e algumas camadas lineares, sendo que após o treinamento, habitualmente se usa a saída da penúltima camada para fazer essa representação espacial, mas dependendo da quantidade de camadas de saída (no caso das categorias, mais de 600), a saída da última camada pode ser o suficiente.*

O alto custo computacional aqui foi um problema que tornou a conclusão inviável, utilizando os dados completos, cada época no treinamento demoraria mais de 6 horas, reduzi a quantidade dedos e cada época ainda passou a demorar aproximadamente 2 horas usando a GPU do google colab, a implementação pode ser vista neste [link](https://colab.research.google.com/drive/1a3APFg5LcPsSwtkXMaFhMY3K5tu7YV6-?usp=sharing)

De forma geral o grande problema da aplicabilidade de deep learning no mundo real é o elevado custo computacional, mesmo que existam formas de mitigar grande parte dos problemas de desempenho (analisando um histograma das camadas para saber quais não estão sendo treinadas e portanto podemos considerar como descartáveis, métodos de seleção de hiperparâmetros que vão desde o tamanho das camadas até a escolha do tamanho de float), ainda há barreiras mesmo para testes aparentemente simples.

---

* Uma boa postagem sobre o assunto: [Self-supervised learning and computer vision](https://www.fast.ai/2020/01/13/self_supervised/)
