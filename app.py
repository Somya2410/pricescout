import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Laptop Price Comparison - Indian E-commerce",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cheapest-platform {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 10px 0;
        border-top: 1px solid #dee2e6;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the laptop pricing dataset"""
    try:
        df = pd.read_csv('data/laptop_prices.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'data/laptop_prices.csv' exists.")
        return pd.DataFrame()

def preprocess_data(df):
    """Clean and preprocess the dataset"""
    if df.empty:
        return df
    
    # Convert price to numeric, removing currency symbols
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace('[₹,]', '', regex=True), errors='coerce')
    
    # Handle missing values
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['price'])
    
    # Convert date column if exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    return df

def create_price_per_platform_chart(df):
    """Create bar chart showing average price per platform"""
    avg_prices = df.groupby('platform')['price'].mean().reset_index()
    avg_prices = avg_prices.sort_values('price')
    
    fig = px.bar(
        avg_prices, 
        x='platform', 
        y='price',
        title='Average Laptop Price by E-commerce Platform',
        labels={'price': 'Average Price (₹)', 'platform': 'Platform'},
        color='price',
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        xaxis_title="E-commerce Platform",
        yaxis_title="Average Price (₹)",
        showlegend=False,
        height=400
    )
    return fig

def create_price_distribution_chart(df):
    """Create box plot showing price distribution per brand"""
    fig = px.box(
        df, 
        x='brand', 
        y='price',
        title='Price Distribution by Laptop Brand',
        labels={'price': 'Price (₹)', 'brand': 'Brand'},
        color='brand'
    )
    fig.update_layout(
        xaxis_title="Brand",
        yaxis_title="Price (₹)",
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    return fig

def create_price_trend_chart(df):
    """Create line chart showing price trends over time"""
    if 'date' not in df.columns or df['date'].isna().all():
        # Create a placeholder trend chart with sample data
        sample_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        trend_data = pd.DataFrame({
            'date': sample_dates,
            'avg_price': np.random.randint(40000, 80000, len(sample_dates))
        })
        fig = px.line(
            trend_data,
            x='date',
            y='avg_price',
            title='Laptop Price Trends Over Time (Sample Data)',
            labels={'avg_price': 'Average Price (₹)', 'date': 'Date'}
        )
    else:
        monthly_prices = df.groupby(df['date'].dt.to_period('M'))['price'].mean().reset_index()
        monthly_prices['date'] = monthly_prices['date'].dt.to_timestamp()
        
        fig = px.line(
            monthly_prices,
            x='date',
            y='price',
            title='Laptop Price Trends Over Time',
            labels={'price': 'Average Price (₹)', 'date': 'Date'}
        )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Average Price (₹)",
        height=400
    )
    return fig

def create_platform_market_share_chart(df):
    """Create pie chart showing platform market share"""
    platform_counts = df['platform'].value_counts().reset_index()
    platform_counts.columns = ['platform', 'count']
    
    fig = px.pie(
        platform_counts,
        values='count',
        names='platform',
        title='Market Share by E-commerce Platform (Based on Listed Products)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=400)
    return fig

def create_rating_price_scatter(df):
    """Create scatter plot showing rating vs price correlation"""
    if 'rating' not in df.columns or df['rating'].isna().all():
        st.warning("Rating data not available for scatter plot analysis.")
        return None
    
    fig = px.scatter(
        df,
        x='rating',
        y='price',
        color='platform',
        size='price',
        title='Laptop Rating vs Price Analysis',
        labels={'rating': 'Customer Rating', 'price': 'Price (₹)'},
        hover_data=['brand', 'model']
    )
    fig.update_layout(
        xaxis_title="Customer Rating",
        yaxis_title="Price (₹)",
        height=400
    )
    return fig

def identify_cheapest_platforms(df):
    """Identify the top 2 cheapest platforms"""
    platform_stats = df.groupby('platform').agg({
        'price': ['mean', 'min', 'count']
    }).round(2)
    platform_stats.columns = ['avg_price', 'min_price', 'product_count']
    platform_stats = platform_stats.reset_index()
    platform_stats = platform_stats.sort_values('avg_price')
    
    return platform_stats.head(2)

def main():
    # Header
    st.markdown('<h1 class="main-header">Laptop Price Comparison in Indian E-commerce (Bhopal)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore and compare laptop prices across Amazon, Flipkart, Reliance Digital & more</p>', unsafe_allow_html=True)
    
    # Load and preprocess data
    df = load_data()
    if df.empty:
        st.stop()
    
    df = preprocess_data(df)
    
    # Sidebar filters
    st.sidebar.header("Filter Options")
    
    # Brand filter
    brands = ['All'] + list(df['brand'].unique())
    selected_brands = st.sidebar.multiselect(
        "Select Brand(s)",
        options=brands,
        default=['All']
    )
    
    # Price range filter
    min_price, max_price = int(df['price'].min()), int(df['price'].max())
    price_range = st.sidebar.slider(
        "Price Range (₹)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=1000
    )
    
    # Platform filter
    platforms = ['All'] + list(df['platform'].unique())
    selected_platforms = st.sidebar.multiselect(
        "Select E-commerce Platform(s)",
        options=platforms,
        default=['All']
    )
    
    # City filter
    cities = ['All'] + list(df['city'].unique())
    selected_city = st.sidebar.selectbox(
        "Select City",
        options=cities,
        index=cities.index('Bhopal') if 'Bhopal' in cities else 0
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'All' not in selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_range[0]) & 
        (filtered_df['price'] <= price_range[1])
    ]
    
    if 'All' not in selected_platforms:
        filtered_df = filtered_df[filtered_df['platform'].isin(selected_platforms)]
    
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(filtered_df))
    
    with col2:
        if not filtered_df.empty:
            st.metric("Average Price", f"₹{filtered_df['price'].mean():,.0f}")
        else:
            st.metric("Average Price", "₹0")
    
    with col3:
        if not filtered_df.empty:
            st.metric("Lowest Price", f"₹{filtered_df['price'].min():,.0f}")
        else:
            st.metric("Lowest Price", "₹0")
    
    with col4:
        if not filtered_df.empty:
            st.metric("Highest Price", f"₹{filtered_df['price'].max():,.0f}")
        else:
            st.metric("Highest Price", "₹0")
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please adjust your filter criteria.")
        return
    
    # Identify cheapest platforms
    st.subheader("Recommended Platforms (Cheapest Options)")
    cheapest_platforms = identify_cheapest_platforms(filtered_df)
    
    col1, col2 = st.columns(2)
    for idx, (_, platform_data) in enumerate(cheapest_platforms.iterrows()):
        with col1 if idx == 0 else col2:
            st.markdown(f"""
            <div class="cheapest-platform">
                <h4>#{idx + 1} {platform_data['platform']}</h4>
                <p><strong>Average Price:</strong> ₹{platform_data['avg_price']:,.0f}</p>
                <p><strong>Lowest Price:</strong> ₹{platform_data['min_price']:,.0f}</p>
                <p><strong>Products Available:</strong> {platform_data['product_count']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Visualizations
    st.subheader("Interactive Data Visualizations")
    
    # Row 1: Price comparison and distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = create_price_per_platform_chart(filtered_df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = create_price_distribution_chart(filtered_df)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Trend and market share
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = create_price_trend_chart(filtered_df)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = create_platform_market_share_chart(filtered_df)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: Rating vs Price scatter plot
    fig5 = create_rating_price_scatter(filtered_df)
    if fig5:
        st.plotly_chart(fig5, use_container_width=True)
    
    # Data table
    st.subheader("Detailed Product Data")
    st.dataframe(
        filtered_df[['brand', 'model', 'platform', 'price', 'city', 'rating']].sort_values('price'),
        use_container_width=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <p><strong>Made with ❤️ by Somya Nigam</strong></p>
        <p>
            <a href="https://www.linkedin.com/in/somya-nigam-789408183/" target="_blank">LinkedIn Profile</a> | 
            Project built using Python & Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
