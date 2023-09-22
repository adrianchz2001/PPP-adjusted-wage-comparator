import streamlit as st
import requests
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from unidecode import unidecode
from time import sleep
from funciones import translator, cleaning, graph, extraction

# Título de la página

def main():
    st.set_page_congig("🪙 Salarios-por-PPA")
    st.title("Comparador de salarios ajustados por PPA")
    st.header(
        "¿Quieres saber cuánto ganarías en un país si cobraras según la paridad adquisitiva de otro?")
    st.write("Este proyecto te permite seleccionar dos países dentro de un rango determinado y comparar el salario medio de un país con el mismo salario medio ajustado a la paridad de poder adquisitivo (PPA) del otro país; esto nos permite saber 2 cosas:/n1- El salario medio del país en cuestión y su evolución./n2- El poder adquisitivo real de una persona cuando se compara con el otro país")
    st.image("medium-illustration-paycheque-globe.jpg")


def project():
    
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)

    paises = ["Spain", "France", "Germany", "Norway", "Italy", "Ireland",
              "Switzerland", "Sweden", "Finland", "Poland", "Greece"]

    country1 = st.selectbox("Selecciona un país:", paises)
    country2 = st.selectbox("Selecciona otro país:", paises)
    
    st.exception("Seleccione dos países distintos.")

    countries = translator(country1=country1.lower(),
                           country2=country2.lower())

    salaries = extraction(countries=countries)

    df = cleaning(country1.capitalize(), country2.capitalize(), salaries)

    dates = [df.index[i] for i in range(len(df.index))]

    country_1 = country1.lower()
    country_2 = country2.lower()

    st.set_option('deprecation.showPyplotGlobalUse', False)

    if st.checkbox("Visualizar los datos"):
        st.dataframe(df)
    st.pyplot(graph(df=df, country_1=country_1, country_2=country_2))


def method():
    st.title("Metodología aplicada")
    st.header("¿De dónde salen los datos?")
    st.write("Los datos salen de la base de datos de Eurostat y de la página web del diario español Expansión, conocida popularmente esta página web como 'Datosmacro'.")
    st.header("¿Qué tan fiables son los datos?")
    st.write("Dado que Eurostat es una institución propiedad de la Comisión Europea para el registro de estadísticas de países dentro y fuera de la UE-27 que pueda interesar a los mismos, consideramos su fiabilidad como bastante elevada. En cuanto a Eurostat, independientemente del prestigio del diario Expansión, que en temas económicos es innegable, contamos con que esta página se dedica, meramente, a recopilar datos que salen de los Institutos Nacionales de Estadística de cada país, de modo que funciona como un recopilatorio de estadísticas oficiales de cada nación.")
    st.write("Si deseas conocer más sobre mí o mis proyectos, te dejo a continuación mi enlace a GitHub y a LinkedIn. ¡Muchas gracias por tu atención!")
    url_LK = "https://linkedin.com/in/adri%C3%A1n-ch%C3%A1vez"
    url_git = "https://github.com/adrianchz2001"

    column1, column2 = st.columns(2)
    with column1:
        st.image("LinkedIn_logo_initials.png")
        st.markdown(f"[Enlace a mi LinkedIn. Click aquí]({url_LK})")
    with column2:
        st.image("GitHub-Mark.png")
        st.markdown(f"[Enlace a mi GitHub. Click aquí]({url_git})")


# Barra lateral para navegar entre las páginas
opciones_paginas = ["Página Inicial",
                    "Página de Proyecto", "Página de Metodología"]
pagina_seleccionada = st.sidebar.selectbox(
    "Selecciona una página:", opciones_paginas)

# Mostrar la página seleccionada
if pagina_seleccionada == "Página Inicial":
    main()
elif pagina_seleccionada == "Página de Proyecto":
    project()
else:
    method()
