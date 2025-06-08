"""
Templates para diferentes tipos de documentos
"""

from typing import Dict, Any
from abc import ABC, abstractmethod

class DocumentTemplate(ABC):
    """Classe base para templates de documentos"""
    
    def __init__(self, language: str = "pt-BR"):
        self.language = language
    
    def get_prompt(self, title: str, theme: str, page_count: int) -> str:
        """
        Retorna o prompt completo para o tipo de documento
        
        Args:
            title: Título do documento
            theme: Tema do documento
            page_count: Número de páginas (20 ou 50)
            
        Returns:
            Prompt completo para enviar à IA
        """
        if self.language.lower() == "pt-br":
            return self._get_prompt_pt(title, theme, page_count)
        else:
            return self._get_prompt_en(title, theme, page_count)
    
    @abstractmethod
    def _get_prompt_pt(self, title: str, theme: str, page_count: int) -> str:
        """Implementação do prompt em português"""
        pass
    
    @abstractmethod
    def _get_prompt_en(self, title: str, theme: str, page_count: int) -> str:
        """Implementação do prompt em inglês"""
        pass
    
    def _get_structure_pt(self) -> Dict[str, Any]:
        """Retorna a estrutura do documento em português"""
        return {}
    
    def _get_structure_en(self) -> Dict[str, Any]:
        """Retorna a estrutura do documento em inglês"""
        return {}

class EbookTemplate(DocumentTemplate):
    """Template para eBooks"""
    
    def _get_prompt_pt(self, title: str, theme: str, page_count: int) -> str:
        chapter_count = 5 if page_count == 20 else 10
        
        return f"""Crie um eBook completo em formato Markdown com o título "{title}" sobre o tema "{theme}".

O eBook deve ter a seguinte estrutura:
1. Capa com título e subtítulo atraente
2. Sumário detalhado
3. Introdução envolvente (aproximadamente 500 palavras)
4. {chapter_count} capítulos principais, cada um com:
   - Título claro e atraente
   - 3-4 subtópicos por capítulo
   - Aproximadamente {1000 if page_count == 20 else 2500} palavras por capítulo
   - Exemplos práticos e casos de estudo
   - Citações relevantes (quando apropriado)
5. Conclusão com resumo dos pontos principais e chamada para ação (aproximadamente 500 palavras)
6. Referências bibliográficas (pelo menos 5 fontes)
7. Sobre o autor (crie uma biografia fictícia de um especialista no tema)

Requisitos de qualidade:
- Use linguagem profissional mas acessível
- Inclua exemplos práticos e aplicáveis
- Evite jargões desnecessários
- Mantenha um tom consistente e envolvente
- Use formatação Markdown para destacar pontos importantes
- Crie um conteúdo original e valioso para o leitor

O eBook completo deve ter aproximadamente {page_count * 500} palavras no total.
"""
    
    def _get_prompt_en(self, title: str, theme: str, page_count: int) -> str:
        chapter_count = 5 if page_count == 20 else 10
        
        return f"""Create a complete eBook in Markdown format with the title "{title}" about the theme "{theme}".

The eBook should have the following structure:
1. Cover with title and attractive subtitle
2. Detailed table of contents
3. Engaging introduction (approximately 500 words)
4. {chapter_count} main chapters, each with:
   - Clear and attractive title
   - 3-4 subtopics per chapter
   - Approximately {1000 if page_count == 20 else 2500} words per chapter
   - Practical examples and case studies
   - Relevant quotes (when appropriate)
5. Conclusion with summary of main points and call to action (approximately 500 words)
6. Bibliographical references (at least 5 sources)
7. About the author (create a fictional biography of an expert on the theme)

Quality requirements:
- Use professional but accessible language
- Include practical and applicable examples
- Avoid unnecessary jargon
- Maintain a consistent and engaging tone
- Use Markdown formatting to highlight important points
- Create original and valuable content for the reader

The complete eBook should have approximately {page_count * 500} words in total.
"""

class PracticalGuideTemplate(DocumentTemplate):
    """Template para Guias Práticos"""
    
    def _get_prompt_pt(self, title: str, theme: str, page_count: int) -> str:
        section_count = 5 if page_count == 20 else 10
        
        return f"""Crie um guia prático completo em formato Markdown com o título "{title}" sobre o tema "{theme}".

O guia deve ter a seguinte estrutura:
1. Capa com título e subtítulo explicativo
2. Índice detalhado
3. Introdução explicando o propósito do guia (aproximadamente 400 palavras)
4. {section_count} seções principais, cada uma com:
   - Título claro e objetivo
   - Explicação detalhada do tópico
   - Passo a passo com instruções numeradas
   - Dicas e avisos em destaque (usando blockquotes >)
   - Melhores práticas em formato de lista
   - Aproximadamente {800 if page_count == 20 else 2000} palavras por seção
5. Recursos adicionais (ferramentas, modelos, checklists)
6. Glossário com termos técnicos
7. Conclusão com próximos passos (aproximadamente 300 palavras)

Requisitos de qualidade:
- Use linguagem direta e objetiva
- Inclua exemplos concretos e aplicáveis
- Forneça instruções detalhadas e claras
- Use formatação Markdown para destacar pontos importantes
- Organize o conteúdo de forma lógica e progressiva
- Foque em soluções práticas e acionáveis

O guia completo deve ter aproximadamente {page_count * 500} palavras no total.
"""
    
    def _get_prompt_en(self, title: str, theme: str, page_count: int) -> str:
        section_count = 5 if page_count == 20 else 10
        
        return f"""Create a complete practical guide in Markdown format with the title "{title}" about the theme "{theme}".

The guide should have the following structure:
1. Cover with title and explanatory subtitle
2. Detailed table of contents
3. Introduction explaining the purpose of the guide (approximately 400 words)
4. {section_count} main sections, each with:
   - Clear and objective title
   - Detailed explanation of the topic
   - Step-by-step with numbered instructions
   - Tips and warnings highlighted (using blockquotes >)
   - Best practices in list format
   - Approximately {800 if page_count == 20 else 2000} words per section
5. Additional resources (tools, templates, checklists)
6. Glossary with technical terms
7. Conclusion with next steps (approximately 300 words)

Quality requirements:
- Use direct and objective language
- Include concrete and applicable examples
- Provide detailed and clear instructions
- Use Markdown formatting to highlight important points
- Organize content in a logical and progressive manner
- Focus on practical and actionable solutions

The complete guide should have approximately {page_count * 500} words in total.
"""

class TipsGuideTemplate(DocumentTemplate):
    """Template para Guias de Dicas"""
    
    def _get_prompt_pt(self, title: str, theme: str, page_count: int) -> str:
        tips_count = 20 if page_count == 20 else 50
        
        return f"""Crie um guia de dicas completo em formato Markdown com o título "{title}" sobre o tema "{theme}".

O guia deve ter a seguinte estrutura:
1. Capa com título e subtítulo atraente
2. Introdução explicando a importância das dicas (aproximadamente 300 palavras)
3. {tips_count} dicas práticas, cada uma com:
   - Título claro e objetivo para a dica
   - Explicação detalhada (100-150 palavras por dica)
   - O que fazer (em formato de lista)
   - O que evitar (em formato de lista)
   - Um exemplo de aplicação prática
4. Resumo das principais dicas
5. Recursos adicionais para aprofundamento
6. Conclusão com reflexões finais (aproximadamente 200 palavras)

Requisitos de qualidade:
- Use linguagem direta e objetiva
- Forneça dicas práticas e aplicáveis imediatamente
- Evite generalidades e seja específico
- Use formatação Markdown para destacar pontos importantes
- Organize as dicas em ordem lógica (do básico ao avançado)
- Inclua exemplos concretos para cada dica

O guia completo deve ter aproximadamente {page_count * 500} palavras no total.
"""
    
    def _get_prompt_en(self, title: str, theme: str, page_count: int) -> str:
        tips_count = 20 if page_count == 20 else 50
        
        return f"""Create a complete tips guide in Markdown format with the title "{title}" about the theme "{theme}".

The guide should have the following structure:
1. Cover with title and attractive subtitle
2. Introduction explaining the importance of the tips (approximately 300 words)
3. {tips_count} practical tips, each with:
   - Clear and objective title for the tip
   - Detailed explanation (100-150 words per tip)
   - What to do (in list format)
   - What to avoid (in list format)
   - A practical application example
4. Summary of the main tips
5. Additional resources for further learning
6. Conclusion with final reflections (approximately 200 words)

Quality requirements:
- Use direct and objective language
- Provide practical and immediately applicable tips
- Avoid generalities and be specific
- Use Markdown formatting to highlight important points
- Organize tips in logical order (from basic to advanced)
- Include concrete examples for each tip

The complete guide should have approximately {page_count * 500} words in total.
"""

class OfficialDocumentTemplate(DocumentTemplate):
    """Template para Documentos Oficiais"""
    
    def _get_prompt_pt(self, title: str, theme: str, page_count: int) -> str:
        section_count = 5 if page_count == 20 else 10
        
        return f"""Crie um documento oficial completo em formato Markdown com o título "{title}" sobre o tema "{theme}".

O documento deve ter a seguinte estrutura:
1. Cabeçalho com título, organização fictícia e data atual
2. Sumário executivo (aproximadamente 300 palavras)
3. Índice detalhado
4. Introdução com contexto, escopo e objetivos (aproximadamente 400 palavras)
5. {section_count} seções principais, cada uma com:
   - Título formal e numerado
   - 3 subseções numeradas
   - Dados e estatísticas relevantes
   - Análise técnica e considerações formais
   - Aproximadamente {800 if page_count == 20 else 2000} palavras por seção
6. Conclusões e recomendações
7. Anexos (tabelas, gráficos, informações complementares)
8. Referências bibliográficas em formato acadêmico

Requisitos de qualidade:
- Use linguagem formal e técnica
- Mantenha tom objetivo e imparcial
- Inclua dados e estatísticas (fictícios mas plausíveis)
- Use formatação Markdown para estruturar o documento
- Mantenha consistência na numeração e formatação
- Evite linguagem coloquial ou opinativa

O documento completo deve ter aproximadamente {page_count * 500} palavras no total.
"""
    
    def _get_prompt_en(self, title: str, theme: str, page_count: int) -> str:
        section_count = 5 if page_count == 20 else 10
        
        return f"""Create a complete official document in Markdown format with the title "{title}" about the theme "{theme}".

The document should have the following structure:
1. Header with title, fictional organization, and current date
2. Executive summary (approximately 300 words)
3. Detailed table of contents
4. Introduction with context, scope, and objectives (approximately 400 words)
5. {section_count} main sections, each with:
   - Formal and numbered title
   - 3 numbered subsections
   - Relevant data and statistics
   - Technical analysis and formal considerations
   - Approximately {800 if page_count == 20 else 2000} words per section
6. Conclusions and recommendations
7. Appendices (tables, graphs, complementary information)
8. Bibliographical references in academic format

Quality requirements:
- Use formal and technical language
- Maintain objective and impartial tone
- Include data and statistics (fictional but plausible)
- Use Markdown formatting to structure the document
- Maintain consistency in numbering and formatting
- Avoid colloquial or opinionated language

The complete document should have approximately {page_count * 500} words in total.
"""

class TemplateFactory:
    """Fábrica para criar instâncias de templates de documentos"""
    
    @staticmethod
    def create_template(doc_type: str, language: str = "pt-BR") -> DocumentTemplate:
        """
        Cria uma instância do template baseado no tipo de documento
        
        Args:
            doc_type: Tipo de documento ('ebook', 'guia_pratico', 'dicas', 'documento_oficial')
            language: Idioma do documento ('pt-BR' ou 'en-US')
            
        Returns:
            Instância do template de documento
        """
        if doc_type.lower() == "ebook":
            return EbookTemplate(language)
        elif doc_type.lower() == "guia_pratico":
            return PracticalGuideTemplate(language)
        elif doc_type.lower() == "dicas":
            return TipsGuideTemplate(language)
        elif doc_type.lower() == "documento_oficial":
            return OfficialDocumentTemplate(language)
        else:
            # Fallback para eBook
            print(f"Tipo de documento {doc_type} não suportado, usando eBook como fallback")
            return EbookTemplate(language)
