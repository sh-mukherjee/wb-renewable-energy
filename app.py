import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# --- Load Data ---
# It's good practice to add caching for data loading to improve performance
@st.cache_data
def load_data():
    df = pd.read_csv('renewable_energy_long_format.csv')
    return df

df = load_data()

# --- Page Configuration and Title ---
st.set_page_config(layout="wide")
st.title('World Bank Data on Renewable Energy Consumption')

# --- Sidebar for User Inputs ---
# Placing the selectors in a sidebar makes the main dashboard area cleaner.
with st.sidebar:
    st.header('Dashboard Controls')
    
    # Setting the dropdown list for the line chart
    regions = st.multiselect(
        'Choose Country or Region for Line Chart', 
        list(df['Country Name'].unique()), 
        default=['United Kingdom', 'United States', 'Japan', 'Germany', 'Australia', 'China', 'India']
    )
    
    # Setting the year selection for the map
    years = st.selectbox(
        'Choose Year for Map', 
        sorted(list(df['Year'].unique()), reverse=True)
    )

# --- Main Content with Tabs ---
# Use st.tabs to create separate sections for the dashboard and insights.
tab1, tab2 = st.tabs(["Dashboard", "Insights"])

# --- Tab 1: Dashboard ---
with tab1:
    st.header("Interactive Visualizations")
    
    # Create the line chart
    new_df = df[df['Country Name'].isin(regions)]
    fignew = px.line(
        new_df, 
        x='Year', 
        y='Value', 
        color='Country Name', 
        title='Renewable Energy Consumption Over Time by Country/Region'
    )
    st.plotly_chart(fignew, use_container_width=True)
    
    # Create the choropleth map
    year_df = df[df['Year'] == years]
    figmap = px.choropleth(
        year_df,
        locations="Country Code",
        color="Value",
        hover_name="Country Name",
        color_continuous_scale='Greens',
        title=f'Renewable Energy Consumption by Country ({years})'
    )
    st.plotly_chart(figmap, use_container_width=True)

# --- Tab 2: Insights and Attribution ---
with tab2:
    st.header("Insights and Data Information")
    
    # Data Attribution section
    st.subheader('Attribution')
    st.write('**The World Bank** (https://worldbank.org)')
    st.write('**Dataset Name:** Renewable Energy Consumption (% of Total Final Energy Consumption) (https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS)')
    st.write('**Data Source:** World Bank, Sustainable Energy for All (SE4ALL) database from the SE4ALL Global Tracking Framework led jointly by the World Bank, International Energy Agency, and the Energy Sector Management Assistance Program.')
    
    st.markdown("---")
    
    # Concluding remarks formatted with a clear structure
    st.subheader("Concluding Remarks")
    st.write("Play around with the countries and the years to see what percentage of the total energy consumption was from renewable energy sources. Here are some observations:")
    
    st.markdown("""
    * Richer, developed countries generally have a **low percentage** of their total energy coming from renewable sources, though some show an increasing trend.
    * **Iceland**, which makes use of geothermal energy, has a higher proportion of its consumption coming from renewable energy.
    * Many poorer and less-developed countries have **much higher levels** of renewable energy consumption as a percentage of their total energy consumption (e.g., Nepal). This could be due to a combination of hydroelectric power and the use of biomass for domestic energy needs.
    * The line charts for **India** and **China** show a decreasing trend over the years as they have grown richer, perhaps due to rapidly increasing energy demand that cannot be satisfied fast enough by renewable energy.
    """)
    
    st.write("It is important to remember that 'renewable' does not always mean 'clean' or 'sustainable.' Wood, for instance, is technically renewable, but its overuse can lead to deforestation. Hydroelectric power also has potential negative environmental consequences. However, many developing countries are now investing in better renewable energy technologies.")
    
    # External link section
    st.markdown("---")
    st.subheader("Further Reading")
    st.write("For more detailed information, check out the **Renewables Global Status Report (GSR)**, released annually by the Renewable Energy Policy Network for the 21st Century (REN21).")
    st.link_button("Go to REN21 GSR", "https://ren21.net/gsr-2019/")
