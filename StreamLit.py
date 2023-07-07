import streamlit as st
import pandas as pd
import pickle
from sklearn.base import BaseEstimator, TransformerMixin

class ItemSelector(BaseEstimator, TransformerMixin):    
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


with open(r'xgb.pickle', 'rb') as arquivo:    
 modelo_carregado = pickle.load(arquivo)

st.set_page_config(page_title='Modelo IDEB', page_icon="bar_chart:", layout='wide')

st.markdown('# Predição IDEB (Índice de Desenvolvimento da Educação Básica)')

st.markdown('###### Preencha os dados abaixo para saber se a escola possui chances de atingir um nível de IDEB adequado.')

container = st.container()

# Formulário para entrada de dados
with container:
    col1, col2 = st.columns(2)
    
    with col1:
        # st.header('Dados da Escola')

        # Dropdown dos estados do Brasil
        lista_estados = [
            'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo',
            'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba',
            'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul',
            'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
        ]
        estado = st.selectbox('Estado', lista_estados)

        lista_municipios = pd.read_csv(r'Municipios.csv')
        municipio = st.selectbox('Município', lista_municipios.values.flatten())

        lista_localizacao = ['urbana', 'rural']
        localizacao = st.selectbox('Localização', lista_localizacao)

        lista_rede = ['estadual', 'federal', 'municipal']
        rede = st.selectbox('Tipo de Escola', lista_rede)

        ideb = st.number_input('Nota IDEB', min_value=0.0, max_value=10.0, value=0.0)

    with col2:

        lista_complexidade = ['Nível ' + str(num + 1) for num in range(6)]
        complexidade = st.selectbox('Complexidade (Indicador baixo indica facilidade na gestão da escola)', lista_complexidade)

        regularidade_docente = st.number_input('Regularidade de Formação Docente (Formação condizente com aulas ministradas)', min_value=0.0, max_value=5.0, value=0.0)

        inse = st.number_input('INSE', min_value=0.0, max_value=10.0, value=0.0)

        lista_classificacao = ['Nível I', 'Nível II', 'Nível III', 'Nível IV', 'Nível V', 'Nível VI', 'Nível VII']
        classificacao = st.selectbox('Nível de Classificação Socioeconômico (Indicador baixo indica maior pobreza)', lista_classificacao)

        aluno_turma = st.number_input('Média de Alunos por Turma')

amostra = {'uf':[estado]
           ,'municipio':[municipio]
           ,'localizacao':[localizacao]
           ,'rede':[rede]
           ,'ideb':[ideb]
           ,'Regularidade.Formação.Docente':[regularidade_docente]
           ,'inse':[inse]
           ,'classificacao':[classificacao]
           ,'fun_af_cat_0':[aluno_turma]}

df_amostra = pd.DataFrame.from_dict(amostra)

if st.button('Fazer Predição'):
    predicao = modelo_carregado.predict(df_amostra)
    if predicao <= 0:
        resultado_predicao = 'SIM'
    else:
        resultado_predicao = 'NÃO'
    
    st.header('Resultado da Predição')
    st.write('A escola tem chances de atingir um nível adequado no IDEB:', resultado_predicao)