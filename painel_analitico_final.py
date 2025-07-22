import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Painel Analítico sobre Obesidade", layout="wide")

df = pd.read_csv('Obesity.csv')

#Traduzindo o as opções de escolha para o português

dic_genero = {'Male':'Masculino','Female':'Feminino'}
dic_family_history = {"yes" : "sim","no" : "não"}
dic_FAVC = {"yes" : "sim","no" : "não"}
dic_caec = {"no" : "NÃO","Sometimes":"as vezes","Frequently":"frequentemente", "Always":"sempre"}
dic_smoke = {"yes" : "sim","no" : "não"}
dic_scc = {"yes" : "sim","no" : "não"}
dic_calc = {"no":"não" ,"Sometimes":"as vezes" , "Frequently":"frequentemente" , "Always":"sempre"}
dic_mtrans = {"Public_Transportation":"transporte público","Walking":"caminhada", "Automobile":"automóvel", "Motorbike":"motocicleta", "Bike":"bicicleta"}
dic_obesity = {
                "Normal_Weight": "Peso Normal",
                "Insufficient_Weight": "Peso Insuficiente",
                "Obesity_Type_I": "Obesidade Tipo I",
                "Obesity_Type_II": "Obesidade Tipo II",
                "Obesity_Type_III": "Obesidade Tipo III",
                "Overweight_Level_I": "Sobrepeso Nível I",
                "Overweight_Level_II": "Sobrepeso Nível II"}

df['Gender'] = df['Gender'].map(dic_genero)
df['family_history'] = df['family_history'].map(dic_family_history)
df['FAVC'] = df['FAVC'].map(dic_FAVC)
df['CAEC'] = df['CAEC'].map(dic_caec)
df['SMOKE'] = df['SMOKE'].map(dic_smoke)
df['SCC'] = df['SCC'].map(dic_scc)
df['CALC'] = df['CALC'].map(dic_calc)
df['MTRANS'] = df['MTRANS'].map(dic_mtrans)
df['Obesity'] = df['Obesity'].map(dic_obesity)



#Ajustando valor de colunas para representar numero inteiro
df['Age']=df['Age'].round(0)
df['Height']=df['Height'].round(2)
df['Weight']=df['Weight'].round(0)
df['NCP']=df['NCP'].round(0)
df['NCP']=df['NCP'].astype(int)
df['FCVC']=df['FCVC'].round(0)
df['FCVC']=df['FCVC'].astype(int)
#df['Age']=df['Age'].astype(int)
#df['FCVC']=pd.to_numeric(df['FCVC'])

df['ambos'] = 'Ambos'

#Dicionário das colunas 
#● Gender: Gênero.
#● Age: Idade.
#● Height:Altura em metros.
#● Weight: Peso em kgs.
#● family_history: Algum membro da família sofreu ou sofre de excesso de peso?
#● FAVC: Você come alimentos altamente calóricos com frequência?
#● FCVC: Você costuma comer vegetais nas suas refeições?
#● NCP: Quantas refeições principais você faz diariamente?
#● CAEC: Você come alguma coisa entre as refeições?
#● SMOKE: Você fuma?
#● CH2O: Quanta água você bebe diariamente?
#● SCC: Você monitora as calorias que ingere diariamente?
#● FAF: Com que frequência você pratica atividade física?
#● TER: Quanto tempo você usa dispositivos tecnológicos como celular, videogame, televisão, computador e outros?
#● CALC: Com que frequência você bebe álcool?
#● MTRANS: Qual meio de transporte você costuma usar?
#● Obesity_level (coluna alvo): Nível de obesidade

with st.sidebar:
        #st.title("Filtros")
        st.header("")
        st.write("")

st.header("📊 Painel Analítico sobre Obesidade")

st.markdown("A obesidade é uma doença crônica, progressiva, com causas multifatoriais associadas principalmente a estilo de vida (sedentarismo, hábitos alimentares inadequados) e também a outras condições, como fatores genéticos, hereditários, psicológicos, culturais e étnicos.")
st.markdown("*Fonte: https://abeso.org.br*")

st.subheader("Panorama Geral da Base Estudada")

st.metric('Quantidade total de pessoas', df['Gender'].count())

valor1 = 'Obesidade Tipo I'
valor2 = 'Obesidade Tipo II'
valor3 = 'Obesidade Tipo III'

total = df['Gender'].count()



col1, col2 = st.columns(2)

with col1:
    st.write("Informações Genero Maculino")
    st.metric('Quantidade', df['Gender'][df['Gender']=='Masculino'].count())
    
    df_masc_total = df[(df['Gender']=='Masculino')].count()
    df_masc_obesity = df[(df['Gender']=='Masculino') & (df['Obesity'] == valor1) | (df['Obesity'] == valor2) | (df['Obesity'] == valor3)]
    total_masc_obesity = df_masc_obesity['Obesity'].count()
    perc_masc_obesity = (total_masc_obesity / df_masc_total)*100

    df_filterM = df[df['Gender']=='Masculino']
    mediaPesoM = df_filterM['Weight'].mean()
    st.write(f"Média de peso: {mediaPesoM:.2f} Kg.")

    mediaIdadeM = df_filterM['Age'].mean()
    st.write(f"Média de idade: {mediaIdadeM:.0f} anos.")

    st.metric('Qtde. Obesos (Tipo I, II e III)', total_masc_obesity)

with col2:
    st.write("Informações Genero Feminino")
    st.metric('Quantidade', df['Gender'][df['Gender']=='Feminino'].count())

    df_fem_total = df[(df['Gender']=='Feminino')].count()
    df_fem_obesity = df[(df['Gender']=='Feminino') & (df['Obesity'] == valor1) | (df['Obesity'] == valor2) | (df['Obesity'] == valor3)]
    total_fem_obesity = df_fem_obesity['Obesity'].count()
    perc_fem_obesity = (total_fem_obesity / df_masc_total)*100
    

    df_filterF = df[df['Gender']=='Feminino']
    mediaPesoF = df_filterF['Weight'].mean()
    st.write(f"Média de peso: {mediaPesoF:.2f} Kg.")

    mediaIdadeF = df_filterF['Age'].mean()
    st.write(f"Média de idade: {mediaIdadeF:.0f} anos.")

    st.metric('Qtde. Obesos (Tipo I, II e III)', total_fem_obesity)


st.markdown("Os números gerais acima já indicam que 75% das pessoas estudadas de ambos os generos estão obesos.")

#filtro de genero
genero_escolhido = st.sidebar.multiselect('Selecione um genero ou ambos :',df['Gender'].unique(),df['Gender'].unique())

if genero_escolhido == 'Feminino' and 'Masculino':
    df_filtrado = df.loc[(df['Gender']=='Feminino') & (df['Gender']=='Masculino')]
else:
    df_filtrado = df.loc[df['Gender'].isin(genero_escolhido)]


hist = px.histogram(data_frame=df_filtrado, x='Age', title="Histograma por Idade", labels={'Age' : 'idade'})
st.plotly_chart(hist, key='plot1')

st.markdown("Nota-se que a base é constituída em grande parte de pessoas mais jovens (entre 17 e 26 anos).")
st.markdown("No gráfico seguinte é possível observar uma elevação quase que constante de peso após os 16 anos.")

mediaPeso = df_filtrado.groupby('Age')['Weight'].mean().reset_index()
fig1 = px.line(mediaPeso,x='Age',y='Weight',
             title = 'Média de peso por idade', 
             labels={'Weight' : 'Peso', 'Age': 'Idade'})
fig1.update_layout(barmode='group')
st.plotly_chart(fig1, key='plot3')


st.markdown("No gráfico seguinte vemos que grande parte as pessoas mais jovens estão obesas.")
df_contagem_obesity = df_filtrado.groupby(['Age','Obesity']).size().reset_index(name='Quantidade')
st.bar_chart(df_contagem_obesity,x='Obesity',y='Quantidade', color='Age',horizontal=True)


st.markdown("No gráfico seguinte observa-se um certo equilibrio entre os generos quanto a sobrepeso e obesidade na população da base analisada, porém um detalhe chama a atenção há uma concentração de pessoas em um tipo de obesidade, no feminino obesidade tipo III e no masculino obesidade tipo II.")
df_contagem_obesity = df_filtrado.groupby(['Gender','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='Gender',
             title = 'Classificação por genero', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'Gender' : 'Genero'})
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot2')          


st.subheader("Características e Hábitos")

st.markdown("Grande parte das pessoas com sobrepeso e obesidade consomem frequentemente alimentos altamente calóricos conforme observa-se no gráfico a seguir.")
st.markdown("Esses alimentos, ricos em gorduras e açúcares, muitas vezes são processados ou ultraprocessados, com baixo valor nutricional e alta densidade calórica.") 

df_contagem_obesity = df_filtrado.groupby(['FAVC','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='FAVC',
             title = 'Você come alimentos altamente calóricos com frequência?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'FAVC' : 'Resposta'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot4')

st.markdown("No gráfico abaixo, identificamos que mesmo as pessoas com peso insuficiente, tem o hábito de fazer 3 refeições diárias, o que pode ser um indício a que a qualidade das refeições destas pessoas não suprem a necessidade nutricional.")
df_contagem_obesity = df_filtrado.groupby(['NCP','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='NCP',
             title = 'Quantas refeições principais você faz diariamente?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'NCP' : 'Qtd de refeições'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot5')

st.markdown("O gráfico abaixo nos mostra que a maioria das pessoas com alguma obesidade ou sobrepeso as vezes consomem algo entre as refeições")
st.markdown("Nos demais tipos, peso normal e insuficiente, curiosamente tem um grupo de pessoas que responderam que consomem algo frequentemente, no peso normal a maioria são do genero masculino e no insuficiente o feminino.")
df_contagem_obesity = df_filtrado.groupby(['CAEC','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='CAEC',
             title = 'Você come alguma coisa entre as refeições?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'CAEC' : 'Resposta'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot6')


st.markdown("O consumo de vegetais nas refeições, está bem distribuído entre os tipos de obesidade, portanto não há uma relação direta com algum perfil em especifico.")
df_contagem_obesity = df_filtrado.groupby(['FCVC','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='FCVC',
             title = 'Você costuma comer vegetais nas suas refeições?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'FCVC' : 'Qtd de vezes'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot7')

st.markdown("Abaixo observamos uma relação, quanto maior a obesidade (tipo I, II, III), maior a quantidade de pessoas que consomem alcool esporadicamente (as vezes).")
df_contagem_obesity = df_filtrado.groupby(['CALC','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='CALC',
             title = 'Com que frequencia você bebe alcool?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'CALC' : 'Resposta'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot8')

st.markdown("Aparentemente o consumo de cigarros não representa uma caracteristica de nenhum tipo de obesidade.")
df_contagem_obesity = df_filtrado.groupby(['SMOKE','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='SMOKE',
             title = 'Você fuma?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'SMOKE' : 'Resposta'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig,key='plot9')

st.markdown("A maioria das das pessoas com algum tipo de sobrepeso ou obesidade possuem historico familias com membros com obesidade ou sobrepeso.")
df_contagem_obesity = df_filtrado.groupby(['family_history','Obesity']).size().reset_index(name='valor')
fig = px.bar(df_contagem_obesity,x='Obesity',y='valor', color='family_history',
             title = 'Algum membro da família sofreu ou sofre de excesso de peso?', 
             labels={'valor' : 'Quantidade de pessoas', 'Obesity': 'Classificação', 'family_history' : 'Resposta'},)
fig.update_layout(barmode='group')
st.plotly_chart(fig, key='plot10')



st.subheader("Base Completa com filtro por Nível de Obesidade")

tipo_obeso = st.selectbox('Classificação :',df['Obesity'].unique())
df_filtrado_obeso = df.loc[df['Obesity']==tipo_obeso]


df_filtrado_obeso = df_filtrado_obeso.rename(columns={
     'Gender':'Genero',
     'Age':'Idade',
     'Height':'Altura',
     'Weight': 'Peso',
     'family_history': 'Histórico Familiar',
     'FAVC':'Consome alimentos altamente caloricos?',
     'FCVC':'Consome vegetais?',
     'NCP':'Qtde. refeições principais diárias',
     'CAEC':'Come alguma coisa entre as refeições?',
     'SMOKE':'Fuma?',
     'CH2O':'Quanta água você bebe diariamente?',
     'SCC':'Monitora as calorias?',
     'FAF':'Frequencia atividade física',
     'TUE':'Tempo de uso de dispositivos tecnologicos',
     'CALC':'Com que freq. bebe alcool?',
     'MTRANS':'Tipo de Transporte que mais usa',
     'Obesity':'Obesidade'
})

df_base = df_filtrado_obeso.drop([
     'ambos',
     'Obesidade'
],axis=1)

st.dataframe(df_base)

st.subheader("Conclusão:")
st.markdown("Com base nos números e gráficos apresentados acima podemos concluir que a obesidade está muito presente principalmente na população mais jovem, de acordo com projeção realizada pela Comissão Lancet* sobre saúde e bem-estar dos adolescentes, cerca de 464 milhões de adolescentes do mundo terão sobrepeso ou obesidade até 2030. " \
" Os hábitos diários e histórico familiar também estão diretamente relacionados a existência de obesidade e sobrepeso. O acompanhamento médico, do estilo de vida, dos hábitos alimentares e a conscientização sobre os riscos é crucial para combater a obesidade. " \
"Além disso, no caso dos adolescentes, o apoio familiar também se mostra muito importante. " \
"Em alguns casos, intervenções como medicamentos ou cirurgia bariátrica pode ser necessário. " \
"Portanto, é importante avaliar a melhor estratégia para cada indivíduo e lidar com as causas e consequências da obesidade. " \
"")

st.markdown("**Referência: https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(25)00397-6/fulltext*")
