from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import uuid
from datetime import datetime
import markdown
from weasyprint import HTML, CSS

# Importar módulos personalizados
from ai_models import AIModelFactory
from document_templates import TemplateFactory
from pdf_generator import PdfGenerator
from content_validator import ContentValidator
from document_generator import DocumentGenerator

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(24)

# Configuração de pastas
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PDF_FOLDER = os.path.join(UPLOAD_FOLDER, 'pdfs')
os.makedirs(PDF_FOLDER, exist_ok=True)

# Armazenamento temporário (em produção seria um banco de dados)
documents_db = []

# Configuração de chaves de API (em produção, usar variáveis de ambiente)
API_KEYS = {
    'openai': os.getenv('OPENAI_API_KEY', ''),
    'anthropic': os.getenv('ANTHROPIC_API_KEY', ''),
    'gemini': os.getenv('GEMINI_API_KEY', '')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_document():
    try:
        # Obter dados do formulário
        data = request.json
        title = data.get('title')
        theme = data.get('theme')
        ai_model_provider = data.get('ai_model')
        doc_type = data.get('doc_type')
        page_count = int(data.get('page_count', 20))
        language = data.get('language', 'pt-BR')
        quality = data.get('quality', 'high')
        
        # Validar dados
        if not all([title, theme, ai_model_provider, doc_type]):
            return jsonify({'error': 'Dados incompletos'}), 400
        
        # Obter chave de API
        api_key = API_KEYS.get(ai_model_provider)
        
        # Para fins de demonstração, se não houver chave, simular geração
        if not api_key:
            print(f"Chave de API para {ai_model_provider} não configurada, usando simulação")
            content = simulate_ai_generation(title, theme, doc_type, page_count, language)
        else:
            # Criar instância do modelo de IA
            ai_model = AIModelFactory.create_model(ai_model_provider, api_key)
            
            # Criar instância do template de documento
            document_template = TemplateFactory.create_template(doc_type, language)
            
            # Gerar prompt baseado no template
            prompt = document_template.get_prompt(title, theme, page_count)
            
            # Ajustar parâmetros de qualidade
            temperature = 0.7  # Padrão
            if quality == 'high':
                temperature = 0.5  # Mais determinístico para alta qualidade
            elif quality == 'premium':
                temperature = 0.3  # Ainda mais determinístico para qualidade premium
            
            # Calcular tokens com base no tamanho do documento
            max_tokens = 4000 if page_count == 20 else 8000
            
            # Gerar conteúdo usando o modelo de IA
            content = ai_model.generate_content(prompt, max_tokens=max_tokens, temperature=temperature)
        
        # Validar e melhorar o conteúdo
        content = ContentValidator.enhance_content(content, doc_type, language)
        
        # Gerar nome de arquivo único
        doc_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{title.replace(' ', '_')}_{timestamp}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, filename)
        
        # Gerar PDF
        success, message, generated_path = DocumentGenerator.generate_document(
            content, doc_type, language, title, pdf_path
        )
        
        if not success:
            return jsonify({'error': message}), 500
        
        # Salvar no "banco de dados" temporário
        doc_info = {
            'id': doc_id,
            'title': title,
            'theme': theme,
            'ai_model': ai_model_provider,
            'doc_type': doc_type,
            'page_count': page_count,
            'language': language,
            'file_path': filename,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        documents_db.append(doc_info)
        
        # Retornar informações do documento gerado
        return jsonify(doc_info), 200
    
    except Exception as e:
        print(f"Erro na geração: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    return jsonify(documents_db), 200

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    global documents_db
    
    # Encontrar o documento
    doc = next((d for d in documents_db if d['id'] == doc_id), None)
    
    if not doc:
        return jsonify({'error': 'Documento não encontrado'}), 404
    
    # Excluir arquivo PDF
    pdf_path = os.path.join(PDF_FOLDER, doc['file_path'])
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    # Remover do "banco de dados"
    documents_db = [d for d in documents_db if d['id'] != doc_id]
    
    return jsonify({'message': 'Documento excluído com sucesso'}), 200

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview_file(filename):
    return send_from_directory(PDF_FOLDER, filename)

@app.route('/api/settings', methods=['POST'])
def save_settings():
    try:
        # Obter dados do formulário
        data = request.json
        
        # Atualizar chaves de API
        if 'openai_api_key' in data and data['openai_api_key']:
            API_KEYS['openai'] = data['openai_api_key']
        
        if 'anthropic_api_key' in data and data['anthropic_api_key']:
            API_KEYS['anthropic'] = data['anthropic_api_key']
        
        if 'gemini_api_key' in data and data['gemini_api_key']:
            API_KEYS['gemini'] = data['gemini_api_key']
        
        # Em produção, salvar em variáveis de ambiente ou banco de dados seguro
        
        return jsonify({'message': 'Configurações salvas com sucesso'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Simulação de geração de conteúdo por IA
def simulate_ai_generation(title, theme, doc_type, page_count, language):
    # Em um cenário real, aqui seria feita a chamada à API de IA
    # Por enquanto, vamos usar templates predefinidos
    
    template = TemplateFactory.create_template(doc_type, language)
    prompt = template.get_prompt(title, theme, page_count)
    
    # Gerar conteúdo simulado baseado no tipo de documento
    if doc_type == "ebook":
        chapter_count = 5 if page_count == 20 else 10
        words_per_chapter = 600 if page_count == 20 else 1500
        
        if language == "pt-BR":
            content = f"""# {title}

## Sumário

1. Introdução
{', '.join([f'{i+2}. Capítulo {i+1}' for i in range(chapter_count)])}
{chapter_count+2}. Conclusão
{chapter_count+3}. Referências
{chapter_count+4}. Sobre o Autor

## Introdução

Este é um eBook sobre {theme}. O conteúdo foi gerado automaticamente como demonstração.

{chr(10).join([f'''
## Capítulo {i+1}

Conteúdo do capítulo {i+1} sobre {theme}.

### Subtópico 1

Desenvolvimento do primeiro subtópico.

### Subtópico 2

Desenvolvimento do segundo subtópico.

### Subtópico 3

Desenvolvimento do terceiro subtópico com exemplos práticos.
''' for i in range(chapter_count)])}

## Conclusão

Resumo dos pontos principais e reflexões finais sobre {theme}.

## Referências

1. Referência 1
2. Referência 2
3. Referência 3

## Sobre o Autor

Breve biografia fictícia de um especialista em {theme}.
"""
        else:  # en-US
            content = f"""# {title}

## Table of Contents

1. Introduction
{', '.join([f'{i+2}. Chapter {i+1}' for i in range(chapter_count)])}
{chapter_count+2}. Conclusion
{chapter_count+3}. References
{chapter_count+4}. About the Author

## Introduction

This is an eBook about {theme}. The content was automatically generated as a demonstration.

{chr(10).join([f'''
## Chapter {i+1}

Content of chapter {i+1} about {theme}.

### Subtopic 1

Development of the first subtopic.

### Subtopic 2

Development of the second subtopic.

### Subtopic 3

Development of the third subtopic with practical examples.
''' for i in range(chapter_count)])}

## Conclusion

Summary of main points and final reflections on {theme}.

## References

1. Reference 1
2. Reference 2
3. Reference 3

## About the Author

Brief fictional biography of an expert on {theme}.
"""
    else:
        # Para outros tipos, usar um template genérico
        if language == "pt-BR":
            content = f"""# {title}

## Introdução

Este é um documento sobre {theme}. O conteúdo foi gerado automaticamente como demonstração.

## Seção 1

Conteúdo da primeira seção.

## Seção 2

Conteúdo da segunda seção.

## Seção 3

Conteúdo da terceira seção.

## Conclusão

Resumo e considerações finais sobre {theme}.
"""
        else:  # en-US
            content = f"""# {title}

## Introduction

This is a document about {theme}. The content was automatically generated as a demonstration.

## Section 1

Content of the first section.

## Section 2

Content of the second section.

## Section 3

Content of the third section.

## Conclusion

Summary and final considerations about {theme}.
"""
    
    return content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
