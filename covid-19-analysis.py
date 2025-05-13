import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# 1. Data Loading

# Load the dataset
file_path = 'owid-covid-data.csv'
df = pd.read_csv(file_path)

# 2. Data Preprocessing

# Preview data
print("First 5 rows:")
print(df.head())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# View unique countries
df['location'].unique()

# 3. Data Cleaning

# Filter relevant countries
countries = ['Kenya', 'United States', 'India']
df = df[df['location'].isin(countries)]

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# Drop rows with missing 'total_cases' or 'total_deaths'
df = df.dropna(subset=['total_cases', 'total_deaths'])

# Fill or interpolate other missing numeric values
df.fillna(method='ffill', inplace=True)


# 4. Data Exploration (EDA)

# Plot total cases over time
plt.figure(figsize=(10,6))
for country in countries:
    country_df = df[df['location'] == country]
    plt.plot(country_df['date'], country_df['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.grid()
plt.show()

# Death rate calculation
df['death_rate'] = df['total_deaths'] / df['total_cases']


# 5. Vaccination Progress

# Plot total vaccinations
plt.figure(figsize=(10,6))
for country in countries:
    country_df = df[df['location'] == country]
    plt.plot(country_df['date'], country_df['total_vaccinations'], label=country)
plt.title('Total Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.grid()
plt.show()

# % of population vaccinated
df['percent_vaccinated'] = (df['total_vaccinations'] / df['population']) * 100


# 6. Choropleth Map Visualization

# Get the latest available data for each country
latest_df = df.sort_values('date').groupby('location', as_index=False).last()

# Filter out regions that are not individual countries (based on iso_code length)
latest_df = latest_df[latest_df['iso_code'].str.len() == 3]

# Fill missing values with 0 for mapping
latest_df['total_cases'] = latest_df['total_cases'].fillna(0)
latest_df['total_vaccinations'] = latest_df['total_vaccinations'].fillna(0)

# Choropleth: Total Cases
fig_cases = px.choropleth(
    latest_df,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    color_continuous_scale="Reds",
    title="🌍 Total COVID-19 Cases by Country (Latest)"
)
fig_cases.show()

# Optional: Choropleth of vaccination rate if population is available
if 'population' in latest_df.columns:
    latest_df['percent_vaccinated'] = (latest_df['total_vaccinations'] / latest_df['population']) * 100
    fig_vax = px.choropleth(
        latest_df,
        locations="iso_code",
        color="percent_vaccinated",
        hover_name="location",
        color_continuous_scale="Greens",
        title="💉 Percent Vaccinated by Country (Latest)"
    )
    fig_vax.show()