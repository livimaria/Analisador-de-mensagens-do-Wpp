import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_dataframe(df):
    # garante que a coluna exista mesmo se vier com outro nome
    df = df.rename(columns={
        "text": "mensagem",
        "message": "mensagem",
        "conteudo": "mensagem",
        "texto": "mensagem"
    })

    df["mensagem"] = df["mensagem"].apply(clean_text)

    if "remetente" in df.columns:
        df["remetente"] = df["remetente"].fillna("Desconhecido")

    df = df[df["mensagem"] != ""]
    df = df.drop_duplicates()

    return df
