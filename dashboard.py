import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Configuração do layout do Streamlit
st.set_page_config(page_title="Análise de Satisfação do Cliente", layout="wide")

# Função para carregar os dados e padronizar nomes das colunas
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/Customer_support_data.csv", parse_dates=["order_date_time"])
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")  # Padroniza nomes das colunas
    return df

# Carrega os dados
df = load_data()

# Verifica se a coluna 'csat_score' existe no dataset antes de continuar
if "csat_score" not in df.columns:
    st.error("⚠️ Erro: A coluna 'csat_score' não foi encontrada no dataset!")
else:
    st.success("✅ Coluna 'csat_score' encontrada! Gerando gráficos...")

    # Título do Dashboard
    st.title("📊 Análise de Satisfação do Cliente - E-commerce")

    # Criando filtros interativos
    agentes = df["agent_name"].unique().tolist()
    supervisores = df["supervisor"].unique().tolist()
    gerentes = df["manager"].unique().tolist()
    categorias = df["product_category"].unique().tolist()

    # Seção de Filtros na Barra Lateral
    st.sidebar.header("🔍 Filtros Interativos")
    agente_selecionado = st.sidebar.selectbox("Filtrar por Agente:", ["Todos"] + agentes)
    supervisor_selecionado = st.sidebar.selectbox("Filtrar por Supervisor:", ["Todos"] + supervisores)
    gerente_selecionado = st.sidebar.selectbox("Filtrar por Gerente:", ["Todos"] + gerentes)
    categoria_selecionada = st.sidebar.selectbox("Filtrar por Categoria de Produto:", ["Todos"] + categorias)

    # Aplicando filtros no DataFrame
    df_filtrado = df.copy()
    
    if agente_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["agent_name"] == agente_selecionado]

    if supervisor_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["supervisor"] == supervisor_selecionado]

    if gerente_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["manager"] == gerente_selecionado]

    if categoria_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado["product_category"] == categoria_selecionada]

    # Exibição de métricas principais
    st.header("📊 Métricas Gerais")
    col1, col2 = st.columns(2)
    col1.metric("📈 Média de Satisfação", round(df_filtrado["csat_score"].mean(), 2))
    col2.metric("📞 Total de Atendimentos", len(df_filtrado))

    # Seção 1: Relacionamento entre Gerente, Supervisor e Agente (Gráfico Sankey)
    def create_sankey(df):
        """Cria um diagrama Sankey para visualizar a relação entre Gerente, Supervisor e Agente."""
        gerentes = df["manager"].unique().tolist()
        supervisores = df["supervisor"].unique().tolist()
        agentes = df["agent_name"].unique().tolist()
        all_nodes = gerentes + supervisores + agentes
        node_indices = {name: i for i, name in enumerate(all_nodes)}

        links = {"source": [], "target": [], "value": []}

        for _, row in df.drop_duplicates(subset=["manager", "supervisor"]).iterrows():
            links["source"].append(node_indices[row["manager"]])
            links["target"].append(node_indices[row["supervisor"]])
            links["value"].append(1)

        for _, row in df.drop_duplicates(subset=["supervisor", "agent_name"]).iterrows():
            links["source"].append(node_indices[row["supervisor"]])
            links["target"].append(node_indices[row["agent_name"]])
            links["value"].append(1)

        fig = go.Figure(go.Sankey(
            node=dict(pad=20, thickness=20, line=dict(color="black", width=0.5), label=all_nodes),
            link=dict(source=links["source"], target=links["target"], value=links["value"])
        ))
        fig.update_layout(title_text="Relacionamento entre Gerente, Supervisor e Agente", font_size=10)
        return fig

    st.header("🔗 Relacionamento entre Gerente, Supervisor e Agente")
    if df_filtrado[["manager", "supervisor", "agent_name"]].dropna().shape[0] > 0:
        st.plotly_chart(create_sankey(df_filtrado), use_container_width=True)
    else:
        st.warning("⚠️ Dados insuficientes para exibir o gráfico de relacionamento.")

    # Seção 2: Performance da Equipe
    st.header("📊 Performance da Equipe (Gerente > Supervisor > Agente)")
    df_performance = df_filtrado.groupby(["manager", "supervisor", "agent_name"]).agg({
        "csat_score": "mean",
        "connected_handling_time": "mean"
    }).reset_index()

    # Adicionando manualmente a contagem de atendimentos por agente
    df_performance["total_atendimentos"] = df_filtrado.groupby(["manager", "supervisor", "agent_name"])["agent_name"].transform("count")

    st.dataframe(df_performance.sort_values(by="csat_score", ascending=False))

    # Seção 3: Análise Detalhada por Categoria de Produto
    st.header("📦 Análise Detalhada por Categoria de Produto")
    categoria_satisfacao = df_filtrado.groupby("product_category")[["csat_score", "connected_handling_time"]].mean().reset_index()
    st.dataframe(categoria_satisfacao.sort_values(by="csat_score", ascending=False))

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="product_category", y="csat_score", data=df_filtrado, palette="magma", ci=None, ax=ax)
    plt.xticks(rotation=45)
    plt.title("Satisfação Média por Categoria de Produto")
    plt.xlabel("Categoria do Produto")
    plt.ylabel("Média da Nota de Satisfação")
    st.pyplot(fig)

    # Seção 4: Exportação de Relatório em Excel
    st.header("📥 Exportar Dados")
    @st.cache_data
    def convert_df_to_excel(df):
        return df.to_csv(index=False).encode("utf-8")

    excel_data = convert_df_to_excel(df_filtrado)
    st.download_button(label="📂 Baixar Relatório em CSV", data=excel_data, file_name="relatorio_satisfacao.csv", mime="text/csv")

    st.markdown("**Criado por [Seu Nome]** 🚀")
