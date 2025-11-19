import re

CATEGORIAS = {
    "Consulta": [
        "consulta", "retorno", "consultar", "agendar médico",
        "agendamento", "consulta médica", "voltar com o médico",
        "revisão", "acompanhamento", "dr.", "doutor", "médico"
    ],
    "Exame": [
        "exame", "resultado", "laudo", "ultrassom", "ultrasom",
        "tomografia", "ressonância", "eco", "eletro", "holter",
        "mapa", "teste", "laboratório", "lab", "coleta", "imagem"
    ],
    "Cirurgia": [
        "cirurgia", "procedimento", "operação", "operar",
        "pré-operatório", "pós-operatório", "cirúrgico"
    ]
}


def classificar_msg(texto):
    texto = texto.lower()

    for categoria, termos in CATEGORIAS.items():
        for termo in termos:
            if termo in texto:
                return categoria

    return "Outros"


def aplicar_classificacao(df):
    df["categoria"] = df["mensagem"].apply(classificar_msg)
    return df
