"""
Serviço para geração de PDF a partir de conteúdo Markdown
"""

import os
import markdown
from weasyprint import HTML, CSS
from typing import Optional

class PdfGenerator:
    """Classe para geração de PDF a partir de conteúdo Markdown"""
    
    @staticmethod
    def markdown_to_html(markdown_content: str) -> str:
        """
        Converte conteúdo Markdown para HTML
        
        Args:
            markdown_content: Conteúdo em formato Markdown
            
        Returns:
            Conteúdo em formato HTML
        """
        # Extensões para melhorar a conversão
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
        
        html = markdown.markdown(markdown_content, extensions=extensions)
        
        # Adicionar CSS básico para melhorar a aparência
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Documento Gerado</title>
            <style>
                @page {{
                    margin: 2.5cm 1.5cm;
                    @top-center {{
                        content: '';
                    }}
                    @bottom-center {{
                        content: counter(page);
                    }}
                }}
                
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                }}
                
                h1 {{
                    font-size: 2.2em;
                    text-align: center;
                    page-break-before: always;
                    page-break-after: avoid;
                }}
                
                h1:first-of-type {{
                    page-break-before: avoid;
                }}
                
                h2 {{
                    font-size: 1.8em;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 0.3em;
                    page-break-after: avoid;
                }}
                
                h3 {{
                    font-size: 1.5em;
                    page-break-after: avoid;
                }}
                
                p {{
                    margin-bottom: 1em;
                    text-align: justify;
                }}
                
                ul, ol {{
                    margin-bottom: 1em;
                }}
                
                li {{
                    margin-bottom: 0.5em;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 1em;
                }}
                
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                }}
                
                th {{
                    background-color: #f2f2f2;
                    text-align: left;
                }}
                
                img {{
                    max-width: 100%;
                    height: auto;
                }}
                
                blockquote {{
                    border-left: 4px solid #ddd;
                    padding-left: 1em;
                    color: #666;
                    margin-left: 0;
                }}
                
                code {{
                    background-color: #f5f5f5;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                    font-family: monospace;
                }}
                
                pre {{
                    background-color: #f5f5f5;
                    padding: 1em;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                
                hr {{
                    border: 0;
                    border-top: 1px solid #eee;
                    margin: 2em 0;
                }}
                
                .page-break {{
                    page-break-after: always;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return html_template
    
    @staticmethod
    def generate_pdf(markdown_content: str, output_path: str) -> str:
        """
        Gera um arquivo PDF a partir de conteúdo Markdown
        
        Args:
            markdown_content: Conteúdo em formato Markdown
            output_path: Caminho para salvar o arquivo PDF
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Converter Markdown para HTML
        html_content = PdfGenerator.markdown_to_html(markdown_content)
        
        # Gerar PDF com WeasyPrint
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
