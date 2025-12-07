# 📊 Data Driven Stock Analysis Dashboard

A comprehensive Streamlit-based web application for analyzing Indian stock market data with interactive visualizations, technical analysis, and sector performance metrics.

## 🎯 Overview

This project provides an interactive dashboard for analyzing stock market data including:
- **Volatility Analysis** - Identify the most volatile stocks
- **Cumulative Return Analysis** - Track stock performance over time
- **Monthly Gainers & Losers** - Monthly performance tracking
- **Stock Correlation Heatmap** - Identify correlated stocks
- **Sector Performance** - Average returns by sector

## 📋 Project Structure

```
DS_Data Driven Stock Analysis/
├── main.py                          # Streamlit app entry point
├── pyproject.toml                   # Project dependencies & metadata
├── README.md                        # This file
│
├── helper/                          # Helper modules
│   ├── dbhelper.py                 # Database connection & queries
│   └── helper.py                   # Utility functions
│
├── view/                            # Page modules (Streamlit pages)
│   ├── volatility.py               # Volatility analysis page
│   ├── cumulative_return.py        # Cumulative return analysis page
│   ├── monthly_gainers_losers.py   # Monthly performance page
│   ├── stock_correlation.py        # Correlation heatmap page
│   ├── stock_return.py             # Sector return analysis page
│   └── __init__.py                 # Package initialization
│
├── stock_data/                      # Raw YAML stock data (organized by month)
│   ├── 2023-10/
│   ├── 2023-11/
│   ├── ...
│   └── 2024-11/
│
├── stock_csv_data/                  # Extracted CSV files for each stock ticker
│   ├── ADANIENT.csv
│   ├── HDFCBANK.csv
│   ├── TCS.csv
│   └── ... (50+ stocks)
│
├── cleaned_data/                    # Processed & cleaned data
│   ├── all_stock_data.csv          # Combined stock data
│   ├── sector_stock_data.csv       # Stock data with sector info
│   └── sector.csv                  # Sector mapping
│
├── Analysis.ipynb                   # Jupyter notebook for exploratory analysis
├── Extract.ipynb                    # Jupyter notebook for data extraction
│
└── prediction/                      # Analysis results & visualizations
    ├── volatility/                  # Volatility analysis results
    │   ├── top_10_volatility_bar_chart.png
    │   └── top_10_volatility.csv
    ├── Cumulative_Return/           # Cumulative return analysis results
    │   ├── top_5_cumulative_return_line_chart.png
    │   └── top_5_cumulative_return_final.csv
    ├── monthly_gainers_losers/      # Monthly performance results
    │   ├── monthly_gainers_losers_*.png
    │   └── monthly_top5_gainers_losers_data.csv
    ├── stock_correlation_heatmap/   # Correlation analysis results
    │   ├── stock_correlation_heatmap.png
    │   └── stock_correlation_matrix.csv
    └── sector_return/               # Sector performance results
        ├── average_sector_return_bar_chart.png
        └── average_sector_return_data.csv
```

## 🗄️ Database Schema

### Tables

#### `stock_data`
Stores historical stock price data for all tickers.

```sql
CREATE TABLE `stock_analysis`.`stock_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ticker` VARCHAR(100) NULL,
  `close` DECIMAL(10,2) NULL,
  `date` VARCHAR(45) NULL,
  `high` DECIMAL(10,2) NULL,
  `low` DECIMAL(10,2) NULL,
  `month` VARCHAR(10) NULL,
  `open` DECIMAL(10,2) NULL,
  `volume` INT NULL,
  PRIMARY KEY (`id`)
) COMMENT = 'contains the stockdata';
```

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| ticker | VARCHAR(100) | Stock ticker symbol (e.g., HDFCBANK, TCS) |
| close | DECIMAL(10,2) | Closing price |
| date | VARCHAR(45) | Trading date |
| high | DECIMAL(10,2) | Daily high price |
| low | DECIMAL(10,2) | Daily low price |
| month | VARCHAR(10) | Month identifier (YYYY-MM) |
| open | DECIMAL(10,2) | Opening price |
| volume | INT | Trading volume |

#### `sector_data`
Maps stocks to their respective sectors.

```sql
CREATE TABLE `stock_analysis`.`sector_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Company` VARCHAR(150) NULL,
  `Sector` VARCHAR(100) NULL,
  `Symbol` TEXT(600) NULL,
  `Ticker` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ticker_idx` (`Ticker` ASC) VISIBLE,
  CONSTRAINT `fk_ticker`
    FOREIGN KEY (`Ticker`)
    REFERENCES `stock_analysis`.`stock_data` (`ticker`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) COMMENT = 'sector data for the stocks';
```

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| Company | VARCHAR(150) | Company name |
| Sector | VARCHAR(100) | Sector name |
| Symbol | TEXT(600) | Stock symbol |
| Ticker | VARCHAR(100) | Stock ticker (Foreign Key) |

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- MySQL Server running
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "DS_Data Driven Stock Analysis"
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create MySQL database `stock_analysis`
   - Run the SQL schema scripts provided in the database section
   - Update database credentials in `helper/dbhelper.py`

4. **Configure Database Connection**
   
   Edit `helper/dbhelper.py`:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "your_mysql_user",
       "password": "your_mysql_password",
       "database": "stock_analysis"
   }
   ```

### Running the Application

```bash
# Start the Streamlit app
streamlit run main.py
```

The dashboard will be available at `http://localhost:8501`

## 📊 Features

### 1. 📈 Volatility Analysis
- Calculates standard deviation of daily returns
- Displays top 10 most volatile stocks
- Generates bar charts and CSV exports

### 2. 💹 Cumulative Return Analysis
- Tracks cumulative returns over the entire period
- Displays top 5 performing stocks
- Line chart visualization showing performance trends

### 3. 🏆 Monthly Gainers & Losers
- Monthly performance tracking
- Top 5 gainers and losers per month
- Color-coded visualization (green for gains, red for losses)

### 4. 🔗 Stock Correlation Heatmap
- Correlation matrix of all stock prices
- Visual heatmap representation
- Identifies highly correlated stocks

### 5. 📊 Sector Performance
- Average returns by sector
- Sector comparison analysis
- Color-coded by performance (positive/negative)

## 🔧 Architecture

### Main Components

**main.py** - Streamlit application entry point
- Session state management for page navigation
- Dynamic CSS for active button highlighting
- Page routing logic

**helper/dbhelper.py** - Database utilities
- Connection pooling
- Query execution methods
- Data fetching operations

**view/** - Page modules
- Each module contains a `show()` function
- Renders specific analysis visualizations
- Imports data and generates charts

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.52.1 | Web framework |
| pandas | >=2.3.3 | Data manipulation |
| matplotlib | >=3.10.7 | Visualization |
| plotly | >=6.5.0 | Interactive charts |
| mysql-connector-python | >=9.5.0 | Database connection |
| numpy | (implicit) | Numerical operations |
| pyyaml | >=6.0.3 | YAML parsing |

## 📝 Data Processing Workflow

1. **Extract** - Raw YAML files → CSV extraction
2. **Clean** - Data validation and standardization
3. **Transform** - Merge with sector information
4. **Analyze** - Calculate metrics and returns
5. **Visualize** - Generate dashboard displays

## 🎨 UI Features

- **Responsive Design** - Adapts to different screen sizes
- **Navigation Buttons** - Sidebar navigation with active state highlighting
- **Interactive Charts** - Hover tooltips and zoomable visualizations
- **Color Coding** - Green for positive returns, red for negative
- **Emojis** - Visual indicators for each analysis type

## 📈 Sample Analysis Outputs

All analysis outputs are saved in the `prediction/` directory with the following structure:

| Directory | Contents |
|-----------|----------|
| `prediction/volatility/` | Top 10 volatility chart & CSV data |
| `prediction/Cumulative_Return/` | Cumulative return line chart & CSV data |
| `prediction/monthly_gainers_losers/` | Monthly performance charts & consolidated CSV |
| `prediction/stock_correlation_heatmap/` | Correlation heatmap visualization & matrix CSV |
| `prediction/sector_return/` | Sector performance bar chart & CSV data |

## 🔐 Security Notes

⚠️ **Important**: Database credentials in `helper/dbhelper.py` should be moved to environment variables for production:

```python
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "stock_analysis")
}
```

## 📚 Jupyter Notebooks

- **Analysis.ipynb** - Exploratory data analysis and visualization experiments
- **Extract.ipynb** - Data extraction pipeline from raw YAML files

## 🐛 Troubleshooting

### Database Connection Issues
```
Error: MySQL connection failed
Solution: Verify MySQL server is running and credentials are correct
```

### Missing Data
```
Error: CSV files not found
Solution: Run Extract.ipynb to generate CSV files from raw data
```

### Port Already in Use
```
Error: Streamlit port 8501 already in use
Solution: streamlit run main.py --server.port 8502
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact & Support

For issues, questions, or suggestions, please open an issue on the repository.

---

**Last Updated**: December 2025  
**Status**: Active Development  
**Stocks Covered**: 50+ Indian stocks (NSE)
