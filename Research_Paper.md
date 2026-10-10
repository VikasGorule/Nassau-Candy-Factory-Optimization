# Factory Reallocation & Shipping Optimization Recommendation System for Nassau Candy Distributor

## Abstract

This project develops a data-driven recommendation system to analyze factory performance and explore alternative factory assignments for products distributed by Nassau Candy Distributor. The system uses exploratory data analysis, historical sales and profit metrics, factory-location coordinates, and a machine learning experiment to investigate potential factory reallocation opportunities. An interactive Streamlit dashboard allows users to compare factory performance and explore alternative assignments based on distance or historical factory profitability. The recommendations are preliminary and require additional operational data and validation before implementation.

## 1. Introduction

Factory allocation can influence distribution distance, operational efficiency, and profitability. Assigning products to alternative factories may provide opportunities for improvement, but decisions must consider transportation costs, production capacity, product requirements, and customer delivery locations.

This project examines the available Nassau Candy Distributor dataset and develops an interactive decision-support dashboard for evaluating factory assignments.

## 2. Project Objectives

- Analyze sales, costs, gross profit, order volumes, and product distribution.
- Compare the historical performance of factories.
- Calculate approximate distances between factory locations.
- Rank alternative factory assignments using configurable priorities.
- Evaluate the available data quality and the limitations of shipping-time prediction.
- Provide an interactive dashboard to support further operational investigation.

## 3. Dataset Description

The dataset contains 10,194 records. The analysis uses available order and shipping dates, product information, division, sales, cost, units, shipping mode, and factory-assignment information.

Factory coordinates are used to estimate straight-line distances between locations. Product-to-factory mappings are based on the project's defined mapping. Seven records remained unmapped in the analyzed data and were not assigned to a factory automatically.

## 4. Methodology

### 4.1 Data Cleaning and Exploratory Analysis

The data preparation process includes parsing date fields, checking missing values, calculating lead times, correcting known product-name variations, and reviewing factory mapping coverage.

Exploratory analysis examines sales and gross profit by division, factory-level performance, order distribution, and shipping-date patterns.

### 4.2 Factory Performance Analysis

Factory performance is evaluated using historical sales, costs, gross profit, units sold, order counts, and gross margin.

Gross profit is calculated as sales minus cost. Gross margin is calculated as gross profit divided by sales, multiplied by 100, where sales are nonzero.

### 4.3 Distance-Based Analysis

Factory coordinates are used with the Haversine formula to estimate great-circle distances between factory locations. Alternative factories are ranked by their calculated distance from the currently assigned factory.

These distances are geographic proxies. They do not represent actual road distances, customer delivery distances, shipping duration, or transportation costs.

### 4.4 Machine Learning Experiment

A Random Forest regression model was evaluated for lead-time prediction and compared with a mean-value baseline.

The Random Forest achieved a mean absolute error (MAE) of approximately 225.90 days, a root mean squared error (RMSE) of approximately 278.26 days, and an R² score of approximately -0.0949. The baseline achieved an MAE of approximately 215.20 days and an RMSE of approximately 265.97 days.

Because the Random Forest performed worse than the baseline, the current experiment does not demonstrate reliable predictive improvement. The model should not be treated as a validated shipping-time prediction solution.

### 4.5 Recommendation Dashboard

The Streamlit dashboard provides four main sections:

- **Overview:** Summarizes dataset-level metrics and division performance.
- **Factory Performance:** Compares historical factory sales, profit, units, orders, and margins.
- **Factory Optimization:** Allows product selection and compares alternative factory assignments.
- **Data Quality:** Displays missing-value information, unmapped records, and lead-time statistics.

The dashboard supports two recommendation priorities:

- **Speed:** Ranks alternative factories using straight-line distance between factory locations.
- **Profit:** Uses historical factory gross-profit performance to rank alternatives.

The profit priority is not a calculation of the selected product's expected profit after reassignment. It is a preliminary ranking based on historical factory performance.

## 5. Key Findings

### 5.1 Division Performance

The analyzed dataset produced the following division-level results:

| Division | Sales | Cost | Gross Profit | Gross Margin |
|---|---:|---:|---:|---:|
| Chocolate | 131,692.90 | 42,868.28 | 88,824.62 | 67.45% |
| Other | 9,663.25 | 5,329.80 | 4,333.45 | 44.84% |
| Sugar | 427.48 | 142.75 | 284.73 | 66.61% |

Chocolate accounted for the largest sales and gross profit in the analyzed dataset.

### 5.2 Factory Performance

The analyzed factory-level results include:

| Factory | Sales | Gross Profit | Gross Margin |
|---|---:|---:|---:|
| Lot's O' Nuts | 76,340.15 | 52,771.05 | 69.13% |
| Wicked Choccy's | 55,352.75 | 36,053.57 | 65.13% |
| Secret Factory | 8,587.50 | 4,344.70 | 50.59% |
| Sugar Shock | 208.98 | 116.43 | 55.71% |
| The Other Factory | 1,205.75 | 92.75 | 7.69% |

These figures describe historical performance within the analyzed dataset. They do not establish that moving products between factories would reproduce the same financial results.

### 5.3 Shipping-Date Data Quality

Order dates range from January 2, 2024, to December 31, 2025, while shipping dates range from June 30, 2026, to June 28, 2030.

Calculated lead times range from 904 to 1,642 days, with a mean of approximately 1,320.84 days and a median of approximately 1,274 days. These unusually long intervals raise a significant data-quality concern. The date fields and their meanings should be verified before interpreting these intervals as actual shipping durations.

## 6. Limitations

The current project has several limitations:

1. The available data does not provide sufficient evidence to estimate actual delivery-time savings from factory reassignment.
2. Customer-level delivery coordinates, road-network distances, transportation rates, factory capacities, and incremental production costs are not available in the analyzed dataset.
3. The Random Forest model did not outperform the mean baseline.
4. Seven records remained unmapped to a factory.
5. Historical factory profitability does not equal the expected profitability of assigning a particular product to another factory.
6. The distance-based ranking is a preliminary screening method, not a complete logistics optimization model.

## 7. Future Scope

Future improvements could include validating the date fields, obtaining customer delivery locations and road-distance estimates, collecting factory capacity and production-cost information, incorporating shipping rates, and developing a cost-aware optimization model. The predictive model could also be revisited after data-quality issues are resolved and more suitable features are available.

## 8. Conclusion

The project combines exploratory data analysis, historical factory performance comparisons, geographic distance calculations, a machine learning experiment, and an interactive Streamlit dashboard. It provides a practical starting point for investigating factory reallocation opportunities and identifying data-quality issues.

The results support further analysis rather than immediate factory reassignment. Actual operational decisions should be made only after validating the source data and evaluating transportation costs, production capacity, customer locations, and expected product-level profitability.

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Jupyter Notebook
- Streamlit

## Project Repository

https://github.com/VikasGorule/Nassau-Candy-Factory-Optimization
