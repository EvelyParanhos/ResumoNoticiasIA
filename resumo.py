import re
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # device=-1 força usar CPU

def resumir_texto(texto, max_length=130, min_length=30):

    if not texto:
        return "Texto vazio."

    # Remove tags HTML
    texto = re.sub(r'<.*?>', '', texto)

    # Remove links
    texto = re.sub(r'http\S+', '', texto)

    # Remove espaços extras
    texto = texto.strip()

    # Limita tamanho máximo do input para evitar erros
    MAX_INPUT_CHARS = 1000
    texto = texto[:MAX_INPUT_CHARS]

    # Ajusta max_length para não ultrapassar tamanho do texto
    max_len = min(len(texto), max_length)

    try:
        resumo = summarizer(texto, max_length=max_len, min_length=min_length, do_sample=False)
        return resumo[0]['summary_text']
    except Exception as e:
        return f"[Erro ao resumir]: {e}"
