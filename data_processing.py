import pandas as pd

def carregar_csv(caminho_arquivo: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho_arquivo)
        if df.empty:
            raise ValueError("O arquivo CSV está vazio.")
        return df
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo: {e}")

def obter_dados_limpos(df: pd.DataFrame) -> pd.DataFrame:
    mascara = (
        df[['course_id', 'course_title', 'price']].notnull().all(axis=1) &
        (df['price'] >= 0) & 
        (df['num_subscribers'] >= 0) &
        (~df.duplicated(subset=['course_id'], keep='first'))
    )
    df_limpo = df[mascara].copy()
    df_limpo['published_timestamp'] = pd.to_datetime(df_limpo['published_timestamp'], errors='coerce')
    return df_limpo

def obter_dados_excedentes(df: pd.DataFrame) -> pd.DataFrame:
    mascara = (
        df[['course_id', 'course_title', 'price']].notnull().all(axis=1) &
        (df['price'] >= 0) & 
        (df['num_subscribers'] >= 0) &
        (~df.duplicated(subset=['course_id'], keep='first'))
    )
    return df[~mascara].copy()