# GlobalTech E-Commerce: Full-Stack Data Analysis

This project demonstrates an end-to-end data analysis workflow, going from raw synthetic data generation to SQL-based database management, statistical analysis in Python, and business intelligence reporting.

## 🚀 Project Architecture

Raw Dataset (Python Generated) ➔ MySQL Database ➔ SQL Analysis ➔ Python EDA & Statistics ➔ Excel Summary ➔ Power BI Dashboard

## 📂 Repository Structure

```text
globaltech_ecommerce_analysis/
│
├── README.md                      # Project documentation
├── data/                          
│   ├── raw/                       # Generated raw CSV files
│   └── cleaned/                   # Cleaned output from Python
├── sql/                           # SQL queries (DDL, Cleaning, EDA, Advanced)
├── python/                        
│   ├── data_generation.py         # Script to generate realistic dataset
│   ├── create_notebook.py         # Script to build the Jupyter notebook
│   └── data_analysis.ipynb        # Comprehensive Python EDA & Hypothesis Testing
├── excel/                         # Exported Pivot tables and summary
├── powerbi/                       # DAX measures and Star Schema instructions
└── documentation/                 # Additional reports (if any)
```

## 🛠️ Tools & Technologies Used
- **Database:** MySQL (Primary/Foreign Keys, Views, Window Functions, CTEs)
- **Programming:** Python (Pandas, NumPy, Matplotlib, Seaborn, SciPy)
- **Data Visualization:** Power BI, Jupyter Notebooks
- **Statistics:** Correlation Analysis, Two-Sample T-Tests, Distributions

## 📊 Key Insights & Business Recommendations
1. **Profitability vs. Volume:** The hypothesis test conducted in Python reveals a statistically significant difference in profit margins between Consumer and Corporate segments. *Recommendation:* Allocate more B2B marketing budget to the Corporate segment.
2. **Discount Strategies:** A low correlation was found between higher discounts and increased order quantities for specific electronics. *Recommendation:* Re-evaluate the discount tier structure for the Electronics category to preserve margins.

## ⚙️ How to Reproduce
1. Run `python/data_generation.py` to create the raw dataset.
2. Use the scripts in `sql/` to set up your MySQL database and run the queries.
3. Open `python/data_analysis.ipynb` in Jupyter to view the exploratory data analysis and statistical testing.
4. Follow the guide in `powerbi/dashboard_instructions.md` to build the final interactive dashboard.
