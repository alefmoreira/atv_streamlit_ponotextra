import pandas as pd
import streamlit as st
import plotly.express as px

# Carregamento do arquivo CSV
csv_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if csv_file is not None:
    csv_file = pd.read_csv(csv_file, sep=';', encoding='latin1')
else:
    csv_file = pd.read_csv('consulta_cand_2024_CE.csv', sep=';', encoding='latin1')

# Manter estado dos filtros no Streamlit
if 'nm_ue' not in st.session_state:
    st.session_state.nm_ue = None
if 'cargo' not in st.session_state:
    st.session_state.cargo = None

# Configurações de filtro na barra lateral
st.sidebar.title('Filtros')
st.sidebar.write('Selecione uma unidade Eleitoral')
nm_ue = st.sidebar.selectbox('Unidade Eleitoral', [''] + list(csv_file['NM_UE'].unique()), index=0)
st.write(f'Unidade Eleitoral selecionada: {nm_ue}')

st.sidebar.write('Selecione um Cargo')
cargo = st.sidebar.selectbox('Cargo', [''] + list(csv_file['DS_CARGO'].unique()), index=0)
st.write(f'Cargo selecionado: {cargo}')

# Botão para limpar filtros
if st.sidebar.button('Limpar Filtros'):
    st.session_state.nm_ue = None
    st.session_state.cargo = None
    nm_ue = ''
    cargo = ''

# Filtrando os dados conforme os filtros aplicados
filtered_df = csv_file
if nm_ue:
    filtered_df = filtered_df[filtered_df['NM_UE'] == nm_ue]
if cargo:
    filtered_df = filtered_df[filtered_df['DS_CARGO'] == cargo]

# Títulos e prévia dos dados
st.title('Dashboard de Análise dos Candidatos')
st.subheader('Prévia dos Dados Filtrados')
st.write(filtered_df.head())

# Análise por gênero
st.subheader('Distribuição de Candidatas Femininas por Partido')
feminino_df = filtered_df.query('DS_GENERO == "FEMININO"')
contagem_partido = feminino_df['SG_PARTIDO'].value_counts().reset_index()
contagem_partido.columns = ['SG_PARTIDO', 'count']
fig = px.bar(contagem_partido, x='SG_PARTIDO', y='count', color='count', 
             color_continuous_scale='Bluered', title='Número de Candidatas Femininas por Partido')
st.plotly_chart(fig)

st.subheader('Distribuição de Candidatos Masculinos por Partido')
masculino_df = filtered_df.query('DS_GENERO == "MASCULINO"')
contagem_partido = masculino_df['SG_PARTIDO'].value_counts().reset_index()
contagem_partido.columns = ['SG_PARTIDO', 'count']
fig = px.bar(contagem_partido, x='SG_PARTIDO', y='count', color='count', 
             color_continuous_scale='Portland', title='Número de Candidatos Masculinos por Partido')
st.plotly_chart(fig)

# Gráficos de distribuição
st.subheader('Distribuição da Cor/Raça entre os Candidatos')
fig_pie = px.pie(filtered_df, names='DS_COR_RACA', color_discrete_sequence=px.colors.sequential.RdBu, 
                 title='Distribuição Percentual da Cor/Raça dos Candidatos')
st.plotly_chart(fig_pie)

st.subheader('Distribuição de Gênero entre os Candidatos')
fig_pie = px.pie(filtered_df, names='DS_GENERO', color_discrete_sequence=px.colors.sequential.RdBu, 
                 title='Proporção de Gênero dos Candidatos')
st.plotly_chart(fig_pie)

st.subheader('Nível de Instrução dos Candidatos')
fig = px.histogram(filtered_df, x='DS_GRAU_INSTRUCAO', color_discrete_sequence=['#FFA07A'], 
                   title='Distribuição do Grau de Instrução entre os Candidatos')
st.plotly_chart(fig)

st.subheader('Comparação de Gênero por Grau de Instrução')
fig = px.histogram(filtered_df, x='DS_GRAU_INSTRUCAO', color='DS_GENERO', color_discrete_sequence=px.colors.qualitative.Set3, 
                   title='Relação entre Gênero e Grau de Instrução')
st.plotly_chart(fig)

st.subheader('Distribuição de Candidatos por Partido e Gênero')
fig = px.histogram(filtered_df, x='SG_PARTIDO', color='DS_GENERO', color_discrete_sequence=px.colors.cyclical.IceFire, 
                   title='Proporção de Candidatos Masculinos e Femininos por Partido')
fig.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig)
