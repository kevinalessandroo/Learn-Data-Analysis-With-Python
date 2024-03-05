Certainly! It looks like you want to refactor your Streamlit app code to make it different from the previous one but still maintain the same functionality. Here's a refactored version with some changes in structure and style:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day = pd.read_csv("Dashboard/day.csv")

# Clean and transform data
day.drop(columns=['windspeed'], inplace=True)

column_mapping = {
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}

day.rename(columns=column_mapping, inplace=True)

month_mapping = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weekday_mapping = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
weather_cond_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
}

day['month'] = day['month'].map(month_mapping)
day['season'] = day['season'].map(season_mapping)
day['weekday'] = day['weekday'].map(weekday_mapping)
day['weather_cond'] = day['weather_cond'].map(weather_cond_mapping)

# Sidebar filter
min_date = pd.to_datetime(day['dateday']).dt.date.min()
max_date = pd.to_datetime(day['dateday']).dt.date.max()

with st.sidebar:
    st.image('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEAAA//9k=')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day[(day['dateday'] >= str(start_date)) & (day['dateday'] <= str(end_date))]

# Create various dataframes
daily_rent_df = main_df.groupby(by='dateday').agg({'count': 'sum'}).reset_index()
daily_casual_rent_df = main_df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
daily_registered_rent_df = main_df.groupby(by='dateday').agg({'registered': 'sum'}).reset_index()
season_rent_df = main_df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
monthly_rent_df = main_df.groupby(by='month').agg({'count': 'sum'}).reindex(month_mapping.values(), fill_value=0)
weekday_rent_df = main_df.groupby(by='weekday').agg({'count': 'sum'}).reset_index()
workingday_rent_df = main_df.groupby(by='workingday').agg({'count': 'sum'}).reset_index()
holiday_rent_df = main_df.groupby(by='holiday').agg({'count': 'sum'}).reset_index()
weather_rent_df = main_df.groupby(by='weather_cond').agg({'count': 'sum'})

# Create Dashboard
st.header('Bike Rental Dashboard 🚲')

# Daily Rentals
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Casual User', value=daily_casual_rent_df['casual'].sum())

with col2:
    st.metric('Registered User', value=daily_registered_rent_df['registered'].sum())

with col3:
    st.metric('Total User', value=daily_rent_df['count'].sum())

# Monthly Rentals
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(monthly_rent_df.index, monthly_rent_df['count'], marker='o', linewidth=2, color='tab:blue')

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Seasonal Rentals
st.subheader('Seasonly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(x='season', y='registered', data=season_rent_df, label='Registered', color='tab:blue', ax=ax)
sns.barplot(x='season', y='casual', data=season_rent_df, label='Casual', color='tab:orange', ax=ax)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Weatherly Rentals
st.subheader('Weatherly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

colors = ["tab:blue", "tab:orange", "tab:green"]

sns.barplot(x=weather_rent_df.index, y=weather_rent_df['count'], palette=colors, ax=ax)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x',
