import io
import base64
import matplotlib
# Configura o matplotlib para rodar em segundo plano, evitando erros de interface gráfica no servidor
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Importa as funções do modelo para recriar o ambiente de teste e gerar as avaliações
from sklearn.model_selection import train_test_split
from modelo import preparar_dados, codificar_dados

def _plot_para_base64():
    # Converte o gráfico gerado em um formato de texto (base64) para ser exibido diretamente no HTML
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{imagem_base64}"

def gerar_graficos(df, modelo, colunas):
    # Consolida os gráficos de análise exploratória e desempenho da inteligência artificial
    graficos = {}

    # Identifica o nome do algoritmo escolhido para exibir de forma dinâmica nos títulos
    nome_modelo = type(modelo).__name__
    graficos['nome_modelo'] = nome_modelo

    # Refaz a separação dos dados de teste para garantir que os gráficos avaliem o mesmo cenário que a IA
    X, y = preparar_dados(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    _, X_test_codificado = codificar_dados(X_train, X_test)
    X_test_codificado = X_test_codificado.reindex(columns=colunas, fill_value=0)
    
    # Executa as previsões para comparar os resultados gerados com os dados originais
    previsoes = modelo.predict(X_test_codificado)

    # Gráfico de Fatores de Influência
    plt.figure(figsize=(7, 4))
    
    # Filtra as variáveis puramente numéricas para calcular a correlação com o preço
    colunas_numericas = ['price', 'content_duration', 'num_lectures', 'num_subscribers', 'num_reviews']
    colunas_presentes = [col for col in colunas_numericas if col in df.columns]
    
    if 'price' in colunas_presentes and len(colunas_presentes) > 1:
        df_num = df[colunas_presentes].dropna()
        corr_com_preco = df_num.corr()['price'].drop('price').sort_values()
        
        # Traduz os nomes das colunas para facilitar a leitura visual no painel
        traducao = {
            'content_duration': 'Duração do Curso',
            'num_lectures': 'Quantidade de Aulas',
            'num_subscribers': 'Nº de Inscritos',
            'num_reviews': 'Nº de Avaliações'
        }
        corr_com_preco.index = [traducao.get(x, x) for x in corr_com_preco.index]
        
        # Define vermelho para impactos negativos e verde para impactos que elevam o preço
        cores = ['#d9534f' if val < 0 else '#5cb85c' for val in corr_com_preco]
        corr_com_preco.plot(kind='barh', color=cores)
        
        plt.title('Fatores de Influência (O que faz o preço subir?)')
        plt.xlabel('Impacto no Preço (-1 a 1)')
    else:
        plt.text(0.5, 0.5, 'Dados numéricos insuficientes', ha='center', va='center')
        
    plt.tight_layout()
    graficos['grafico_1'] = _plot_para_base64()


    # Gráfico de Importância das Variáveis
    plt.figure(figsize=(8, 4))
    
    # Verifica dinamicamente o método correto de extração de pesos dependendo do algoritmo utilizado
    if hasattr(modelo, 'feature_importances_'):
        pesos = modelo.feature_importances_
    else:
        pesos = np.abs(modelo.coef_)
        
    # Isola as características que tiveram maior peso na decisão algorítmica
    serie_pesos = pd.Series(pesos, index=colunas).sort_values(ascending=True).tail(7)
    
    serie_pesos.plot(kind='barh', color='teal')
    plt.title(f'Top 7 Variáveis de Maior Impacto ({nome_modelo})')
    plt.xlabel('Grau de Importância / Peso')
    graficos['grafico_2'] = _plot_para_base64()


    # Gráfico de Desempenho do Modelo
    plt.figure(figsize=(7, 4))
    
    # Cria uma dispersão relacionando o valor real do curso com a previsão estipulada pela máquina
    plt.scatter(y_test, previsoes, alpha=0.5, color='purple')
    
    # Adiciona uma linha de referência representando os acertos perfeitos
    max_val = max(y_test.max(), previsoes.max())
    plt.plot([0, max_val], [0, max_val], color='red', linestyle='--', label='Acerto Perfeito')
    
    plt.title(f'Desempenho: Preço Real vs. Preço Previsto ({nome_modelo})')
    plt.xlabel('Preço Real dos Cursos ($)')
    plt.ylabel('Preço Previsto pelo Modelo ($)')
    plt.legend()
    graficos['grafico_3'] = _plot_para_base64()

    return graficos