'''
Using the John Hopkins CSSE COVID-19 data:
https://github.com/CSSEGISandData/COVID-19

Using list of countries by population from Wikipedia:
'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
'''

import pandas as pd
import re

import altair as alt
import pandas as pd
import numpy as np
import datetime

import math
from enum import Enum

from IPython.display import display

class ScaleType(Enum):
    Linear=("linear", 1, 0)
    Log_10=("log", 10, 1)
    Log_2=("log", 2, 1)
    Log_e=("log",  math.exp(1), 1)
    def __init__(self, scale_type, log_base, threshold):
        self.scale_type = scale_type
        self.log_base=log_base
        self.threshold=threshold

class Covid19_status(Enum):
    Confirmed=(0)
    Deaths=(1)
    #Recovered=(2)
    #Active=(3)
    #Merged=(4)

    def __init__(self, idx):
        self.csse = None

class Csse_covid19(Enum):
    Confirmed = (Covid19_status.Confirmed, 
                'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    Deaths = (Covid19_status.Deaths, 
              'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    #Recovered = (Covid19_status.Recovered,
    #             'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
    #Active = (Covid19_status.Active, None)
    #Merged = (Covid19_status.Merged, None)

    def __init__(self, status, url):
        self.status = status
        self.url = url
        self.status.csse = self
        self.df_raw = None
        self.df_pop = None 
        self.re_date='^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}$'    
        self.df_raw = pd.read_csv(self.url, header=0, sep=',')
        self.date_cols = self.df_raw.filter(regex=self.re_date).columns.values    
        print(self.status)
        #if self.status == Covid19_status.Active:
        #  self.df_raw = self.Confirmed.df_raw.copy()
        #  self.date_cols = self.df_raw.filter(regex=self.re_date).columns.values 
        #  self.df_raw[self.date_cols] = self.df_raw[self.date_cols].sub(
        #      self.Recovered.df_raw[self.date_cols]).sub(
        #          self.Deaths.df_raw[self.date_cols])
        #elif self.status is Covid19_status.Merged:
        #  cols = self.Confirmed.df_raw.columns.values.tolist()
        #  cols.insert(0,'Status')
        #  self.df_raw = pd.DataFrame(columns=cols)
        #  for status in Covid19_status:
        #    if status is Covid19_status.Merged:
        #      continue
        #    df = status.csse.df_raw.copy()
        #    df['Status'] = status.name
        #    self.df_raw = self.df_raw.append(df, sort=False, ignore_index=True)      
        #else:
        #  self.df_raw = pd.read_csv(self.url)
        #  self.date_cols = self.df_raw.filter(regex=self.re_date).columns.values
    
    @staticmethod
    def get_names():
        return [status.name for status in Csse_covid19]

    @staticmethod
    def add_population(csv_merged_countries_population): 
        df_countries_population = pd.read_csv(csv_merged_countries_population, header=0, sep=';')
        df_countries_population.dropna(inplace=True)
        df_countries_population['Country or area'].str.replace('\[[a-z0-9]\]$', '', regex=True)
        for status in Csse_covid19:
            status.__add_population(df_countries_population)

    def __add_population(self, df_countries_population): 
        for index, row in df_countries_population.iterrows():
            country_csse = row['Csse Covid-19 countries']      
            if country_csse != np.NaN:
                count = row['Population(1 July 2019)']
                self.df_raw.loc[
                  self.df_raw['Country/Region']==country_csse, 
                  'Population(1 July 2019)'] = count

    def alt_plot(self, countries=None, width=800, height=600, 
                sort_legend=False, scale_type=ScaleType.Linear, 
                normalize_by_population=False,
                file_path=None, show=True, day_delta=0):
        if 'Population(1 July 2019)' not in self.df_raw.columns:
            Csse_covid19.add_population('merged_countries_population_nan.csv')      
        source = self.df_raw
        if countries is not None:
            source = source.loc[source['Country/Region'].isin(countries)]
        else:
            countries = source['Country/Region'].values.tolist()

        source = source.groupby('Country/Region').sum().reset_index()
        source = source.set_index([source.index, 'Country/Region', 'Lat', 'Long', 'Population(1 July 2019)'])
        source = source.stack()
        source.index.set_names('Date', level=len(source.index.names)-1, inplace=True)
        source = source.reset_index().rename(columns={0:'Count'})
        if normalize_by_population:
            source['Count'] /= source['Population(1 July 2019)'] * 1e-6
            source['Count'] = source['Count'].round(3)
        first_date_str = source.iloc[0]['Date'] 
        last_date_str = source.iloc[-1]['Date']
        first_date = datetime.datetime.strptime(first_date_str, "%m/%d/%y")
        last_date = datetime.datetime.strptime(last_date_str, "%m/%d/%y")
        end_date_str = (last_date  + datetime.timedelta(days=day_delta)).strftime("%m/%d/%y")
        date_range=[first_date_str, end_date_str]
        alt.data_transformers.disable_max_rows()
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['Date'], empty='none')

        scale = alt.Scale(type='linear')
        color = alt.Color('Country/Region')
        sort = countries
        title = '{} - including {}'.format(self.name, datetime.datetime.strftime(last_date, '%d %B %Y'))
        title_y = 'Count'
        scale = alt.Scale(type=scale_type.scale_type, base=scale_type.log_base)
        if sort_legend:
            sort = self.get_countries_sorted(countries)
        if normalize_by_population:
            title_y = 'Count/per million (population)'
            title += ', normalized per million of the population'
        color = alt.Color('Country/Region', sort=sort)                    
        line = alt.Chart(source).transform_filter( 
            alt.datum.Count >= scale_type.threshold).mark_line().encode(
            alt.X('Date:T', scale=alt.Scale(domain=date_range), axis=alt.Axis(format = ("%d %b %Y"), labelAngle=90)), 
            alt.Y('Count:Q', scale=scale, axis=alt.Axis(orient='right', title=title_y)), 
            color
            ).properties(title=title)#.interactive()
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='Date:T', 
            opacity=alt.value(0),
        ).add_selection(nearest)
        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        ).interactive()
        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='right', dx=-5, dy=-5).encode(
            text=alt.condition(nearest, 'Count:Q', alt.value(' '))
        )
        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='Date:T',
        ).transform_filter(nearest)
        # Put the five layers into a chart and bind the data
        layer = alt.layer(line, 
                          selectors, 
                          points, rules, text,
        ).properties(width=width, height=height)    

        if file_path is not None:
            layer.save(file_path)
        if show:
            layer.display()
        return layer #layer.display()

    def get_top_countries(self, top=10):
        date = self.df_raw.filter(regex=self.re_date).columns.values[-1]
        df = self.df_raw.groupby(by='Country/Region').sum()
        df.sort_values(by=[date], inplace=True, ascending=False)
        df = df.iloc[:top]
        return df.index.values.tolist()

    def get_countries_sorted(self, countries):
        date = self.df_raw.filter(regex=self.re_date).columns.values[-1]
        df = self.df_raw.groupby(by='Country/Region').sum()
        df.sort_values(by=[date], inplace=True, ascending=False)
        return df.iloc[df.index.isin(countries)].index.tolist()

    def get_by_country(self, countries=None, plot=False, figsize=(10,10)):
        df = self.df_raw.groupby(by='Country/Region').sum().filter(self.date_cols)
        if countries is None:
            df = df.transpose()
        else:
            df = df.loc[countries].transpose()    
        if plot:
            fig = df.plot(figsize=figsize)
        return df, fig
