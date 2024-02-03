import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

url = "https://www.worldometers.info/world-population/population-by-country/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find('table', {'id':'example2'}).find('tbody').find_all('tr')

countries_list = []

for row in rows:
    dic = {}
    dic['country'] = row.find_all('td')[1].text
    dic['Population 2023'] = row.find_all('td')[2].text.replace(',','')
    
    countries_list.append(dic)

df = pd.DataFrame(countries_list)
df.to_csv('data.csv', index=False)

conn = sqlite3.connect('data.db')
df = pd.DataFrame(countries_list)
df.to_sql('population', conn, index=False, if_exists='replace')

# Load data from SQLite database
conn = sqlite3.connect('data.db')
query = "SELECT * FROM population"
df = pd.read_sql_query(query, conn)


# Plot 1: Bar chart for top 10 countries by population
fig1 = px.bar(df.head(10), x='country', y='Population 2023', title='Top 10 Countries by Population in 2023')

# Plot 2: Pie chart for population distribution by continent 
fig2 = px.pie(df, names='country', values='Population 2023', title='Population Distribution by Country in 2023')

# Plot 3: Scatter plot for population  
fig3 = px.scatter(df, x='country', y='Population 2023', title='Population in 2023')

# Save the plots as HTML, PDF, or PNG files
fig1.write_html('plot1.html')
fig1.write_image('plot1.png')
fig1.write_image('plot1.pdf')

fig2.write_html('plot2.html')
fig2.write_image('plot2.png')
fig2.write_image('plot2.pdf')

fig3.write_html('plot3.html')
fig3.write_image('plot3.png')
fig3.write_image('plot3.pdf')
