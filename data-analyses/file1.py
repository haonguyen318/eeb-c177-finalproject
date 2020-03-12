#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


from tkinter import Tk
from tkinter import filedialog as fd


# In[3]:


import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


# In[4]:


def open_file():
    root = Tk().withdraw()
    filename = fd.askopenfilename()
    return filename

def create_dataframe():
    filename = open_file()
    try:
        return pd.read_csv(filename, parse_dates=['dt'])
    except:
        return pd.read_excel(filename)


# In[5]:


# Annual Global Temperatures
def get_avg_global_temperatures(dataframe, start_year, end_year):
    
    df = dataframe.copy()
    
    # extract year from feature 'dt'
    df['dt'] = df['dt'].apply(lambda x: x.year)

    # extract observations of specified year range
    data = df[(df['dt']>=start_year) & (df['dt']<=end_year)]

    # return numpy array of average global temperatures
    return data.groupby(['dt']).mean()['AverageTemperature'].values


# In[6]:


def plot_avg_global_temperatures(dataframe, start_year, end_year):

    # extract corresponding dates and temperatures 
    dates = np.arange(start_year, end_year + 1)
    temps = get_avg_global_temperatures(dataframe, start_year, end_year)

    # plot data
    plt.figure(figsize=(12, 6))
    plt.scatter(dates, temps, c=temps, s=150, alpha=0.6, edgecolors='none', cmap='viridis')
    plt.xlim([start_year - 5, end_year + 5])
    plt.grid(True)
    plt.title("Average Global Temperatures [" + str(start_year) + ", " + str(end_year) + "]")
    plt.xlabel("Year")
    plt.ylabel("Temperature (Celsius)")
    plt.show()


# In[8]:


# Uncertainty

def get_uncertainty(dataframe, start_year, end_year):

    df = dataframe.copy()

    # extract year from feature 'dt'
    df['dt'] = df['dt'].apply(lambda x: x.year)

    # extract observations of specified year range
    data = df[(df['dt']>=start_year) & (df['dt']<=end_year)]

    # return numpy array of average temperature uncertainties
    return data.groupby(['dt']).mean()['AverageTemperatureUncertainty'].values

def plot_uncertainty(dataframe, start_year, end_year):

    # extract corresponding dates, temperatures, and uncertainties 
    dates = np.arange(start_year, end_year + 1)
    temps = get_avg_global_temperatures(dataframe, start_year, end_year)
    uncertainty = get_uncertainty(dataframe, start_year, end_year)


    # plot data
    plt.figure(figsize=(12, 6))
    plt.plot(dates, (temps + uncertainty), c='purple', label='Average Uncertainty Field')
    plt.plot(dates, (temps - uncertainty), c='purple')
    plt.fill_between(dates, (temps + uncertainty), (temps - uncertainty), facecolor='mediumpurple')
    plt.plot(dates, temps, linewidth=3, label='Average Temperature')
    plt.xlim([start_year - 5, end_year + 5])
    plt.grid(True)
    plt.legend(loc='best')
    plt.title("Average Global Temperatures and Uncertainty Field [" + str(start_year) + ", " + str(end_year) + "]")
    plt.xlabel("Year")
    plt.ylabel("Temperature (Celsius)")
    plt.show()


# In[9]:


# Seasons

def get_season(month):
    if month >= 3 and month <= 5:
        return 'Spring'
    elif month >= 6 and month <= 8:
        return 'Summer'
    elif month >= 9 and month <= 11:
        return 'Autumn'
    else:
        return 'Winter'


def get_avg_seasonal_global_temperatures(dataframe, start_year, end_year):

    df = dataframe.copy()

    df['Year'] = df['dt'].apply(lambda x: x.year)
    df['Month'] = df['dt'].apply(lambda x: x.month)
    df['Season'] = df['Month'].apply(get_season)

    years = np.arange(start_year, end_year + 1)

    spring = []
    summer = []
    autumn = []
    winter = []

    for year in years:
        data = df[df['Year'] == year]
        spring.append(data[data['Season']=='Spring']['AverageTemperature'].mean())
        summer.append(data[data['Season']=='Summer']['AverageTemperature'].mean())
        autumn.append(data[data['Season']=='Autumn']['AverageTemperature'].mean())
        winter.append(data[data['Season']=='Winter']['AverageTemperature'].mean())

    return (spring, summer, autumn, winter)


def plot_avg_seasonal_global_temperatures(dataframe, start_year, end_year):

    # extract corresponding dates and seasonal data
    years = np.arange(start_year, end_year + 1)
    spring, summer, autumn, winter = get_avg_seasonal_global_temperatures(dataframe, start_year, end_year)

    plt.figure(figsize=(12, 6))
    plt.plot(years, spring, label='Spring', color='sage')
    plt.plot(years, summer, label='Summer', color='lightcoral')
    plt.plot(years, autumn, label='Autumn', color='orange')
    plt.plot(years, winter, label='Winter', color='lightskyblue')

    plt.legend(loc='best')
    plt.grid(True)
    plt.xlim(start_year - 5, end_year + 5)
    plt.title("Average Global Temperatures by Season [" + str(start_year) + ", " + str(end_year) + "]")
    plt.xlabel('Years')
    plt.ylabel('Temperature (Celsius)')
    plt.show()


# In[ ]:




