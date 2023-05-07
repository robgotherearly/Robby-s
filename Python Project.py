#!/usr/bin/env python
# coding: utf-8

# ## Python Data Science First Project

# In[28]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install nbformat')
get_ipython().system('pip install html5lib ')
get_ipython().system('pip install bs4')


# In[29]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ## Define Graphing Function

# In[30]:



def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ##  Use yfinance to Extract Stock Data

# In[31]:


#Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. 
#The stock is Apple and its ticker symbol is AAPL.
aapl = yf.Ticker("AAPL")
print(aapl)


# In[32]:


#Using the ticker object and the function history extract stock information and save it in a dataframe named aapl_data. 
#Set the period parameter to max so we get information for the maximum amount of time.

m = aapl.history(period="max")
aapl_data = pd.DataFrame(m)


# In[33]:


#Reset the index using the reset_index(inplace=True) function on the aapl_data DataFrame and display the first five rows of the aapl_data dataframe using the head function. 
#Take a screenshot of the results and code from the beginning of Question 1 to the results below.

aapl_data.reset_index(inplace=True)
aapl_data.head()


# ## Use Webscraping to Extract Apple Revenue Data

# In[34]:


#Use the requests library to download the webpage https://www.macrotrends.net/stocks/charts/AAPL/apple/revenue
#Save the text of the response as a variable named html_data.

url = 'https://www.macrotrends.net/stocks/charts/AAPL/apple/revenue'
html_data = requests.get(url).text


# In[35]:


#Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data, "html.parser")


# In[36]:


#Using BeautifulSoup or the read_html function extract 
#the table with Apple Quarterly Revenue and store it into a dataframe named aapl_revenue.
#The dataframe should have columns Date and Revenue.

tables = soup.find_all('table')

for index,table in enumerate (tables):
    if("Apple Quarterly Revenue" in str(table)):
        table_index = index
table_index

aapl_revenue = pd.DataFrame(columns=["Date","Revenue"])

for row in tables[table_index].tbody.find_all('tr'):
    col = row.find_all('td')
    date = col[0].text.strip()
    revenue = col[1].text.strip()
    if date != '' and revenue != '':
        aapl_revenue.loc[len(aapl_revenue)] = [date, revenue]
        
aapl_revenue.head()


# 
# ## You can use this way

# In[37]:


# url = "https://www.macrotrends.net/stocks/charts/AAPL/apple/revenue"
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')


# for index,table in enumerate(tables):
#     if("Apple Quarterly Revenue" in str(table)):
#         table_index = index


# data = pd.read_html(str(tables[table_index]))
# df = pd.DataFrame(data[0])

# df.columns = ['Date', 'Revenue']
# df.head()


# In[38]:


#Execute the following line to remove the comma and dollar sign from the Revenue column.

aapl_revenue['Revenue'] = aapl_revenue['Revenue'].str.replace(',', '').str.replace('$', '')


# In[39]:


#To check if our code worked
aapl_revenue.head()


# In[40]:


#Execute the following lines to remove an null or empty strings in the Revenue column.
aapl_revenue.dropna(inplace=True)

aapl_revenue = aapl_revenue[aapl_revenue['Revenue'] != ""]


# ## Use yfinance to Extract Stock Data

# In[41]:


#Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. 
#The stock is Microsoft and its ticker symbol is MSFT.
msft = yf.Ticker("MSFT")
print(msft)


# In[42]:


#Using the ticker object and the function history extract stock information and save it in a dataframe named msft_data. 
#Set the period parameter to max so we get information for the maximum amount of time.

msft_history = msft.history(period="max")
msft_data = pd.DataFrame(msft_history)


# In[43]:


#Reset the index using the reset_index(inplace=True) function on the msft_data DataFrame and display the first five rows of the msft_data dataframe using the head function. 
#Take a screenshot of the results and code from the beginning of Question 1 to the results below.

msft_data.reset_index(inplace=True)
msft_data.head()


# ## Use Webscraping to Extract Apple Revenue Data

# In[44]:


#Use the requests library to download the webpage https://www.macrotrends.net/stocks/charts/MSFT/microsoft/revenue
#Save the text of the response as a variable named html_data.
url = 'https://www.macrotrends.net/stocks/charts/MSFT/microsoft/revenue'
msft_quest = requests.get(url).text


# In[45]:


#Parse the html data using beautiful_soup.
soup = BeautifulSoup(msft_quest,"html.parser")


# In[46]:


#Using BeautifulSoup or the read_html function extract 
#the table with Microsoft Quarterly Revenue and store it into a dataframe named aapl_revenue.
#The dataframe should have columns Date and Revenue.

tables =soup.find_all('table')

for index,table in enumerate (tables):
    if("Microsoft Quarterly Revenue" in str(table)):
        table_index = index
table_index

msft_revenue = pd.DataFrame(columns=["Date","Revenue"])

for row in tables[table_index].tbody.find_all('tr'):
    col = row.find_all('td')
    date = col[0].text.strip()
    revenue = col[1].text.strip()
    if date != '' and revenue != '':
        msft_revenue.loc[len(msft_revenue)] = [date, revenue]
    
msft_revenue.head()


# In[47]:


#Execute the following line to remove the comma and dollar sign from the Revenue column.
msft_revenue['Revenue'] = msft_revenue['Revenue'].str.replace(',', '').str.replace('$', '')


# In[48]:


#To check if our code worked
msft_revenue.head()


# In[49]:


#Execute the following lines to remove an null or empty strings in the Revenue column.
msft_revenue.dropna(inplace=True)

msft_revenue = msft_revenue[msft_revenue['Revenue'] != ""]


# In[50]:


make_graph(aapl_data,aapl_revenue,"Apple")


# In[51]:


make_graph(msft_data,msft_revenue,"Microsoft")

