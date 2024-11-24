!pip install plotly
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache
def load_data():
    file_path = "ELB-Sales-Data.xlsx"  # Ensure this file is in your GitHub repo
    df = pd.read_excel(file_path, sheet_name="Elbrit Sales Log")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Load data
df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
month = st.sidebar.selectbox("Select Month", df['Date'].dt.month_name().unique())
hq = st.sidebar.selectbox("Select HQ", df['HQ'].unique())
sales_team = st.sidebar.selectbox("Select Sales Team", df['Sales Team'].unique())
product = st.sidebar.selectbox("Select Product", df['Item Name'].unique())
customer = st.sidebar.selectbox("Select Customer", df['Customer'].unique())

# Header
st.title("Elbrit Sales Dashboard")
st.markdown("An interactive dashboard to analyze sales data and answer business questions.")

# Visualization: Overall Primary Sales by Month
st.header("Primary Sales by Month")
monthly_sales = df.groupby(df['Date'].dt.month_name())['Primary Sales'].sum().reset_index()
fig = px.bar(monthly_sales, x='Date', y='Primary Sales', title="Primary Sales by Month", labels={"Date": "Month"})
st.plotly_chart(fig)

# Q1: Highest-Selling Product in Selected Month
st.subheader("Highest-Selling Product in Selected Month")
month_data = df[df['Date'].dt.month_name() == month]
highest_selling_product = month_data.groupby('Item Name')['Primary Sales'].sum().idxmax()
highest_sales_value = month_data.groupby('Item Name')['Primary Sales'].sum().max()
st.write(f"In **{month}**, the highest-selling product was **{highest_selling_product}** with sales of **{highest_sales_value:.2f}**.")

# Q2: Product with Highest Sales for Selected Sales Team in Selected Month
st.subheader("Product with Highest Sales for Selected Sales Team in Selected Month")
team_data = month_data[month_data['Sales Team'] == sales_team]
if not team_data.empty:
    highest_team_product = team_data.groupby('Item Name')['Primary Sales'].sum().idxmax()
    highest_team_sales = team_data.groupby('Item Name')['Primary Sales'].sum().max()
    st.write(f"For the sales team **{sales_team}**, the product with highest sales was **{highest_team_product}** with **{highest_team_sales:.2f}**.")
else:
    st.write("No sales data available for the selected sales team in this month.")

# Q3: Customer with Maximum Stock Returns for Selected HQ in October
st.subheader("Customer with Maximum Stock Returns in October")
october_data = df[(df['Date'].dt.month == 10) & (df['HQ'] == hq)]
if not october_data.empty:
    max_returns_customer = october_data.groupby('Customer')['Quantity'].sum().idxmin()
    max_returns_quantity = october_data.groupby('Customer')['Quantity'].sum().min()
    st.write(f"In October, the customer with the most stock returns at **{hq}** was **{max_returns_customer}**, returning **{abs(max_returns_quantity)} units**.")
else:
    st.write("No stock return data available for October at the selected HQ.")

# Q4: Sales Team with Maximum Percentage of Expired Returns
st.subheader("Sales Team with Maximum Percentage of Expired Returns")
expiry_data = df[df['Return for Reason'] == 'Expired']
if not expiry_data.empty:
    expiry_percentage = (
        expiry_data.groupby('Sales Team')['Against Expiry'].sum() /
        expiry_data.groupby('Sales Team')['Primary Sales'].sum()
    ).sort_values(ascending=False)
    top_team = expiry_percentage.idxmax()
    top_team_percentage = expiry_percentage.max() * 100
    st.write(f"The sales team with the highest percentage of expired returns is **{top_team}** with **{top_team_percentage:.2f}%**.")
else:
    st.write("No expired return data available.")

# Q5: Percentage of Overall Primary Sales Affected by Breakage
st.subheader("Percentage of Sales Affected by Breakage")
total_breakage = df['Breakage'].sum()
total_primary_sales = df['Primary Sales'].sum()
breakage_percentage = (total_breakage / total_primary_sales) * 100
st.write(f"The percentage of primary sales affected by breakage is **{breakage_percentage:.2f}%**.")

# Q6: Primary Sales for Selected HQ in September
st.subheader("Primary Sales for Selected HQ in September")
september_data = df[(df['Date'].dt.month == 9) & (df['HQ'] == hq)]
hq_september_sales = september_data['Primary Sales'].sum()
st.write(f"The total primary sales for **{hq}** in September were **{hq_september_sales:.2f}**.")

# Q7: Sales of Specific Product for Specific Customer under HQ
st.subheader("Sales of Specific Product for Specific Customer under HQ in September")
specific_sales = df[
    (df['Item Name'] == product) &
    (df['Customer'] == customer) &
    (df['HQ'] == hq) &
    (df['Date'].dt.month == 9)
]['Primary Sales'].sum()
st.write(f"The sales of **{product}** for **{customer}** under **{hq}** in September were **{specific_sales:.2f}**.")

# Add a Footer
st.markdown("---")
st.markdown("### Powered by [Streamlit](https://streamlit.io/) | Data Visualization with [Plotly](https://plotly.com/)")
