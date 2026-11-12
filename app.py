from flask import Flask, render_template, request, redirect, url_for, flash
import os

# Importação dos módulos internos criados para organizar a arquitetura do projeto
from data_processing import carregar_csv, obter_dados_limpos, obter_dados_excedentes
from treinamento import treinar
from graficos import gerar_graficos
from modelo import prever

# Inicialização da aplicação Flask e configuração da chave de segurança para alertas
app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash_messages"

# Captura o caminho absoluto da pasta onde o app.py está localizado para evitar erros de diretório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

# Cria a pasta 'uploads' na raiz do projeto, caso ela ainda não exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Rota da página inicial responsável por exibir a tela de upload e receber o CSV
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o campo de arquivo foi enviado no formulário
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado.')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Verifica se o utilizador clicou em enviar sem selecionar um arquivo
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
            
        # Confirma a extensão do arquivo antes de salvar por segurança
        if file and file.filename.endswith('.csv'):
            caminho_salvo = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(caminho_salvo)
            # Redireciona para o dashboard passando o nome do arquivo salvo
            return redirect(url_for('dashboard', filename=file.filename))
        else:
            flash('Por favor, envie um arquivo .csv válido.')
            
    return render_template('index.html')


# Rota do dashboard que orquestra a limpeza, treino do modelo, gráficos e simulador
@app.route('/dashboard/<filename>', methods=['GET', 'POST'])
def dashboard(filename):
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # Leitura e limpeza dos dados
        df_original = carregar_csv(caminho_arquivo)
        df_limpo = obter_dados_limpos(df_original)
        df_excedentes = obter_dados_excedentes(df_original)

        # Treinamento e avaliação do modelo
        modelo_escolhido, colunas_treinadas, resultados = treinar(df_limpo)
        
        # Criação das imagens base64 dos gráficos analíticos
        graficos_gerados = gerar_graficos(df_limpo, modelo_escolhido, colunas_treinadas)

        # Preparação dos dados tabulares e estatísticas para exibir no HTML
        amostra_html = df_limpo.head(5).to_html(classes="table")
        estatisticas = {
            "total_original": len(df_original),
            "total_limpos": len(df_limpo),
            "total_excedentes": len(df_excedentes),
            "colunas": len(df_limpo.columns)
        }
        
        # Extrai os valores únicos das colunas para preencher as opções do formulário dinamicamente
        niveis_unicos = sorted(df_limpo['level'].dropna().unique().tolist())
        assuntos_unicos = sorted(df_limpo['subject'].dropna().unique().tolist())

        previsao_resultado = None
        dados_inseridos = None
        
        # Executa o simulador de preço apenas quando o formulário lateral é submetido
        if request.method == 'POST':
            # Captura e converte os dados preenchidos no HTML
            content_duration = float(request.form.get('content_duration', 0))
            num_lectures = int(request.form.get('num_lectures', 0))
            level = request.form.get('level')
            subject = request.form.get('subject')

            # Agrupa os inputs em um dicionário para enviar ao modelo
            dados_inseridos = {
                'content_duration': content_duration,
                'num_lectures': num_lectures,
                'level': level,
                'subject': subject
            }
            
            # Chama a função de predição e formata o resultado para exibir como moeda ($)
            preco_estimado = prever(modelo_escolhido, dados_inseridos, colunas_treinadas)
            previsao_resultado = f"${max(0.0, float(preco_estimado)):.2f}"

        # Renderiza a página final enviando todas as variáveis processadas para o frontend
        return render_template('dashboard.html', 
                               estatisticas=estatisticas, 
                               amostra=amostra_html,
                               graficos=graficos_gerados,
                               resultados=resultados,
                               niveis=niveis_unicos,
                               assuntos=assuntos_unicos,
                               previsao_resultado=previsao_resultado,
                               dados_inseridos=dados_inseridos,
                               filename=filename)    
                               
    except Exception as e:
        # Tratamento de erro genérico para problemas como arquivo corrompido ou colunas ausentes
        flash(f'Erro ao processar dados: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug para facilitar o desenvolvimento
    app.run(debug=True)