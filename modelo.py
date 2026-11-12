import pandas as pd

def preparar_dados(df):
    # Filtra apenas os cursos pagos, pois cursos gratuitos distorceriam a previsão de preços
    df = df[df['is_paid'] == True].copy()

    # Remove qualquer linha que tenha dados em branco nas colunas essenciais para o modelo
    df = df.dropna(subset=[
        'content_duration',
        'num_lectures',
        'level',
        'subject',
        'price'
    ])

    # Separa as características (X) que vão prever o resultado e o alvo (y) que é o preço
    X = df[['content_duration', 'num_lectures', 'level', 'subject']]
    y = df['price']

    return X, y


def codificar_dados(X_train, X_test):
    # Transforma as colunas de texto (nível e assunto) em números (colunas binárias) para a IA conseguir ler
    treino = pd.get_dummies(
        X_train,
        columns=['level', 'subject']
    )

    teste = pd.get_dummies(
        X_test,
        columns=['level', 'subject']
    )

    # Garante que os dados de teste tenham exatamente as mesmas colunas estruturais que os dados de treino
    teste = teste.reindex(
        columns=treino.columns,
        fill_value=0
    )

    return treino, teste


def prever(modelo, dados, colunas):
    # Converte os dados preenchidos pelo utilizador no formulário num formato de tabela (DataFrame)
    X = pd.DataFrame([dados])

    # Aplica a mesma transformação de texto para números utilizada no treinamento
    X = pd.get_dummies(
        X,
        columns=['level', 'subject']
    )

    # Alinha as colunas do formulário com as colunas exatas que o modelo aprendeu a usar
    X = X.reindex(
        columns=colunas,
        fill_value=0
    )

    # Executa a inteligência artificial para calcular o valor e retorna o primeiro resultado
    resultado = modelo.predict(X)

    return resultado[0]