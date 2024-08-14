import streamlit as st
from datetime import datetime, date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go


start_date = "2018-01-01"
today = date.today().strftime('%Y-%m-%d')


st.title("Stock Predictions")

stocks = ("META", "GS", "AMZN", "LICI.NS", "BCS", "GOOG", "MSFT", "GME")
select_stock =  st.selectbox("Select Stock for prediction : ", stocks)


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start_date, today)
    data.reset_index(inplace = True)
    return data

data_load_state = st.text("Loading Data!")
data = load_data(select_stock)
data_load_state.text("Data Loaded!")

st.subheader('Raw Data')
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data['Date'], y = data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x = data['Date'], y = data['Close'], name = 'stock_close'))
    fig.layout.update(title_text = "Time Seires Data", xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw_data()

n_years = st.slider("Year of Prediction : ", 1, 6)
period = n_years * 365

#Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns = {'Date': 'ds', "Close":'y'})

m = Prophet()
m.fit(df_train)

future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

#st.subheader('Forecast Data')
#st.write(forecast.tail())

st.write('Forecast Data Graph')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('Forecast Data')
fig2 = m.plot_components(forecast)
st.write(fig2)