"""
Serviço para validação e melhoria de conteúdo gerado
"""

import re
from typing import Dict, Any, List, Optional, Tuple

class ContentValidator:
    """Classe para validação e melhoria de conteúdo gerado"""
    
    @staticmethod
    def validate_content(content: str, doc_type: str, language: str) -> Tuple[bool, List[str]]:
        """
        Valida o conteúdo gerado para garantir qualidade
        
        Args:
            content: Conteúdo gerado em formato Markdown
            doc_type: Tipo de documento ('ebook', 'guia_pratico', 'dicas', 'documento_oficial')
            language: Idioma do conteúdo ('pt-BR' ou 'en-US')
            
        Returns:
            Tupla com (is_valid, list_of_issues)
        """
        issues = []
        
        # Verificar se o conteúdo está vazio
        if not content or len(content) < 100:
            issues.append("Conteúdo muito curto ou vazio")
            return False, issues
        
        # Verificar estrutura básica (cabeçalhos)
        if not re.search(r'#\s+\w+', content):
            issues.append("Faltam cabeçalhos no documento")
        
        # Verificar seções específicas por tipo de documento
        if doc_type == 'ebook':
            if language == 'pt-BR':
                if not re.search(r'#\s+Introdução', content, re.IGNORECASE) and not re.search(r'#\s+Introdução', content):
                    issues.append("Falta seção de Introdução")
                if not re.search(r'#\s+Conclusão', content, re.IGNORECASE) and not re.search(r'#\s+Conclusão', content):
                    issues.append("Falta seção de Conclusão")
            else:  # en-US
                if not re.search(r'#\s+Introduction', content, re.IGNORECASE):
                    issues.append("Missing Introduction section")
                if not re.search(r'#\s+Conclusion', content, re.IGNORECASE):
                    issues.append("Missing Conclusion section")
        
        # Verificar comprimento mínimo
        min_length = 3000  # Aproximadamente 1 página
        if len(content) < min_length:
            issues.append(f"Conteúdo muito curto ({len(content)} caracteres, mínimo {min_length})")
        
        # Verificar erros comuns de formatação Markdown
        if '](http' in content and not re.search(r'\[.+?\]\(http', content):
            issues.append("Links Markdown mal formatados")
        
        # Verificar parágrafos vazios consecutivos
        if re.search(r'\n\s*\n\s*\n\s*\n', content):
            issues.append("Múltiplos parágrafos vazios consecutivos")
        
        # Verificar se há conteúdo suficiente em cada seção
        sections = re.split(r'#\s+', content)
        for section in sections[1:]:  # Ignorar o que vem antes do primeiro #
            section_title = section.split('\n')[0].strip()
            section_content = '\n'.join(section.split('\n')[1:]).strip()
            
            if len(section_content) < 200:  # Seção muito curta
                issues.append(f"Seção '{section_title}' tem conteúdo insuficiente")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def enhance_content(content: str, doc_type: str, language: str) -> str:
        """
        Melhora o conteúdo gerado para garantir qualidade
        
        Args:
            content: Conteúdo gerado em formato Markdown
            doc_type: Tipo de documento ('ebook', 'guia_pratico', 'dicas', 'documento_oficial')
            language: Idioma do conteúdo ('pt-BR' ou 'en-US')
            
        Returns:
            Conteúdo melhorado
        """
        enhanced_content = content
        
        # Corrigir formatação de cabeçalhos
        enhanced_content = re.sub(r'#(\w+)', r'# \1', enhanced_content)
        
        # Garantir espaçamento adequado após cabeçalhos
        enhanced_content = re.sub(r'(#+ .+)\n([^#\n])', r'\1\n\n\2', enhanced_content)
        
        # Corrigir links Markdown mal formatados
        enhanced_content = re.sub(r'\[([^\]]+)\] \(([^)]+)\)', r'[\1](\2)', enhanced_content)
        
        # Remover múltiplos parágrafos vazios consecutivos
        enhanced_content = re.sub(r'\n\s*\n\s*\n', r'\n\n', enhanced_content)
        
        # Garantir que haja uma linha em branco antes de cada cabeçalho (exceto o primeiro)
        enhanced_content = re.sub(r'([^\n])\n(#+\s+)', r'\1\n\n\2', enhanced_content)
        
        return enhanced_content
    
    @staticmethod
    def get_quality_score(content: str, doc_type: str, language: str) -> float:
        """
        Calcula uma pontuação de qualidade para o conteúdo gerado
        
        Args:
            content: Conteúdo gerado em formato Markdown
            doc_type: Tipo de documento ('ebook', 'guia_pratico', 'dicas', 'documento_oficial')
            language: Idioma do conteúdo ('pt-BR' ou 'en-US')
            
        Returns:
            Pontuação de qualidade (0.0 a 1.0)
        """
        score = 1.0
        
        # Verificar se o conteúdo está vazio
        if not content or len(content) < 100:
            return 0.0
        
        # Penalizar por falta de cabeçalhos
        headers_count = len(re.findall(r'#\s+\w+', content))
        if headers_count < 3:
            score -= 0.2
        
        # Penalizar por conteúdo curto
        if len(content) < 3000:
            score -= 0.1
        
        # Penalizar por falta de seções específicas
        if doc_type == 'ebook':
            if language == 'pt-BR':
                if not re.search(r'#\s+Introdução', content, re.IGNORECASE) and not re.search(r'#\s+Introdução', content):
                    score -= 0.1
                if not re.search(r'#\s+Conclusão', content, re.IGNORECASE) and not re.search(r'#\s+Conclusão', content):
                    score -= 0.1
            else:  # en-US
                if not re.search(r'#\s+Introduction', content, re.IGNORECASE):
                    score -= 0.1
                if not re.search(r'#\s+Conclusion', content, re.IGNORECASE):
                    score -= 0.1
        
        # Penalizar por erros de formatação Markdown
        if '](http' in content and not re.search(r'\[.+?\]\(http', content):
            score -= 0.05
        
        # Penalizar por parágrafos vazios consecutivos
        if re.search(r'\n\s*\n\s*\n\s*\n', content):
            score -= 0.05
        
        # Garantir que a pontuação esteja entre 0.0 e 1.0
        return max(0.0, min(1.0, score))
