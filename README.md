
# 🩺 Obesity Predictor App

Este projeto é uma aplicação de Machine Learning desenvolvida para prever o nível de obesidade de uma pessoa com base em hábitos alimentares, comportamentais e características físicas.

A solução foi construída como parte do Tech Challenge - Fase 4 (Data Analytics) e integra:

- ✅ Pipeline completo de Machine Learning com feature engineering
- ✅ Aplicação preditiva em Streamlit
- ✅ Dashboard analítico com gráficos de apoio à decisão médica

---

## 📁 Estrutura do Projeto

- `obesity_predictor_app_final.py`: aplicação completa em Streamlit
- `Obesity.csv`: base de dados utilizada para treinamento e análise
- `requirements.txt`: lista de dependências para execução
- `README.md`: este arquivo :)

---

## 🚀 Como Executar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/fiap-predicao-obesidade.git
cd obesity-predictor
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run obesity_predictor_app_final.py
```

---

## 🌐 Deploy no Streamlit Cloud

O app pode ser executado diretamente no navegador via:
```
https://seu-usuario.streamlit.app/obesity-predictor
```

---

## 📊 Sobre os Dados

A base `Obesity.csv` inclui variáveis como:

- Gênero, idade, altura, peso
- Hábitos alimentares e físicos
- Histórico familiar
- Nível de obesidade (variável alvo)

---

## 📈 Principais Resultados

- Modelo Random Forest com **93% de acurácia**
- Pipeline implementada com `ColumnTransformer` e `Pipeline` do scikit-learn
- Visualizações com `matplotlib` e `seaborn`

---

## 🧠 Créditos

Desenvolvido como parte do Tech Challenge da Pós Tech pelos colegas: Rodrigo da Silva, Paulo Henrique Santana Silva, Thiago Jardim de Andrade, Tatiane Maria Ramos e Eduardo Patrocina Soares Teixeira
