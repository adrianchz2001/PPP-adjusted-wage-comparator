import streamlit as st
import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from unidecode import unidecode
from time import sleep

def translator(country1, country2):
    
    translator = GoogleTranslator(source='en', target='es') # Automate translation from the Google translator
    
    country1 = translator.translate(country1)
    country2 = translator.translate(country2)
    
    country1 = country1.lower()
    country1 = country1.capitalize()
    
    country2 = country2.lower()
    country2 = country2.capitalize()
    
    country1 = unidecode(country1)
    country2 = unidecode(country2)
        # By this, we make sure that the country selected respect the format of Datosmacro
    
    countries = list()
    countries.append(country1)
    countries.append(country2)
    
    return countries

def extraction(countries):
    url_1 = f"https://datosmacro.expansion.com/mercado-laboral/salario-medio/{countries[0].lower()}"
    url_2 = f"https://datosmacro.expansion.com/mercado-laboral/salario-medio/{countries[1].lower()}"
    
    response_1 = requests.get(url_1)
    
    sleep(1)
    
    response_2 = requests.get(url_2)
    
    soup_1 = BeautifulSoup(response_1.text, "html.parser")
    soup_2 = BeautifulSoup(response_2.text, "html.parser")
    
    mean_wage_1 = [soup_1.find_all("td", class_ = "numero")[i].text for i in range(len(soup_1.find_all("td", class_ = "numero")))]

    mean_wage_2 = [soup_2.find_all("td", class_ = "numero")[i].text for i in range(len(soup_2.find_all("td", class_ = "numero")))]
    
    mean_wage_1 = [mean_wage_1[i].split()[0] for i in range(len(mean_wage_1))]

    mean_wage_2 = [mean_wage_2[i].split()[0] for i in range(len(mean_wage_2))]
    
    mean_wage_1 = mean_wage_1[::3] # For some reason, the webpage returns a value that it's not on the mean wages table
    
    mean_wage_2 = mean_wage_2[::3] # However, the return follows a pattern. Therefore, every two values after the the first one and so on are deleted
    
    del mean_wage_1[-1] # Eurostat has data only referred to the PPP until 2021, but Datosmacro offers data for mean wages up to 2022
    
    del mean_wage_2[-1]
    
    mean_wage_1 = mean_wage_1[::-1] # The values are inverted, so that we can get, then, a DataFrame with the values in an ascending order by year
    
    mean_wage_2 = mean_wage_2[::-1]
    
    return [mean_wage_1, mean_wage_2]

def cleaning(country1, country2, wages):
    df = pd.read_excel("PPPs.xlsx", sheet_name= "Sheet 2") # The Excel is clean and prepared for the extraction

    df = df.set_index("TIME") # We set the years as the index, so that, at the moment of visualizing we'll be able to use df.index as the x-axis
    
    country1 = country1.lower()
    country2 = country2.lower()
    
    df = df.loc[:, [country1.capitalize(), country2.capitalize()]]
    
    wage1 = [float(i) * 1000 for i in wages[0][:len(df)]]
    wage2 = [float(i) * 1000 for i in wages[1][:len(df)]]
    
    df[f"Mean wage of {country1.capitalize()}"] = wage1
    df[f"Mean wage of {country2.capitalize()}"] = wage2
    
    df[f"Adjusted wage for {country1.capitalize()}"] = [round((df[f"Mean wage of {country1.capitalize()}"].iloc[i] * df[f"{country2.capitalize()}"].iloc[i])/(df[f"{country1.capitalize()}"].iloc[i]), 2) for i in range(len(df[f"Mean wage of {country1.capitalize()}"]))]
    df[f"Adjusted wage for {country2.capitalize()}"] = [round((df[f"Mean wage of {country2.capitalize()}"].iloc[i] * df[f"{country1.capitalize()}"].iloc[i])/(df[f"{country2.capitalize()}"].iloc[i]), 2) for i in range(len(df[f"Mean wage of {country2.capitalize()}"]))]
    
    return df

def graph(df, country_1, country_2):
    dates = [df.index[i] for i in range(len(df.index))]
    
    country_1 = country_1.lower()
    country_2 = country_2.lower()
    
    plt.figure(figsize = (16, 12))
    
    plt.subplot(3, 1, 1)
    plt.plot(dates, df[f"Adjusted wage for {country1.capitalize()}"], linestyle= '--', color= 'orange')
    plt.plot(dates, df[f"Mean wage of {country_2.capitalize()}"], linestyle= '-', color= 'blue')

    plt.grid()
    plt.xlabel("Years")
    plt.ylabel("Salary (adjusted, in euros)")
    plt.legend([f"What should you earn in {country_2.capitalize()} if you want to keep the purchasing power from {country_1.capitalize()}", f"Mean wage in {country_2.capitalize()}"], loc= 'best', fontsize= 10)
    
    
    plt.subplot(3, 1, 2)
    plt.plot(dates, df[f"Adjusted wage for {country2.capitalize()}"], linestyle= '--', color= 'orange')
    plt.plot(dates, df[f"Mean wage of {country_1.capitalize()}"], linestyle= '-', color= 'blue')

    plt.grid()
    plt.xlabel("Years")
    plt.ylabel("Salary (adjusted, in euros)")
    plt.legend([f"What should you earn in {country_1.capitalize()} if you want to keep the purchasing power from {country_2.capitalize()}", f"Mean wage in {country_1.capitalize()}"], loc= 'best', fontsize= 10)
    
    plt.subplot(3, 1, 3)
    plt.plot(dates, df[f"{country_1.capitalize()}"], linestyle= '-', color= 'orange')
    plt.plot(dates, df[f"{country_2.capitalize()}"], linestyle= '-', color= 'blue')

    plt.grid()
    plt.xlabel("Years")
    plt.ylabel("PPPs (actual individual expenditure)")
    plt.legend([f"PPPs of {country_1.capitalize()}", f"PPPs of {country_2.capitalize()}"], loc= 'best', fontsize= 12)
    plt.savefig("Gráficos por países.png", format = "png")
