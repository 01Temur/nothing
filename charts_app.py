import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app setup
st.set_page_config(page_title="Financial Analysis", layout="wide")

# Sidebar input
with st.sidebar:
    st.title("Financial Analysis")
    ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", "AAPL")
    period = st.selectbox("Enter a time frame", ("1D", "5D", "1M", "6M", "YTD", "1Y", "5Y"), index=2)
    button = st.button("Submit")

# Helper functions
def format_value(value):
    """Format large numbers into human-readable strings."""
    if value is None or not isinstance(value, (int, float)):
        return "N/A"
    suffixes = ["", "K", "M", "B", "T"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def safe_format(value, format_str="{:.2f}"):
    """Safely format numbers and handle None or invalid values."""
    try:
        return format_str.format(float(value))
    except (TypeError, ValueError):
        return "N/A"

# Tabs
tab1, tab2 = st.tabs(["Stock Analysis", "Economic Calendar"])

# Tab 1: Stock Analysis
with tab1:
    st.markdown("### Stock Analysis")
    if button:
        if not ticker.strip():
            st.error("Please provide a valid stock ticker.")
        else:
            try:
                with st.spinner("Fetching data, please wait..."):
                    # Retrieve stock data
                    stock = yf.Ticker(ticker)
                    info = stock.info

                    st.subheader(f"{ticker.upper()} - {info.get('longName', 'N/A')}")

                    # Historical stock price data
                    interval_map = {
                        "1D": ("1d", "1h"),
                        "5D": ("5d", "1d"),
                        "1M": ("1mo", "1d"),
                        "6M": ("6mo", "1wk"),
                        "YTD": ("ytd", "1mo"),
                        "1Y": ("1y", "1mo"),
                        "5Y": ("5y", "3mo"),
                    }
                    period_input, interval = interval_map.get(period, ("1mo", "1d"))
                    history = stock.history(period=period_input, interval=interval)

                    if not history.empty:
                        chart_data = pd.DataFrame(history["Close"])
                        st.line_chart(chart_data)
                    else:
                        st.warning("No historical data available for the selected period.")

                    # Stock Info
                    stock_info = [
                        ("Country", info.get("country", "N/A")),
                        ("Sector", info.get("sector", "N/A")),
                        ("Industry", info.get("industry", "N/A")),
                        ("Market Cap", format_value(info.get("marketCap"))),
                        ("Enterprise Value", format_value(info.get("enterpriseValue"))),
                        ("Employees", info.get("fullTimeEmployees", "N/A")),
                    ]
                    st.table(pd.DataFrame(stock_info, columns=["Stock Info", "Value"]))

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Tab 2: Economic Calendar
with tab2:
    st.markdown("### Economic Calendar")
    st.write("This section can include details like upcoming economic events, indicators, and reports.")
    
    # Example: Placeholder for Economic Calendar data
    calendar_data = [
        {"Date": "2024-11-17", "Event": "US Retail Sales", "Impact": "High"},
        {"Date": "2024-11-18", "Event": "UK Inflation Rate", "Impact": "Medium"},
        {"Date": "2024-11-19", "Event": "FOMC Minutes Release", "Impact": "High"},
    ]
    df_calendar = pd.DataFrame(calendar_data)
    st.table(df_calendar)
