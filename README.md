# 🎓 Previsão de Preços de Cursos da Udemy

Este projeto tem como objetivo analisar cursos da Udemy e utilizar *Machine Learning* para tentar prever o preço de um curso com base em algumas de suas características.

O projeto utiliza *Python, **Pandas, **Scikit-learn, **Numpy, **Matplotlib* e *Flask*.

---

## 🛠️ Ferramentas utilizadas

| Ferramenta | Utilização |
|:---:|---|
| 🐼 *Pandas* | Leitura e organização dos dados |
| 🤖 *Scikit-learn* | Treinamento e avaliação dos modelos |
| 📊 *Matplotlib* | Criação dos gráficos |
| 📊 *Numpy* | Suporte a operações numéricas e arrays |
| 🌐 *Flask* | Desenvolvimento do site |

---

## 📁 Sobre os dados

O dataset utilizado contém informações sobre cursos da Udemy.

Inicialmente, foram encontrados *3.678 cursos. Após a limpeza dos dados e a remoção de cursos duplicados, ficaram **3.672 cursos*.

Como o objetivo do projeto é prever preços, foram utilizados apenas os cursos pagos.

| Informação | Quantidade |
|---|---:|
| Total de cursos originais | 3.678 |
| Cursos após a limpeza | 3.672 |
| Cursos pagos | *3.362* |
| Cursos gratuitos | 310 |

Os cursos pagos possuem preços entre *US$ 20 e US$ 200, com uma média de aproximadamente **US$ 72*.

---

## 🧹 Limpeza dos dados

Durante a preparação dos dados, foram realizadas algumas verificações:

- Remoção de cursos duplicados;
- Verificação de informações importantes, como ID, título e preço;
- Remoção de valores negativos;
- Organização das datas de publicação.

Após essa etapa, os dados ficaram prontos para a análise e o treinamento dos modelos.

---

## 📊 Análise dos dados

O projeto apresenta três gráficos para ajudar na análise dos cursos e dos resultados do modelo.

### 1️⃣ Relação das características com o preço

Foi analisada a relação entre algumas características dos cursos e seus preços.

| Característica | Relação com o preço |
|---|---:|
| Quantidade de aulas | 0,33 |
| Duração do curso | 0,29 |
| Número de avaliações | 0,11 |
| Número de inscritos | 0,05 |

A quantidade de aulas e a duração foram as características que apresentaram uma relação maior com o preço.

Mesmo assim, essa relação não é muito forte, mostrando que o preço de um curso também depende de outros fatores.

---

### 2️⃣ Características utilizadas no modelo

Para realizar as previsões, foram utilizadas as seguintes informações:

| Característica | Descrição |
|---|---|
| ⏱️ Duração | Tempo total do curso |
| 📚 Número de aulas | Quantidade de aulas disponíveis |
| 📈 Nível | Nível de dificuldade do curso |
| 🖥️ Assunto | Área do curso |

Como algumas informações eram textos, como o nível e o assunto, elas foram transformadas em valores que os modelos conseguem utilizar.

---

### 3️⃣ Comparação entre preço real e previsto

O último gráfico compara o preço real dos cursos com o preço previsto pelo modelo.

Quanto mais próximo o valor previsto estiver do valor real, melhor é a previsão.

Os resultados mostraram que o modelo consegue identificar alguns padrões, mas ainda apresenta dificuldades para prever corretamente cursos muito baratos ou muito caros.

---

## 🤖 Modelos utilizados

Foram utilizados dois modelos para comparar os resultados.

| Modelo | Descrição |
|---|---|
| *Regressão Linear* | Procura encontrar uma relação entre as características do curso e o seu preço |
| *Árvore de Decisão* | Divide os dados em grupos com características semelhantes para realizar as previsões |

---

## 🧪 Treinamento e testes

Os dados foram divididos da seguinte forma:

| Utilização | Porcentagem | Quantidade aproximada |
|---|---:|---:|
| 🧠 Treinamento | 80% | 2.689 cursos |
| 📝 Teste | 20% | 673 cursos |

Os dados de teste não são utilizados durante o treinamento. Dessa forma, é possível verificar como o modelo se comporta com cursos que ele ainda não conhece.

---

## 📏 Avaliação dos modelos

Para avaliar os resultados, foi utilizado o *MAE (Erro Absoluto Médio)*.

Essa métrica mostra, em média, quantos dólares o modelo errou ao tentar prever o preço de um curso. Quanto menor o valor, melhor é o resultado.

| Modelo | Erro no teste |
|---|---:|
| 🥇 *Regressão Linear* | *US$ 43,28* |
| 🌳 Árvore de Decisão | US$ 52,70 |
| 📌 Previsão pela média | US$ 48,61 |

---

## 🏆 Melhor modelo

A *Regressão Linear* apresentou o melhor resultado, pois teve o menor erro médio nos dados de teste.

A Árvore de Decisão teve um resultado muito bom durante o treinamento, mas apresentou mais erros nos cursos novos. Isso indica que ela pode ter se adaptado demais aos dados utilizados durante o treinamento.

Por esse motivo, a *Regressão Linear foi escolhida como o melhor modelo para este projeto*.

---

## 🌐 Site em Flask

Além da análise dos dados, o projeto possui um site desenvolvido com *Flask*.

No site, é possível:

- 📂 Enviar e visualizar os dados;
- 📊 Visualizar os gráficos da análise;
- 🤖 Consultar os resultados dos modelos;
- 💰 Testar a previsão do preço de um curso.

Para realizar uma previsão, o usuário informa:

| Informação |
|---|
| Duração do curso |
| Número de aulas |
| Nível do curso |
| Assunto do curso |

Com essas informações, o modelo realiza uma estimativa do preço.

---

## ⚠️ Limitações do projeto

Apesar dos resultados, existem algumas limitações:

- O modelo ainda apresenta um erro médio considerável;
- O preço de um curso pode depender de informações que não estão presentes no dataset;
- Características como a reputação do instrutor e promoções podem influenciar no preço;
- Os resultados podem mudar dependendo dos dados utilizados para treinamento e teste.

---

## 📌 Conclusão

O projeto permitiu realizar todas as etapas principais de uma análise de dados utilizando Machine Learning, desde a limpeza e análise dos dados até o treinamento e comparação dos modelos.

Entre os modelos testados, a *Regressão Linear apresentou o melhor resultado*. Mesmo com algumas limitações, o projeto mostrou como características de um curso podem ser utilizadas para realizar uma estimativa de seu preço.

---

## 👥 Desenvolvido por

*Gustavo Zavatti*  
*Pedro Serra*  
*Fabricio Milano*

Projeto desenvolvido como parte das atividades do curso de *Ciência da Computação*.