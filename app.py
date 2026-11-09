from flask import Flask, render_template, request, redirect, url_for, flash
import os
from data_processing import carregar_csv, obter_dados_limpos, obter_dados_excedentes

app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash_messages"
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado.')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            caminho_salvo = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(caminho_salvo)
            return redirect(url_for('dashboard', filename=file.filename))
        else:
            flash('Por favor, envie um arquivo .csv válido.')
            
    return render_template('index.html')

@app.route('/dashboard/<filename>')
def dashboard(filename):
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # Apenas processamento de limpeza
        df_original = carregar_csv(caminho_arquivo)
        df_limpo = obter_dados_limpos(df_original)
        df_excedentes = obter_dados_excedentes(df_original)
        
        # Gera a amostra exigida no enunciado
        amostra_html = df_limpo.head(5).to_html(classes="table")
        
        estatisticas = {
            "total_original": len(df_original),
            "total_limpos": len(df_limpo),
            "total_excedentes": len(df_excedentes),
            "colunas": len(df_limpo.columns)
        }
        
        return render_template('dashboard.html', 
                               estatisticas=estatisticas, 
                               amostra=amostra_html)    
                               
    except Exception as e:
        flash(f'Erro ao processar dados: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)