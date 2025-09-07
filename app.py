import pandas as pd
import streamlit as st
import plotly.express as px
from dbnomics import fetch_series

# --- Load Data ---
@st.cache_data
def load_data():
    countries = ['ABW', 'AFG', 'AGO', 'ALB', 'AND', 'ARE', 'ARG', 'ARM', 'ASM', 'ATG', 'AUS', 'AUT', 'AZE', 'BDI', 'BEL', 'BEN', 'BFA', 'BGD', 'BGR', 'BHR', 'BHS', 'BIH', 'BLR', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'BRN', 'BTN', 'BWA', 'CAF', 'CAN', 'CHE', 'CHL', 'CHN', 'CIV', 'CMR', 'COD', 'COG', 'COL', 'COM', 'CPV', 'CRI', 'CUB', 'CUW', 'CYM', 'CYP', 'CZE', 'DEU', 'DJI', 'DMA', 'DNK', 'DOM', 'DZA', 'ECU', 'EGY', 'ERI', 'ESP', 'EST', 'ETH', 'FIN', 'FJI', 'FRA', 'FRO', 'FSM', 'GAB', 'GBR', 'GEO', 'GHA', 'GIB', 'GIN', 'GMB', 'GNB', 'GNQ', 'GRC', 'GRD', 'GRL', 'GTM', 'GUM', 'GUY', 'HKG', 'HND', 'HRV', 'HTI', 'HUN', 'IDN', 'IND', 'IRL', 'IRN', 'IRQ', 'ISL', 'ISR', 'ITA', 'JAM', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'KHM', 'KIR', 'KNA', 'KOR', 'KWT', 'LAO', 'LBN', 'LBR', 'LBY', 'LCA', 'LIE', 'LKA', 'LSO', 'LTU', 'LUX', 'LVA', 'MAC', 'MAF', 'MAR', 'MCO', 'MDA', 'MDG', 'MDV', 'MEX', 'MHL', 'MKD', 'MLI', 'MLT', 'MMR', 'MNE', 'MNG', 'MNP', 'MOZ', 'MRT', 'MUS', 'MWI', 'MYS', 'NAM', 'NCL', 'NER', 'NGA', 'NIC', 'NLD', 'NOR', 'NPL', 'NRU', 'NZL', 'OMN', 'PAK', 'PAN', 'PER', 'PHL', 'PLW', 'PNG', 'POL', 'PRI', 'PRK', 'PRT', 'PRY', 'PSE', 'PYF', 'QAT', 'ROU', 'RUS', 'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 'SLB', 'SLE', 'SLV', 'SMR', 'SOM', 'SRB', 'SSD', 'STP', 'SUR', 'SVK', 'SVN', 'SWE', 'SWZ', 'SXM', 'SYC', 'SYR', 'TCA', 'TCD', 'TGO', 'THA', 'TJK', 'TKM', 'TLS', 'TON', 'TTO', 'TUN', 'TUR', 'TUV', 'TZA', 'UGA', 'UKR', 'URY', 'USA', 'UZB', 'VCT', 'VEN', 'VGB', 'VIR', 'VNM', 'VUT', 'WSM', 'XKX', 'YEM', 'ZAF', 'ZMB', 'ZWE']

    df = fetch_series('WB', 'WDI', dimensions={
         "frequency": ["A"],
         "indicator": ["EG.FEC.RNEW.ZS"],
         "country": countries
        },
         max_nb_series=300).query("period >= '1990'").query("period <= '2021'").reset_index(drop=True)

    df = df[['period', 'value', 'country', 'country (label)']]
    df = df.rename(columns={'period': 'Year', 'value': 'Value', 'country': 'Country Code', 'country (label)': 'Country Name'})
    return df

df = load_data()

# --- Page Configuration and Title ---
st.set_page_config(layout="wide")
st.title('World Bank Data on Renewable Energy Consumption')


# --- Main Content with Tabs ---
# Use st.tabs to create separate sections for the data, charts and insights.
tab0, tab1, tab2, tab3 = st.tabs(["Data", "Trends", "Annual Snapshot", "Insights"])

# --- Tab 0: Data ---
with tab0:
    st.header("Data Source")

    # Data Attribution section
    st.subheader('Attribution')
    st.write('**The World Bank** (https://worldbank.org)')
    st.write('**Dataset Name:** Renewable Energy Consumption (% of Total Final Energy Consumption) (https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS)')
    st.write('**Data Source:** IEA Energy Statistics Data Browser, International Energy Agency ( IEA ), uri: iea.org/data-and-statistics/data-tools/energy-statistics-data-browser, publisher: International Energy Agency ( IEA ), data accessed: 2025-03-25')
    st.write('**License:** CC BY-4.0 ')

    st.markdown("---")

    st.header("Full Dataset")
    st.dataframe(df, use_container_width=True)

# --- Tab 1: Trends ---
with tab1:
    st.header("Renewable Energy Consumption Trends Over Time")
    
    # Setting the dropdown list for the line chart
    regions = st.multiselect(
        'Choose Country or Region for Trends',
        list(df['Country Name'].unique()),
        default=['United Kingdom', 'United States', 'Japan', 'Germany', 'Australia', 'China', 'India']
    )
    # --- Create a color map for consistent colors on the line chart ---
    # This ensures that each country/region always has the same color.
    all_regions = list(df['Country Name'].unique())
    colors = px.colors.qualitative.Plotly
    color_map = {region: colors[i % len(colors)] for i, region in enumerate(all_regions)}
    
    # Create the line chart
    new_df = df[df['Country Name'].isin(regions)]
    fignew = px.line(
        new_df,
        x='Year',
        y='Value',
        color='Country Name',
        color_discrete_map=color_map, # Add the fixed color map here,
        title="Renewable Energy Consumption (% of Total Final Energy Consumption)"
    )
    # Update the layout to rename the axis titles
    fignew.update_layout(
      xaxis_title=None,
      yaxis_title=None
    )
    st.plotly_chart(fignew, use_container_width=True)

# --- Tab 2: Annual Snapshot ---
with tab2:
    st.header("Annual Global Snapshot")

    # Setting the year selection for the map
    years = st.selectbox(
        'Choose Year for Annual Snapshot',
        sorted(list(df['Year'].unique()), reverse=True)
    )

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

# --- Tab 3: Insights ---
with tab3:
    st.header("Insights")

    # Concluding remarks formatted with a clear structure
    #st.subheader("Concluding Remarks")
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

    st.link_button("Go to REN21 GSR", "https://www.ren21.net/gsr-2024/")
