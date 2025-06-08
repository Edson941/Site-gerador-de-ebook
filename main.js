// Main JavaScript for Gerador de eBooks AI

document.addEventListener('DOMContentLoaded', function() {
    // Elementos da interface
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const generatorForm = document.getElementById('generator-form');
    const generationStatus = document.getElementById('generation-status');
    const generationResult = document.getElementById('generation-result');
    const previewContainer = document.getElementById('preview-container');
    const previewBtn = document.getElementById('preview-btn');
    const downloadBtn = document.getElementById('download-btn');
    const pdfPreview = document.getElementById('pdf-preview');
    const deleteModal = document.getElementById('delete-modal');
    const closeModal = document.querySelector('.close');
    const confirmDelete = document.getElementById('confirm-delete');
    const cancelDelete = document.getElementById('cancel-delete');
    
    // Variáveis globais
    let currentDocId = null;
    let currentFilePath = null;
    
    // Inicialização
    loadHistory();
    
    // Navegação por abas
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Atualizar abas ativas
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Atualizar conteúdo ativo
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
            
            // Carregar histórico quando a aba for selecionada
            if (tabId === 'history') {
                loadHistory();
            }
        });
    });
    
    // Envio do formulário de geração
    generatorForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Mostrar status de geração
        generatorForm.style.display = 'none';
        generationStatus.style.display = 'block';
        generationResult.style.display = 'none';
        
        // Simular progresso
        simulateProgress();
        
        // Obter dados do formulário
        const formData = {
            title: document.getElementById('title').value,
            theme: document.getElementById('theme').value,
            ai_model: document.getElementById('ai_model').value,
            doc_type: document.getElementById('doc_type').value,
            page_count: parseInt(document.getElementById('page_count').value),
            language: document.getElementById('language').value,
            quality: document.getElementById('quality').value
        };
        
        // Enviar requisição para o backend
        fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na geração do documento');
            }
            return response.json();
        })
        .then(data => {
            // Armazenar informações do documento
            currentDocId = data.id;
            currentFilePath = data.file_path;
            
            // Preencher resultado
            document.getElementById('result-title').textContent = data.title;
            document.getElementById('result-theme').textContent = data.theme;
            document.getElementById('result-type').textContent = getDocTypeName(data.doc_type);
            document.getElementById('result-size').textContent = data.page_count;
            document.getElementById('result-ai').textContent = getAIModelName(data.ai_model);
            document.getElementById('result-language').textContent = getLanguageName(data.language);
            document.getElementById('result-date').textContent = data.created_at;
            
            // Configurar botão de download
            downloadBtn.href = `/download/${data.file_path}`;
            
            // Mostrar resultado
            generationStatus.style.display = 'none';
            generationResult.style.display = 'block';
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao gerar o documento. Por favor, tente novamente.');
            
            // Voltar para o formulário
            generationStatus.style.display = 'none';
            generatorForm.style.display = 'block';
        });
    });
    
    // Visualização do PDF
    previewBtn.addEventListener('click', function() {
        if (currentFilePath) {
            pdfPreview.src = `/preview/${currentFilePath}`;
            previewContainer.style.display = 'block';
            
            // Scroll para a visualização
            previewContainer.scrollIntoView({ behavior: 'smooth' });
        }
    });
    
    // Modal de exclusão
    closeModal.addEventListener('click', function() {
        deleteModal.style.display = 'none';
    });
    
    cancelDelete.addEventListener('click', function() {
        deleteModal.style.display = 'none';
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });
    
    confirmDelete.addEventListener('click', function() {
        if (currentDocId) {
            deleteDocument(currentDocId);
        }
    });
    
    // Funções auxiliares
    function loadHistory() {
        fetch('/api/documents')
            .then(response => response.json())
            .then(data => {
                const historyItems = document.getElementById('history-items');
                const historyEmpty = document.getElementById('history-empty');
                const historyTable = document.getElementById('history-table');
                
                // Limpar histórico atual
                historyItems.innerHTML = '';
                
                if (data.length === 0) {
                    historyEmpty.style.display = 'block';
                    historyTable.style.display = 'none';
                } else {
                    historyEmpty.style.display = 'none';
                    historyTable.style.display = 'block';
                    
                    // Adicionar itens ao histórico
                    data.forEach(doc => {
                        const row = document.createElement('tr');
                        
                        row.innerHTML = `
                            <td>${doc.title}</td>
                            <td>${getDocTypeName(doc.doc_type)}</td>
                            <td>${getAIModelName(doc.ai_model)}</td>
                            <td>${doc.created_at}</td>
                            <td>
                                <a href="/download/${doc.file_path}" class="btn btn-primary btn-sm">
                                    <i class="fas fa-download"></i>
                                </a>
                                <button class="btn btn-secondary btn-sm preview-doc" data-path="${doc.file_path}">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-danger btn-sm delete-doc" data-id="${doc.id}">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        `;
                        
                        historyItems.appendChild(row);
                    });
                    
                    // Adicionar eventos aos botões
                    document.querySelectorAll('.preview-doc').forEach(btn => {
                        btn.addEventListener('click', function() {
                            const path = this.getAttribute('data-path');
                            previewDocument(path);
                        });
                    });
                    
                    document.querySelectorAll('.delete-doc').forEach(btn => {
                        btn.addEventListener('click', function() {
                            const id = this.getAttribute('data-id');
                            showDeleteConfirmation(id);
                        });
                    });
                }
            })
            .catch(error => {
                console.error('Erro ao carregar histórico:', error);
                alert('Ocorreu um erro ao carregar o histórico de documentos.');
            });
    }
    
    function previewDocument(path) {
        // Mudar para a aba do gerador
        tabs[0].click();
        
        // Configurar visualização
        pdfPreview.src = `/preview/${path}`;
        previewContainer.style.display = 'block';
        generatorForm.style.display = 'none';
        generationStatus.style.display = 'none';
        generationResult.style.display = 'none';
        
        // Scroll para a visualização
        previewContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    function showDeleteConfirmation(id) {
        currentDocId = id;
        deleteModal.style.display = 'block';
    }
    
    function deleteDocument(id) {
        fetch(`/api/documents/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao excluir documento');
            }
            return response.json();
        })
        .then(data => {
            // Fechar modal
            deleteModal.style.display = 'none';
            
            // Recarregar histórico
            loadHistory();
            
            // Mostrar mensagem de sucesso
            alert('Documento excluído com sucesso!');
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao excluir o documento.');
            deleteModal.style.display = 'none';
        });
    }
    
    function simulateProgress() {
        const progressBar = document.querySelector('.progress-bar');
        let width = 0;
        const interval = setInterval(function() {
            if (width >= 90) {
                clearInterval(interval);
            } else {
                width += Math.random() * 10;
                if (width > 90) width = 90;
                progressBar.style.width = width + '%';
                progressBar.textContent = Math.round(width) + '%';
            }
        }, 500);
    }
    
    function getDocTypeName(docType) {
        const types = {
            'ebook': 'eBook',
            'guia_pratico': 'Guia Prático',
            'dicas': 'Dicas',
            'documento_oficial': 'Documento Oficial'
        };
        return types[docType] || docType;
    }
    
    function getAIModelName(aiModel) {
        const models = {
            'openai': 'OpenAI (GPT)',
            'anthropic': 'Anthropic (Claude)',
            'gemini': 'Google Gemini'
        };
        return models[aiModel] || aiModel;
    }
    
    function getLanguageName(language) {
        const languages = {
            'pt-BR': 'Português',
            'en-US': 'Inglês'
        };
        return languages[language] || language;
    }
});
