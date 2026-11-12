from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

from modelo import preparar_dados, codificar_dados

def treinar(df):

    # Isola as variáveis independentes (X) e a variável alvo de previsão (y)
    X, y = preparar_dados(df)

    # Garante que há dados suficientes para treinar a inteligência artificial
    if len(X) < 2:
        raise ValueError("Dados insuficientes para treinamento.")

    # Divide os dados em proporção padrão: 80% para a máquina aprender e 20% para testar
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Converte variáveis categóricas de texto em colunas numéricas que o algoritmo consegue ler
    X_train, X_test = codificar_dados(
        X_train,
        X_test
    )

    # Inicializa, treina e testa o primeiro modelo (Regressão Linear)
    modelo_linear = LinearRegression()

    modelo_linear.fit(X_train, y_train)

    previsao_linear = modelo_linear.predict(X_test)

    # Calcula a média de erro do modelo em dólares (Erro Absoluto Médio - MAE)
    mae_linear = mean_absolute_error(
        y_test,
        previsao_linear
    )

    # Inicializa, treina e testa o segundo modelo (Árvore de Decisão) para fins de comparação
    modelo_arvore = DecisionTreeRegressor(
        random_state=42
    )

    modelo_arvore.fit(X_train, y_train)

    previsao_arvore = modelo_arvore.predict(X_test)

    mae_arvore = mean_absolute_error(
        y_test,
        previsao_arvore
    )

    # Exibe os resultados no console do servidor para auditoria e log
    print("\n--- RESULTADOS ---")

    print("Linear Regression:", round(mae_linear, 2))
    print("Decision Tree Regressor:", round(mae_arvore, 2))

    print("\n--- INTERPRETAÇÃO DOS ERROS ---")

    print(
        f"Linear Regression apresenta um erro absoluto médio "
        f"de {mae_linear:.2f} dólares."
    )

    print(
        f"Decision Tree apresenta um erro absoluto médio "
        f"de {mae_arvore:.2f} dólares."
    )

    # Compara o desempenho e seleciona automaticamente o modelo que errou menos para uso no simulador
    if mae_linear < mae_arvore:

        melhor_modelo = "Linear Regression"
        modelo_escolhido = modelo_linear

        justificativa = (
            "Apresentou menor erro absoluto médio "
            "no conjunto de teste."
        )

    elif mae_arvore < mae_linear:

        melhor_modelo = "Decision Tree Regressor"
        modelo_escolhido = modelo_arvore

        justificativa = (
            "Apresentou menor erro absoluto médio "
            "no conjunto de teste."
        )

    else:

        melhor_modelo = "Empate"
        modelo_escolhido = modelo_linear

        justificativa = (
            "Os dois modelos apresentaram o mesmo "
            "erro absoluto médio. Linear Regression "
            "foi selecionado como critério de desempate."
        )

    print("\n--- ESCOLHA FINAL ---")
    print("Melhor modelo:", melhor_modelo)
    print("Justificativa:", justificativa)

    # Empacota os resultados em um dicionário para enviá-los e exibi-los de forma dinâmica no painel HTML
    resultados = {
        "mae_linear": round(mae_linear, 2),
        "mae_arvore": round(mae_arvore, 2),
        "melhor_modelo": melhor_modelo,
        "justificativa": justificativa,
        "proporcao_treino": "80%",
        "proporcao_teste": "20%",
        "random_state": 42
    }

    # Salva o nome das colunas utilizadas para garantir que os dados do usuário sigam a mesma estrutura
    colunas = X_train.columns.tolist()

    return modelo_escolhido, colunas, resultados