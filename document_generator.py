"""
Integração da validação de conteúdo com a geração de PDF
"""

import os
from content_validator import ContentValidator
from pdf_generator import PdfGenerator
from typing import Dict, Any, Tuple, Optional

class DocumentGenerator:
    """Classe para geração e validação de documentos"""
    
    @staticmethod
    def generate_document(content: str, doc_type: str, language: str, title: str, output_path: str) -> Tuple[bool, str, Optional[str]]:
        """
        Valida o conteúdo, melhora se necessário e gera o PDF
        
        Args:
            content: Conteúdo gerado em formato Markdown
            doc_type: Tipo de documento ('ebook', 'guia_pratico', 'dicas', 'documento_oficial')
            language: Idioma do conteúdo ('pt-BR' ou 'en-US')
            title: Título do documento
            output_path: Caminho para salvar o arquivo PDF
            
        Returns:
            Tupla com (success, message, pdf_path)
        """
        # Validar conteúdo
        is_valid, issues = ContentValidator.validate_content(content, doc_type, language)
        
        # Se houver problemas, melhorar o conteúdo
        if not is_valid:
            content = ContentValidator.enhance_content(content, doc_type, language)
            
            # Verificar novamente após melhorias
            is_valid, issues = ContentValidator.validate_content(content, doc_type, language)
            
            # Se ainda houver problemas graves, retornar erro
            if not is_valid and any(issue.startswith("Falta seção") for issue in issues):
                return False, f"Falha na geração do documento: {', '.join(issues)}", None
        
        # Calcular pontuação de qualidade
        quality_score = ContentValidator.get_quality_score(content, doc_type, language)
        
        # Se a qualidade for muito baixa, retornar erro
        if quality_score < 0.5:
            return False, f"Qualidade do conteúdo muito baixa (pontuação: {quality_score:.2f})", None
        
        try:
            # Gerar PDF
            pdf_path = PdfGenerator.generate_pdf(content, output_path)
            
            # Verificar se o arquivo foi criado
            if not os.path.exists(pdf_path):
                return False, "Falha ao criar arquivo PDF", None
            
            return True, "Documento gerado com sucesso", pdf_path
        
        except Exception as e:
            return False, f"Erro ao gerar PDF: {str(e)}", None
