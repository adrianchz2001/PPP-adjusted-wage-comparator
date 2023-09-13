import streamlit as st
import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from unidecode import unidecode
from time import sleep
from funciones import translator, cleaning, graph, extraction

# Título de la página
st.title("Comparador de salarios ajustados por PPA")
paises = ["Spain", "France", "Germany", "Norway", "Italy", "Ireland", "Switzerland", "Sweden", "Finland", "Poland", "Greece"]
country1 = st.selectbox("Selecciona un país:", paises)
country2 = st.selectbox("Selecciona otro país:", paises)

countries = translator(country1 = country1.lower(), country2 = country2.lower())

try:
    salaries = extraction(countries = countries)

    df = cleaning(country1.capitalize(), country2.capitalize(), salaries)

    grafico = graph(df, country1.capitalize(), country2.capitalize())

    st.image("Gráficos por países.png", caption = "Gráficos")

except:
    raise KeyError("Escribe los nombres de los países en inglés. Sentimos las molestias")
