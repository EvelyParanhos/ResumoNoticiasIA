import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

from noticias import pegar_noticias_do_dia
from resumo import resumir_texto
from filtro import filtrar_noticias

load_dotenv()

REMETENTE_EMAIL = os.getenv("REMETENTE_EMAIL")
REMETENTE_SENHA = os.getenv("REMETENTE_SENHA")
DESTINATARIO_EMAIL = os.getenv("DESTINATARIO_EMAIL")


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 # Porta padrão TLS


url = "https://g1.globo.com/dynamo/tecnologia/rss2.xml"


def enviar_email(assunto, corpo_html):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = REMETENTE_EMAIL
        msg['To'] = DESTINATARIO_EMAIL

        # Anexa o corpo HTML
        msg.attach(MIMEText(corpo_html, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Usa criptografia TLS
            server.login(REMETENTE_EMAIL, REMETENTE_SENHA)
            server.sendmail(REMETENTE_EMAIL, DESTINATARIO_EMAIL, msg.as_string())
        
        print("✅ Email enviado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email. Verifique as credenciais e a Senha de App: {e}")
        return False


if __name__ == "__main__":
    
    # 1. Obter e filtrar notícias
    noticias = pegar_noticias_do_dia(url)
    noticias_filtradas = filtrar_noticias(noticias)
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    # --- CONSTRUÇÃO DO CORPO DO EMAIL ---
    
    if not noticias_filtradas:
        print("Nenhuma notícia de tecnologia encontrada hoje.")
        assunto = f"Filtro de Notícias Diário ({data_hoje}): Nenhuma notícia encontrada"
        corpo_html = f"<h1>Nenhuma notícia de tecnologia relevante foi encontrada hoje, {data_hoje}.</h1>"
        enviar_email(assunto, corpo_html)
        exit()
        
    # Início do HTML do email
    corpo_html = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                .noticia {{ margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px dashed #eee; }}
                .titulo {{ color: #0056b3; font-size: 1.3em; margin-bottom: 8px; }}
                .resumo {{ margin-top: 5px; }}
                .link {{ color: #28a745; text-decoration: none; font-weight: bold; }}
                hr {{ border: 0; border-top: 1px solid #eee; }}
            </style>
        </head>
    <body>
        <div class="container">
            <h1>📰 Seu Resumo Diário de Notícias de Tecnologia ({data_hoje})</h1>
            <p>Encontradas {len(noticias_filtradas)} notícias relevantes.</p>
            <hr>
    """
    
    # 2. Iterar e adicionar cada notícia ao corpo HTML
    for noticia in noticias_filtradas:
        # A função resumir_texto é custosa. Executa aqui.
        resumo = resumir_texto(noticia.summary)
        
        corpo_html += f"""
        <div class="noticia">
            <h2 class="titulo">{noticia.title}</h2>
            <p class="resumo"><strong>📝 Resumo:</strong> {resumo}</p>
            <p><strong>🔗 Link:</strong> <a class="link" href="{noticia.link}">{noticia.link}</a></p>
        </div>
        """
        
    # Fechamento do HTML
    corpo_html += "</div></body></html>"
    
    # 3. Enviar o email
    assunto = f"Filtro de Notícias Diário ({len(noticias_filtradas)} Notícias) - {data_hoje}"
    enviar_email(assunto, corpo_html)