import pandas as pd

def carregar_csv(caminho_arquivo: str) -> pd.DataFrame:
    # Tenta ler o arquivo CSV e verifica se ele não está vazio antes de prosseguir
    try:
        df = pd.read_csv(caminho_arquivo)
        if df.empty:
            raise ValueError("O arquivo CSV está vazio.")
        return df
    # Captura e repassa qualquer erro que aconteça durante a leitura
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo: {e}")

def obter_dados_limpos(df: pd.DataFrame) -> pd.DataFrame:
    # Cria um filtro com as regras de negócio: colunas obrigatórias, sem valores negativos e sem IDs duplicados
    mascara = (
        df[['course_id', 'course_title', 'price']].notnull().all(axis=1) &
        (df['price'] >= 0) & 
        (df['num_subscribers'] >= 0) &
        (~df.duplicated(subset=['course_id'], keep='first'))
    )
    
    # Aplica o filtro para criar uma cópia apenas com os cursos válidos
    df_limpo = df[mascara].copy()
    
    # Padroniza a coluna de data de publicação para o formato de tempo do Pandas
    df_limpo['published_timestamp'] = pd.to_datetime(df_limpo['published_timestamp'], errors='coerce')
    
    return df_limpo

def obter_dados_excedentes(df: pd.DataFrame) -> pd.DataFrame:
    # Recria o mesmo filtro de validação usado na limpeza principal
    mascara = (
        df[['course_id', 'course_title', 'price']].notnull().all(axis=1) &
        (df['price'] >= 0) & 
        (df['num_subscribers'] >= 0) &
        (~df.duplicated(subset=['course_id'], keep='first'))
    )
    
    # Retorna apenas as linhas que falharam na validação (usando o símbolo ~ para inverter o filtro)
    return df[~mascara].copy()