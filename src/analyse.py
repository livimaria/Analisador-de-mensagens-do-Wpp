import pandas as pd
import re
import plotly.express as px

# -----------------------------------------------------------
# 1) LIMPEZA DO TEXTO
# -----------------------------------------------------------
def limpar_texto(txt):
    if pd.isna(txt):
        return ""
    txt = str(txt).strip()
    txt = re.sub(r"\s+", " ", txt)
    return txt


# -----------------------------------------------------------
# 2) CLASSIFICAÇÃO DAS MENSAGENS
# -----------------------------------------------------------
def classificar_mensagem(texto):
    texto = str(texto).lower()

    palavras_consulta = [
        "consulta", "consultar", "agendar", "agenda", "marcar",
        "retorno", "acompanhamento", "avaliação", "parecer",
        "médico", "medico", "doutor", "dr.", "dr "
    ]

    palavras_exame = [
        "exame", "resultado", "laudo", "ultrassom", "ecg",
        "hemograma", "tomografia", "ressonância", "rx"
    ]

    palavras_cirurgia = [
        "cirurgia", "procedimento", "operação",
        "internação", "internacao"
    ]

    if any(p in texto for p in palavras_consulta):
        return "Consulta"
    elif any(p in texto for p in palavras_exame):
        return "Exame"
    elif any(p in texto for p in palavras_cirurgia):
        return "Cirurgia"
    else:
        return "Outros"


# -----------------------------------------------------------
# 3) GRÁFICO PROFISSIONAL (CORES POR CATEGORIA)
# -----------------------------------------------------------
def gerar_grafico_categorias(df):
    contagem = df["categoria"].value_counts().reset_index()
    contagem.columns = ["categoria", "quantidade"]

    cores = {
        "Consulta": "#1f77b4",
        "Exame": "#2ca02c",
        "Cirurgia": "#d62728",
        "Outros": "#7f7f7f"
    }

    fig = px.bar(
        contagem,
        x="categoria",
        y="quantidade",
        color="categoria",
        color_discrete_map=cores,
        text="quantidade",
        title="Distribuição de Mensagens por Categoria"
    )

    fig.update_layout(
        template="simple_white",
        font=dict(size=16),
        showlegend=True,
        legend_title_text="Categorias",
        title_x=0.5
    )

    fig.update_traces(textposition="outside")
    return fig


# -----------------------------------------------------------
# 4) FUNÇÃO PRINCIPAL DE ANÁLISE
# -----------------------------------------------------------
def analisar_dataframe(df):
    # padroniza para "mensagem"
    df.rename(columns={"texto": "mensagem"}, inplace=True)

    df["mensagem"] = df["mensagem"].apply(limpar_texto)
    df["categoria"] = df["mensagem"].apply(classificar_mensagem)
    return df
