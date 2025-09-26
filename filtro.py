def filtrar_noticias(noticias):
    
    noticias_filtradas = []

    palavras_chave = [
        "tecnologia", "ia", "inteligência artificial", "robótica", "machine learning",
        "computação", "tech", "programação", "inovação"
    ]

    for noticia in noticias:
        titulo = noticia.title.lower()
        resumo = noticia.summary.lower()
        if any(palavra in titulo or palavra in resumo for palavra in palavras_chave):
            noticias_filtradas.append(noticia)
    return noticias_filtradas

