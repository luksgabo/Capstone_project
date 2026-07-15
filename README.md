# SpaceX Launch Success Prediction - IBM Data Science Capstone Project

## Project Overview

This capstone project for the IBM Data Science Professional Certificate predicts the success of SpaceX Falcon 9 rocket launches using machine learning techniques. The project demonstrates a complete data science workflow: from data collection and wrangling through exploratory data analysis to building and evaluating predictive models.

## Objectives

- **Collect** SpaceX launch data using the SpaceX API and web scraping
- **Prepare and clean** the dataset for analysis and modeling
- **Explore and visualize** launch patterns and success factors
- **Build predictive models** to classify launch outcomes
- **Create an interactive dashboard** to visualize key insights
- **Present findings** using data-driven insights

## Dataset

The project uses SpaceX launch data including:
- **Launch Sites**: Kennedy Space Center, Vandenberg Space Force Base, Cape Canaveral, etc.
- **Rocket Type**: Falcon 1, Falcon 9, Falcon Heavy
- **Payload Information**: Mass, type, and destination orbits
- **Launch Outcomes**: Successful or failed landings/launches
- **Geographic Data**: Launch site coordinates and landing zones

### Data Sources
- SpaceX REST API (`https://api.spacexdata.com/v4/`)
-- however there was a problem accessing the API and some counter actions had to be made.
- Web scraping of SpaceX Wikipedia pages
- Preprocessed datasets from IBM Cloud Object Storage

## Project Structure

```
├── data_collection.py / data_collection.ipynb       # Fetch data from SpaceX API
├── data_wrangling.py / data_wrangling.ipynb         # Clean and preprocess data
├── exploratory_data_analysis*.py / .ipynb           # EDA and initial insights
├── launch_sites_visualization.py / .ipynb           # Geographic visualization of launch sites
├── prediction_model.py / prediction_model.ipynb     # ML model development and evaluation
├── spacex-dash-app.py / spacex-dash-app.ipynb       # Interactive Dash dashboard
├── webscrapping.py / webscrapping.ipynb             # Web scraping data collection
├── data/                                            # Processed datasets
├── presentation/                                    # Final presentation materials
└── README.md                                        # You're here!
```

## Project Phases

### Phase 1: Data Collection
- Query the SpaceX API to retrieve launch records
- Web scrape additional data from SpaceX sources
- Combine multiple data sources into a unified dataset
- Extract rocket booster versions, launch sites, and payload information

**Key Files**: `data_collection.py`, `webscrapping.py`

### Phase 2: Data Wrangling & Preprocessing
- Handle missing values and data inconsistencies
- Create target variable for launch success
- Perform feature engineering (e.g., orbital category, payload type encoding)
- Standardize and normalize features for modeling

**Key Files**: `data_wrangling.py`

### Phase 3: Exploratory Data Analysis (EDA)
- Analyze launch success rates by various dimensions
- Identify patterns in payload mass, launch site, and orbit type
- Examine temporal trends in SpaceX launches
- Create visualizations to understand relationships between features

**Key Files**: `exploratory_data_analysis.py`, `exploratory_data_analysis2.py`

### Phase 4: Visualization & Dashboard
- Develop interactive geographic map showing launch sites
- Create a Dash web application with:
  - Launch site filtering
  - Success vs. failure pie charts
  - Payload mass vs. success scatter plots
  - Payload range slider for dynamic filtering

**Key Files**: `launch_sites_visualization.py`, `spacex-dash-app.py`

### Phase 5: Predictive Modeling
- Train multiple ML classifiers:
  - Logistic Regression
  - Support Vector Machine (SVM)
  - Decision Tree Classifier
  - K-Nearest Neighbors (KNN)
- Perform hyperparameter tuning with GridSearchCV
- Evaluate models using accuracy, confusion matrices, and classification metrics
- Select the best-performing model

**Key Files**: `prediction_model.py`

## Technologies & Libraries

### Data Science & Analysis
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **scikit-learn**: Machine learning models and preprocessing

### Visualization
- **Matplotlib**: Static plotting
- **Seaborn**: Statistical data visualization
- **Plotly**: Interactive visualizations
- **Dash**: Web-based interactive dashboard

### Data Collection
- **requests**: HTTP library for API calls
- **BeautifulSoup**: Web scraping

## Key Findings & Results

- **Model Performance**: The prediction models achieved varying levels of accuracy across different algorithms
- **Launch Site Insights**: Certain launch sites show higher success rates
- **Payload Factor**: Launch success correlates with payload mass characteristics
- **Temporal Trends**: SpaceX's success rate has improved over time with booster iterations
- **Orbital Type**: Success rates vary significantly by orbital classification

## Datasets Generated

- `dataset_part_1.csv` - Initial dataset with basic launch information
- `dataset_part2.csv` - Enhanced dataset with derived features
- `dataset_part3.csv` - Final processed features for ML models
- `spacex_launch_dash.csv` - Cleaned data for dashboard visualization
- `spacex_web_scraped.csv` - Web-scraped launch data

## References

- [SpaceX API Documentation](https://docs.spacexdata.com/)
- [IBM Data Science Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-science)
- SpaceX Historical Launch Data

**Last Updated**: July 2024
