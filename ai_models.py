"""
Interfaces para diferentes APIs de IA
"""

import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AIModelInterface(ABC):
    """Interface base para modelos de IA"""
    
    @abstractmethod
    def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """
        Gera conteúdo baseado no prompt
        
        Args:
            prompt: Texto do prompt para a IA
            max_tokens: Número máximo de tokens na resposta
            temperature: Temperatura para geração (0.0 a 1.0)
            
        Returns:
            Conteúdo gerado em formato Markdown
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Retorna o nome do modelo
        
        Returns:
            Nome do modelo de IA
        """
        pass

class OpenAIModel(AIModelInterface):
    """Implementação para OpenAI (GPT-3.5/4)"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Você é um assistente especializado em criar conteúdo de alta qualidade em formato Markdown. Seu trabalho é gerar conteúdo detalhado, bem estruturado e sem erros."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            print(f"Erro na chamada à API OpenAI: {str(e)}")
            # Fallback para conteúdo simulado em caso de erro
            return f"# Conteúdo Simulado\n\n*Este é um conteúdo simulado devido a um erro na API: {str(e)}*"
    
    def get_name(self) -> str:
        return f"OpenAI ({self.model})"

class AnthropicModel(AIModelInterface):
    """Implementação para Anthropic (Claude)"""
    
    def __init__(self, api_key: str, model: str = "claude-2"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.anthropic.com/v1/complete"
    
    def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        data = {
            "model": self.model,
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["completion"]
        
        except Exception as e:
            print(f"Erro na chamada à API Anthropic: {str(e)}")
            # Fallback para OpenAI se configurado
            if os.getenv('OPENAI_API_KEY'):
                print("Usando OpenAI como fallback")
                fallback = OpenAIModel(os.getenv('OPENAI_API_KEY'))
                return fallback.generate_content(prompt, max_tokens, temperature)
            
            # Fallback para conteúdo simulado em caso de erro
            return f"# Conteúdo Simulado\n\n*Este é um conteúdo simulado devido a um erro na API: {str(e)}*"
    
    def get_name(self) -> str:
        return f"Anthropic ({self.model})"

class GeminiModel(AIModelInterface):
    """Implementação para Google Gemini"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}", 
                headers=headers, 
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        
        except Exception as e:
            print(f"Erro na chamada à API Gemini: {str(e)}")
            # Fallback para OpenAI se configurado
            if os.getenv('OPENAI_API_KEY'):
                print("Usando OpenAI como fallback")
                fallback = OpenAIModel(os.getenv('OPENAI_API_KEY'))
                return fallback.generate_content(prompt, max_tokens, temperature)
            
            # Fallback para conteúdo simulado em caso de erro
            return f"# Conteúdo Simulado\n\n*Este é um conteúdo simulado devido a um erro na API: {str(e)}*"
    
    def get_name(self) -> str:
        return f"Google Gemini ({self.model})"

class AIModelFactory:
    """Fábrica para criar instâncias de modelos de IA"""
    
    @staticmethod
    def create_model(provider: str, api_key: str, model: Optional[str] = None) -> AIModelInterface:
        """
        Cria uma instância do modelo de IA baseado no provedor
        
        Args:
            provider: Nome do provedor ('openai', 'anthropic', 'gemini')
            api_key: Chave de API para o provedor
            model: Nome do modelo específico (opcional)
            
        Returns:
            Instância do modelo de IA
        """
        if provider.lower() == "openai":
            return OpenAIModel(api_key, model or "gpt-3.5-turbo")
        elif provider.lower() == "anthropic":
            return AnthropicModel(api_key, model or "claude-2")
        elif provider.lower() == "gemini":
            return GeminiModel(api_key, model or "gemini-pro")
        else:
            # Fallback para OpenAI
            print(f"Provedor {provider} não suportado, usando OpenAI como fallback")
            return OpenAIModel(api_key, "gpt-3.5-turbo")
