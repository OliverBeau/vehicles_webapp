import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv("vehicles_us.csv")

# Convert price to numeric before any operations
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Remove rows with NaN price
df = df.dropna(subset=['price'])

# Display basic app info
st.title("Vehicle Data Analysis")
st.write("This app analyzes vehicle data from the US.")
st.write("The dataset contains information about various vehicles, including their make, model, year, and price.\n Cars less than \$500 or greater than $100,000 are removed from the dataset.")

# Show data overview
st.header("Data Overview")
st.write("The dataset contains the following columns:")
st.write(df.columns.tolist())
st.write("The dataset contains the following number of rows:")
st.write(len(df))

# Display the first few rows - avoid Arrow conversion issues
st.write("The first few rows of the dataset:")
# Create a copy of the head data and reset the index
# display_df = df.head().copy().reset_index(drop=True)
# Convert problematic columns explicitly to Python types
for col in display_df.columns:
    if pd.api.types.is_numeric_dtype(display_df[col]):
        display_df[col] = display_df[col].astype(str).astype(object)
# Use st.table which doesn't use Arrow conversion
st.table(display_df)


df = df.dropna(subset=['price', 'type', 'fuel', 'model_year'])
df = df[(df['price'] > 500) & (df['price'] < 100000)]  # Filter out extreme prices


option = st.sidebar.selectbox(
    'Select Graph to Display',
    ('Fuel Types Over Time', 'Average Price by Vehicle Type', 'Volume Trends by Brand',
     'Price Distribution by Brand', 'Miles vs. Condition', 'Price vs. Year',
     'Price vs. Year for Selected Brand')
)

# Graph 1: Fuel Types Over Time
if option == 'Fuel Types Over Time':
    df_fuel_time = df.dropna(subset=['fuel', 'model_year'])
    fuel_year_counts = (
        df_fuel_time.groupby(['fuel', 'model_year'])
        .size()
        .reset_index(name='count')
    )
    fig = px.line(
        fuel_year_counts,
        x='model_year',
        y='count',
        color='fuel',
        markers=True,
        title='Fuel Types Over Time',
        labels={'model_year': 'Model Year', 'count': 'Number of Listings', 'fuel': 'Fuel Type'}
    )
    st.plotly_chart(fig)

# Graph 2: Average Price by Vehicle Type
elif option == 'Average Price by Vehicle Type':
    df_type_price = df.dropna(subset=['price', 'type'])
    avg_price_by_type = (
        df_type_price.groupby('type')['price']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        avg_price_by_type,
        x='type',
        y='price',
        title='Average Price by Vehicle Type',
        labels={'price': 'Average Price ($)', 'type': 'Vehicle Type'}
    )
    st.plotly_chart(fig)

# Graph 3: Volume Trends by Brand
elif option == 'Volume Trends by Brand':
    df_brand_time = df.dropna(subset=['price', 'model', 'model_year'])
    df_brand_time['brand'] = df_brand_time['model'].str.split().str[0].str.lower()
    brand_year_counts = (
        df_brand_time.groupby(['brand', 'model_year'])
        .size()
        .reset_index(name='count')
    )
    fig = px.line(
        brand_year_counts,
        x='model_year',
        y='count',
        color='brand',
        markers=True,
        title='Volume Trends by Brand Over Time',
        labels={'model_year': 'Model Year', 'count': 'Number of Listings', 'brand': 'Brand'}
    )
    st.plotly_chart(fig)

# Graph 4: Price Distribution by Brand (Histogram)
elif option == 'Price Distribution by Brand':
    df_brand_price = df.dropna(subset=['price', 'model'])
    df_brand_price['brand'] = df_brand_price['model'].str.split().str[0].str.lower()

    # Filter out extreme price values (optional, adjust thresholds as needed)
    df_brand_price = df_brand_price[(df_brand_price['price'] > 500) & (df_brand_price['price'] < 100000)]

    # Create a histogram for price distribution by brand
    fig = px.histogram(
        df_brand_price,
        x='price',
        color='brand',
        title='Price Distribution by Brand',
        labels={'price': 'Price ($)', 'brand': 'Brand'},
        nbins=50,  # Adjust the number of bins
        marginal='rug',  # Add a marginal rug plot
        opacity=0.7  # Adjust opacity for better visualization
    )
    st.plotly_chart(fig)

# Graph 5: Miles vs. Condition
elif option == 'Miles vs. Condition':
    df_cond_odometer = df.dropna(subset=['odometer', 'condition'])
    fig = px.scatter(
        df_cond_odometer,
        x='condition',
        y='odometer',
        title='Miles vs. Condition',
        labels={'odometer': 'Odometer (miles)', 'condition': 'Condition'},
        opacity=0.6
    )
    st.plotly_chart(fig)

# Graph 6: Price vs. Year
elif option == 'Price vs. Year':
    df_year_price = df.dropna(subset=['price', 'model_year'])
    fig = px.scatter(
        df_year_price,
        x='model_year',
        y='price',
        title='Price vs. Model Year',
        labels={'price': 'Price ($)', 'model_year': 'Model Year'},
        opacity=0.6
    )
    st.plotly_chart(fig)

# Graph 7: Price vs. Year for Selected Brand
elif option == 'Price vs. Year for Selected Brand':
    # Get the unique brands from the model column
    df['brand'] = df['model'].str.split().str[0].str.lower()
    brands = df['brand'].unique()
    
    # Allow the user to select a brand
    selected_brand = st.sidebar.selectbox('Select Brand', brands)
    
    # Filter the dataset for the selected brand
    df_selected_brand = df[df['brand'] == selected_brand].dropna(subset=['price', 'model_year'])
    
    # Plot Price vs. Year for the selected brand
    fig = px.scatter(
        df_selected_brand,
        x='model_year',
        y='price',
        title=f'Price vs. Year for {selected_brand.capitalize()}',
        labels={'price': 'Price ($)', 'model_year': 'Model Year'},
        opacity=0.6
    )
    st.plotly_chart(fig)