# 📰 ResumoNoticiasAI: Filtro e Sumarizador de Notícias de Tecnologia

Este projeto é um pipeline automatizado que busca diariamente as notícias mais recentes de um feed RSS de tecnologia, filtra o conteúdo por palavras-chave relevantes, utiliza Inteligência Artificial para gerar resumos concisos e, por fim, envia um relatório formatado em HTML diretamente para o seu e-mail.

## 🚀 Funcionalidades

- **Busca de Notícias**: Utiliza feedparser para consumir feeds RSS (atualmente do G1 - Tecnologia).
- **Filtragem Inteligente**: Filtra notícias com base em uma lista de palavras-chave (IA, Machine Learning, Programação, etc.).
- **Sumarização por IA**: Usa o modelo de deep learning facebook/bart-large-cnn (via biblioteca transformers) para gerar resumos de alta qualidade.
- **Entrega Diária**: Envia o resumo consolidado por e-mail com formatação HTML.
- **Segurança**: Utiliza variáveis de ambiente (.env) para gerenciar credenciais de e-mail.

## 💻 Configuração do Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente.

### 1. Pré-requisitos

- Python 3.8+
- Ter um ambiente virtual ativo (venv).

### 2. Instalação de Dependências

O projeto requer várias bibliotecas, incluindo a Hugging Face transformers e o framework PyTorch (torch) para o modelo de sumarização.

```bash
# Ative seu ambiente virtual se ainda não o fez
# source venv/bin/activate  (Linux/macOS)
# venv\Scripts\activate     (Windows)

# Instale as bibliotecas necessárias
pip install feedparser transformers torch python-dotenv
```

### 3. Configuração de Variáveis de Ambiente (.env)

Para proteger suas credenciais e garantir o envio de e-mail, crie um arquivo chamado `.env` na raiz do projeto e preencha com as informações abaixo.

⚠️ **Atenção**: Para provedores como Gmail, você deve usar uma Senha de App (App Password) no campo `REMETENTE_SENHA`, e não sua senha principal.

```env
# Configurações de E-mail
REMETENTE_EMAIL="seu_email@gmail.com"
REMETENTE_SENHA="SUA_SENHA_DE_APP_DE_16_CARACTERES" 
DESTINATARIO_EMAIL="email_que_recebera_as_noticias@exemplo.com"

# Configurações SMTP (Se estiver usando outro provedor, ajuste aqui)
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
```

### 4. Estrutura de Arquivos

Certifique-se de que seus arquivos estejam organizados da seguinte forma:

```
ResumoNoticiasAI/
├── /venv               # Ambiente virtual do Python
├── .env
├── main.py             # Orquestra o processo e envia o e-mail
├── noticias.py         # Busca e filtra notícias por data 
├── filtro.py           # Filtra notícias por palavra-chave
├── resumo.py           # Sumariza o texto usando IA
└── README.md           # Este arquivo
```

## ▶️ Execução do Script

Para testar o pipeline e garantir que o e-mail está sendo enviado corretamente, execute o arquivo principal:

```bash
python main.py
```

A primeira execução pode demorar, pois o modelo de sumarização (BART-large-cnn) será baixado.

Você verá mensagens de console sobre o progresso e uma confirmação de envio (✅ Email enviado com sucesso!).

## ⏱️ Agendamento Diário (Automação)

Para receber o e-mail diariamente, você precisa agendar a execução do script no seu sistema operacional.

### ⚙️ Windows (Agendador de Tarefas)

- Abra o Agendador de Tarefas (Task Scheduler).
- Crie uma nova Tarefa Básica e defina um gatilho Diário (ex: 9:00 AM).
- Na Ação, escolha Iniciar um programa.
- **Programa/Script**: O caminho completo para o seu executável Python (C:\path\to\venv\Scripts\python.exe).
- **Adicione Argumentos**: O caminho completo para o main.py (C:\path\to\ResumoNoticiasAI\main.py).

### ⚙️ Linux/macOS (Crontab)

Abra o editor do crontab: `crontab -e`

Adicione a linha para executar o script no horário desejado (ex: todos os dias às 9:00):

```bash
# Substitua o caminho completo pelo seu local real
0 9 * * * /caminho/completo/para/venv/bin/python /caminho/completo/para/main.py
```

## ⚠️ Observações de Performance

O arquivo `resumo.py` utiliza o modelo facebook/bart-large-cnn, que é um modelo grande de deep learning.

- **CPU**: A sumarização é feita na CPU (device=-1). Este processo pode consumir muitos recursos e levar alguns segundos por notícia.
- **GPU**: Se você tiver uma placa de vídeo NVIDIA com drivers CUDA configurados, você pode potencialmente acelerar o processo. Basta mudar o parâmetro device=-1 para device=0 (para usar a primeira GPU) no arquivo `resumo.py`.
