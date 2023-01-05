import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import requests
import time
#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")
st.set_option("page_config")
#---------------------------------#
# Title

image = Image.open('logo_crypto.jpg')

st.image(image, width = 500)

st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")
#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")


#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('BTC', 'ETH', 'USD'))

array_check = ['BTC','ETH','USD']

link = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing'
params = {
    'start': 1,
    'limit': 100,
    'sortBy': 'market_cap',
    'sortType': 'desc',
    'convert': 'USD,BTC,ETH',
    'cryptoType': 'all',
    'tagType': 'all',
    'audited': 'false',
    'aux': 'ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d'
}
# Web scraping of CoinMarketCap data


@st.cache(suppress_st_warning=True)
def load_data():
    with requests.Session() as s:
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        res = s.get(link,params=params)
        res.json()['data']['cryptoCurrencyList']
        listings = res.json()['data']['cryptoCurrencyList']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(round(i['high24h'],2))
        percent_change_1h.append(i['quotes'][array_check.index(currency_price_unit)]['percentChange1h'])
        percent_change_24h.append(i['quotes'][array_check.index(currency_price_unit)]['percentChange24h'])
        percent_change_7d.append(i['quotes'][array_check.index(currency_price_unit)]['percentChange7d'])
        market_cap.append(i['quotes'][array_check.index(currency_price_unit)]['fullyDilluttedMarketCap'])
        volume_24h.append(i['quotes'][array_check.index(currency_price_unit)]['volume24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data()


## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data


# Create form for submit
form = col1.form("my_form")

## Sidebar - Number of coins to display
num_coin = form.slider('Display Top N Coins', 1, 100, 50)
df_coins = df_selected_coin[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = form.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = form.selectbox('Sort values?', ['Yes', 'No'])

# Now add a submit button to the form:
form.form_submit_button("Submit")




col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

#---------------------------------#
# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)