import pandas as pd
import time
import datetime
import warnings
import streamlit as st
warnings.filterwarnings('ignore')
import psycopg2

# Page config
st.set_page_config(
    page_title="Stock Recommendations",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📊 Stock Trading Recommendations")
st.markdown("---")

# Custom CSS
st.markdown("""
<style>
    .buy-header {
        color: #1f9431;
        font-weight: bold;
        font-size: 24px;
        padding: 15px 0px;
        text-transform: uppercase;
    }
    .exit-header {
        color: #cc1919;
        font-weight: bold;
        font-size: 24px;
        padding: 15px 0px;
        text-transform: uppercase;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def fetch_buy_recommendations():
    conn = psycopg2.connect(
        host='192.168.1.245',
        port='5432',
        database='Equity_client2',
        user='WMS',
        password='Neoquant@2023'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buy_recommendations")
    data = pd.DataFrame(cursor.fetchall(), 
                       columns=[desc[0] for desc in cursor.description])
    cursor.close()
    conn.close()
    return data

def fetch_sell_recommendations():
    conn = psycopg2.connect(
        host='192.168.1.245',
        port='5432',
        database='Equity_client2',
        user='WMS',
        password='Neoquant@2023'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sell_recommendations")
    data = pd.DataFrame(cursor.fetchall(), 
                       columns=[desc[0] for desc in cursor.description])
    cursor.close()
    conn.close()
    return data

try:
    # Initialize session state for dataframes
    if 'buy_stocks' not in st.session_state:
        st.session_state.buy_stocks = pd.DataFrame()
    if 'sell_stocks' not in st.session_state:
        st.session_state.sell_stocks = pd.DataFrame()

    # Display recommendations in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="buy-header">ENTRY SIGNALS</p>', unsafe_allow_html=True)
        if st.button("🔄 Fetch Entry Signals", key="buy_btn"):
            with st.spinner('Fetching entry signals...'):
                st.session_state.buy_stocks = fetch_buy_recommendations()
                
        if not st.session_state.buy_stocks.empty:
            st.dataframe(
                st.session_state.buy_stocks,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Click button to fetch entry signals")

    with col2:
        st.markdown('<p class="exit-header">EXIT SIGNALS</p>', unsafe_allow_html=True)
        if st.button("🔄 Fetch Exit Signals", key="exit_btn"):
            with st.spinner('Fetching exit signals...'):
                st.session_state.sell_stocks = fetch_sell_recommendations()
                
        if not st.session_state.sell_stocks.empty:
            st.dataframe(
                st.session_state.sell_stocks,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Click button to fetch exit signals")

    # Add timestamp
    st.markdown("---")
    st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

except Exception as e:
    st.error(f"Error: {e}")
