import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# url do app.py (tem que rodar o app.py antes de rodar o streamlit_app.py) 
BASE_URL = "http://localhost:8000"

def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao acessar {endpoint}: {response.status_code}")
        return []

def send_post_request(endpoint, params):
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.status_code == 200

def decision_page():
    st.header("📊 Invest+")

    assets = fetch_data("/assets")
    categories = fetch_data("/categories")
    indicators = fetch_data("/indicators")
        
    if not assets or not categories or not indicators:
        st.warning("Não foi possível carregar dados de ativos, categorias ou indicadores.")
        return

    asset_options = {asset["name"]: asset["id"] for asset in assets}
    category_options = {category["name"]: category["id"] for category in categories}

    asset_category_map = {asset["id"]: asset["category_id"] for asset in assets}
    category_map = {category["id"]: category["name"] for category in categories}

    selected_assets = st.multiselect("Selecione um ou mais ativos:", options=asset_options.keys())
    selected_categories = st.multiselect("Selecione uma ou mais categorias:", options=category_options.keys())

    if selected_assets:
        selected_asset_ids = [asset_options[name] for name in selected_assets]
        indicators = [indicator for indicator in indicators if indicator["asset_id"] in selected_asset_ids]
    
    if selected_categories:
        selected_category_ids = [category_options[name] for name in selected_categories]
        indicators = [indicator for indicator in indicators if asset_category_map[indicator["asset_id"]] in selected_category_ids]
    
    if assets:
        df_assets = pd.DataFrame(assets)
        
        category_map = {category["id"]: category["name"] for category in categories}
        df_assets["category_name"] = df_assets["category_id"].map(category_map)  

        df_assets.index = range(1, len(df_assets) + 1)

    if indicators:
        df_indicators = pd.DataFrame(indicators)

        asset_map = {asset["id"]: asset["name"] for asset in assets}
        df_indicators["asset_name"] = df_indicators["asset_id"].map(asset_map)

        df_indicators.index = range(1, len(df_indicators) + 1)

        cols = st.columns(2)
        with cols[0]:
            st.write("Tabela de Ativos")
            st.dataframe(df_assets)

        with cols[1]:
            st.write("Tabela de Indicadores Filtrados")
            st.dataframe(df_indicators)

        numeric_indicators = df_indicators[df_indicators["value"].apply(lambda x: isinstance(x, (int, float)))] 

        if not numeric_indicators.empty:
            num_columns = len(numeric_indicators["name"].unique())
            columns = st.columns(num_columns)

            for idx, indicator in enumerate(numeric_indicators["name"].unique()):
                indicator_data = numeric_indicators[numeric_indicators["name"] == indicator]
                color_map = {name: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                             for i, name in enumerate(selected_assets)}
                fig = px.bar(
                    indicator_data,
                    x="name",
                    y="value",
                    color="asset_name",
                    barmode="group",
                    title=f"Indicador: {indicator}",
                    labels={"asset_name": "Companhia", "value": "Valor", "name": "Indicador"},
                    color_discrete_map=color_map
                )
                columns[idx].plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum indicador numérico encontrado.")
    else:
        st.warning("Nenhum indicador encontrado para os filtros aplicados.")

# Gerenciamento
def manage_page():
    st.header("📋 Gerenciar Ativos e Indicadores")
    
    categories_placeholder = st.expander("🗂️ Categorias")
    categories = fetch_data("/categories")
    if categories:
        with categories_placeholder:
            st.write("Categorias Disponíveis")
            df_categories = pd.DataFrame(categories)
            st.dataframe(df_categories)

    with st.form("Nova Categoria"):
        category_name = st.text_input("Nome da Categoria")
        description = st.text_input("Descrição")
        if st.form_submit_button("Adicionar Categoria"):
            if send_post_request("/categories/new", {"name": category_name, "description": description}):
                st.success("Categoria adicionada com sucesso.")
                categories = fetch_data("/categories")
                if categories:
                    df_categories = pd.DataFrame(categories)
                    st.dataframe(df_categories)
            else:
                st.error("Erro ao adicionar categoria.")

    assets_placeholder = st.expander("🏢 Ativos")
    assets = fetch_data("/assets")
    if assets:
        with assets_placeholder:
            st.write("Ativos Disponíveis")
            df_assets = pd.DataFrame(assets)
            st.dataframe(df_assets)

    with st.form("Novo Ativo"):
        name = st.text_input("Nome")
        type_ = st.text_input("Tipo")
        category = st.selectbox("Categoria", options={category["name"]: category["id"] for category in categories})
        if st.form_submit_button("Adicionar Ativo"):
            if send_post_request("/assets/new", {"name": name, "type": type_, "category": category}):
                st.success("Ativo adicionado com sucesso.")
                assets = fetch_data("/assets")
                if assets:
                    df_assets = pd.DataFrame(assets)
                    st.dataframe(df_assets)
            else:
                st.error("Erro ao adicionar ativo.")

    indicators_placeholder = st.expander("📈 Indicadores")
    indicators = fetch_data("/indicators")
    if indicators:
        with indicators_placeholder:
            st.write("Indicadores Disponíveis")
            df_indicators = pd.DataFrame(indicators)
            st.dataframe(df_indicators)

    with st.form("Novo Indicador"):
        name = st.text_input("Nome do Indicador")
        value = st.number_input("Valor", step=1.0)
        asset_id = st.selectbox("Ativo Relacionado", options={asset["id"]: asset["name"] for asset in assets})
        if st.form_submit_button("Adicionar Indicador"):
            if send_post_request("/indicators/new", {"name": name, "value": value, "asset_id": asset_id}):
                st.success("Indicador adicionado com sucesso.")
                indicators = fetch_data("/indicators")
                if indicators:
                    df_indicators = pd.DataFrame(indicators)
                    st.dataframe(df_indicators)
            else:
                st.error("Erro ao adicionar indicador.")

st.set_page_config(page_title="Sistema de Decisão", layout="wide")

tabs = {
    "Página Principal": decision_page,
    "Gerenciar Dados": manage_page
}

selected_tab = st.sidebar.selectbox("Navegação", list(tabs.keys()))
tabs[selected_tab]()
