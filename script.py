import streamlit as st
import pandas as pd
from src.analyse import analisar_dataframe, gerar_grafico_categorias
from src.extract import extract_json, extract_csv
from src.clean import clean_dataframe
from src.export import export_to_word

st.set_page_config(page_title="Ecardio | Analisador", page_icon="logo.png")

st.title("Analisador de Mensagens – Ecardio")

uploaded_files = st.file_uploader(
    "Envie arquivos JSON ou CSV",
    type=["json", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []

    for f in uploaded_files:
        if f.name.endswith(".json"):
            dfs.append(extract_json(f))
        else:
            dfs.append(extract_csv(f))

    df = pd.concat(dfs, ignore_index=True)

    st.success("Arquivos carregados com sucesso!")

    # LIMPEZA
    df = clean_dataframe(df)

    # CLASSIFICAÇÃO + TEXTO LIMPO
    df = analisar_dataframe(df)

    st.subheader("Pré-visualização")
    st.dataframe(df.head(50), use_container_width=True)

    # DEBUG opcional — para ver se a categoria existe
    st.write("Contagem de categorias detectadas:")
    st.write(df["categoria"].value_counts())

    # GRÁFICO
    st.subheader("📊 Distribuição de Categorias")
    fig = gerar_grafico_categorias(df)
    st.plotly_chart(fig, use_container_width=True)

    # EXPORTAÇÃO
    if st.button("Gerar relatório em Word"):
        output_path = export_to_word(df, "relatorio.docx")

        with open(output_path, "rb") as f:
            st.download_button(
                label="📄 Baixar Relatório",
                data=f,
                file_name="relatorio.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
