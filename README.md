# Laptop Price Comparison - Indian E-commerce Platforms
A professional Streamlit web application for comparing laptop prices across major Indian e-commerce platforms including Amazon, Flipkart, and Reliance Digital.
## Features
- **Interactive Dashboard**: Professional layout with comprehensive filtering options
- **Multi-Platform Comparison**: Compare prices across Amazon, Flipkart, and Reliance Digital
- **Advanced Filtering**: Filter by brand, price range, platform, and city
- **Interactive Visualizations**: 5 different chart types using Plotly
  - Bar chart: Average price per platform
  - Box plot: Price distribution per brand  
  - Line graph: Price trends over time
  - Pie chart: Platform market share
  - Scatter plot: Rating vs Price correlation
- **Smart Recommendations**: Automatically identifies the top 2 cheapest platforms
- **City-wise Analysis**: Focus on Bhopal with support for multiple Indian cities
## Tech Stack
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualizations**: Plotly Express & Graph Objects
- **Deployment**: Streamlit Cloud ready
## Installation & Setup
### For Local Development
1. Clone the repository:
```bash
git clone <your-repository-url>
cd laptop-price-comparison
Install dependencies:
pip install -r requirements.txt
Run the application:
streamlit run app.py
For Streamlit Cloud Deployment
Fork or upload this repository to GitHub
Go to Streamlit Cloud
Connect your GitHub account
Select your repository
Set the main file path to: app.py
Deploy!
The app will be available at your Streamlit Cloud URL.

Project Structure
laptop-price-comparison/
├── app.py                      # Main Streamlit application
├── data/
│   └── laptop_prices.csv      # Dataset with laptop pricing data
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── requirements.txt           # Python dependencies for Streamlit Cloud
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore rules
Dataset Information
The data/laptop_prices.csv file contains:

platform: E-commerce platform (Amazon, Flipkart, Reliance Digital)
brand: Laptop brand (Dell, HP, Lenovo, Acer, ASUS)
model: Specific laptop model
price: Price in Indian Rupees (₹)
city: Indian city (Bhopal, Mumbai, Delhi, Bangalore, Chennai, Pune, Hyderabad)
rating: Customer rating (1-5 scale)
date: Date of price record
Features in Detail
Interactive Filters
Brand Selection: Choose specific laptop brands or view all
Price Range: Set minimum and maximum price limits
Platform Filter: Focus on specific e-commerce platforms
City Filter: Default set to Bhopal, expandable to other cities
Visualizations
Bar Chart: Compare average prices across platforms
Box Plot: Analyze price distribution by brand
Line Chart: View price trends over time
Pie Chart: Platform market share analysis
Scatter Plot: Rating vs Price correlation
Smart Recommendations
Automatically identifies the top 2 cheapest platforms
Shows average price, lowest price, and product count
Updates dynamically based on applied filters
Author
Made with ❤️ by Somya Nigam

LinkedIn: https://www.linkedin.com/in/somya-nigam-789408183/
Project built using Python & Streamlit
License
This project is open source and available under the MIT License.
