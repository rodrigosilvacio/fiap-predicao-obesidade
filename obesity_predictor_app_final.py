import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
st.set_page_config(page_title="Previsor de Obesidade", layout="wide")

# ======= Treinamento do Modelo (Pipeline completo) =======
@st.cache_resource
def treinar_pipeline():
    df = pd.read_csv("Obesity.csv")
    X = df.drop(columns=["Obesity"])
    y = df["Obesity"]

    numeric_features = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
    categorical_features = ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"]

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop='first', handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])

    pipeline.fit(X, y)
    return pipeline

# Treinar e salvar o modelo
modelo_pipeline = treinar_pipeline()
joblib.dump(modelo_pipeline, "random_forest_obesity_model.pkl")

# ======= Interface do App =======

st.title("🩺 Sistema Preditivo e Analítico de Obesidade")

st.markdown("Preencha os dados abaixo para obter uma previsão do nível de obesidade.")

# Entradas do usuário
with st.form("obesity_form"):
    genero_pt = st.selectbox("Gênero", ["Masculino", "Feminino"])
    dic_genero = {'Masculino' : 'Male','Feminino' : 'Female'}
    gender = dic_genero[genero_pt]

    age = st.slider("Idade", 10, 100, 25)
    height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, step=0.01)
    weight = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)

    historico_pt = st.selectbox("Histórico familiar de sobrepeso?", ["sim", "não"]) 
    dic_historico = {"sim" : "yes","não" : "no"}
    family_history = dic_historico[historico_pt]
 
    facv_pt = st.selectbox("Come alimentos muito calóricos com frequência?", ["sim", "não"])
    dic_facv = {"sim" : "yes","não" : "no"}
    favc = dic_facv[facv_pt]

    fcvc = st.slider("Frequência de vegetais na refeição (1-3)", 1.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais por dia", 1.0, 4.0, 3.0)

    caec_pt = st.selectbox("Petisca entre as refeições?", ["não", "as vezes", "frequentemente", "sempre"])
    dic_caec = {"não" : "no","as vezes" : "Sometimes", "frequentemente" : "Frequently", "sempre" : "Always"}
    caec = dic_caec[caec_pt]

    fuma_pt = st.selectbox("Fuma?", ["sim", "não"])
    dic_fuma = {"sim" : "yes","não" : "no"}
    smoke = dic_fuma[fuma_pt]

    ch2o = st.slider("Quantidade de água por dia (litros)", 1.0, 3.0, 2.0)

    scc_pt = st.selectbox("Monitora calorias ingeridas?", ["sim", "não"])
    dic_scc = {"sim" : "yes","não" : "no"}
    scc = dic_scc[scc_pt]


    faf = st.slider("Frequência de atividade física (horas/semana)", 0.0, 5.0, 1.0)
    tue = st.slider("Tempo de tela diário (horas)", 0.0, 5.0, 1.0)

    calc_pt = st.selectbox("Consumo de álcool", ["não", "as vezes", "frequentemente", "sempre"])
    dic_calc = {"não" : "no","as vezes" : "Sometimes", "frequentemente" : "Frequently", "sempre" : "Always"}
    calc = dic_calc[calc_pt]

    m_trans_pt = st.selectbox("Meio de transporte", ["transporte público", "caminhada", "automóvel", "motocicleta", "bicicleta"])
    dic_m_trans = {"transporte público" : "Public_Transportation","caminhada" : "Walking", "automóvel" : "Automobile", "motocicleta" : "Motorbike", "bicicleta" : "Bike"}
    mtrans = dic_m_trans[m_trans_pt]


    submitted = st.form_submit_button("Prever")

    if submitted:
        input_dict = {
            "Gender": gender,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "family_history": family_history,
            "FAVC": favc,
            "FCVC": fcvc,
            "NCP": ncp,
            "CAEC": caec,
            "SMOKE": smoke,
            "CH2O": ch2o,
            "SCC": scc,
            "FAF": faf,
            "TUE": tue,
            "CALC": calc,
            "MTRANS": mtrans
        }
        input_df = pd.DataFrame([input_dict])
        pred = modelo_pipeline.predict(input_df)[0]
        dic_pred = {
                "Normal_Weight": "Peso Normal",
                "Insufficient_Weight": "Peso Insuficiente",
                "Obesity_Type_I": "Obesidade Tipo I",
                "Obesity_Type_II": "Obesidade Tipo II",
                "Obesity_Type_III": "Obesidade Tipo III",
                "Overweight_Level_I": "Sobrepeso Nível I",
                "Overweight_Level_II": "Sobrepeso Nível II"
}
        st.success(f"Nível de obesidade previsto: **{dic_pred[pred]}**")

