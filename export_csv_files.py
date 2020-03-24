from csse_covid19 import Csse_covid19

import pandas as pd
import re

import requests
from bs4 import BeautifulSoup

def get_world_population_from_wiki():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    element = html.find(text=re.compile('Country or area'))
    #element = html.find(text=re.compile('Countries and areas ranked by population in 2019'))
    html_population_table = element.findParent('table')
    df_population = pd.read_html(str(html_population_table))[0]
    df_population['Country or area'] = df_population['Country or area'].str.replace('\[[a-z0-9]\]$', '', regex=True)
    df_population.sort_values(by='Country or area', inplace=True)
    return df_population.loc[:, ['Country or area', 'Population(1 July 2019)']]

def get_csse_covid19_countries():
    countries = Csse_covid19.Confirmed.df_raw.groupby(by=['Country/Region']).sum().index.tolist()   
    df_countries = pd.DataFrame(columns=['Csse Covid-19 countries'], data=countries)
    df_countries.sort_values(by='Csse Covid-19 countries', inplace=True)
    return df_countries

def export_csv():
    get_world_population_from_wiki().to_csv('world_population_by_countries.csv')
    get_csse_covid19_countries().to_csv('csse_covid19_countries.csv')

export_csv()
#def merge_world_population_csse_countries(merged_csv_path):
#    df_countries = pd.read_csv(merged_csv_path)
#    df_countries.dropna(inplace=True)
#    df_countries['population_countries'].str.replace('\[[a-z0-9]\]$', '', regex=True)
#    
#    df_population.sort_values(by=['Country or area'], inplace=True)
#    df_countries.sort_values(by=['population_countries'], inplace=True)
#
#    for index, row in df_countries.iterrows():
#        country_csse = row['csse_covid19_countries']
#        country_pop = row['population_countries']
#        print(country_csse, country_pop)
#        #if False:
#        if country_csse != np.NaN:
#          count = df_population.loc[df_population['Country or area'] == country_pop,
#                                    'Population(1 July 2019)'].values
#        #df = csse_covid19.df_raw
#        #df.loc[df['Country/Region']==country_csse, 
#        #          'Population_2019-7-1'] = count
#        df_countries.loc[index, 'Population_2019_7_1'] = count   
