# Forecasting Take Home for Lisa VanderVoort  

## **Objective:**  
Analyze regular motor gasoline retail prices and use Facebook Prophet to find a model to fit the data for the US Foods Take Home assignment.

## **Approach:**
A detailed analysis of the data and modeling decisions can be found in forecasting_take_home_lisa_vandervoort.  Additionally, a Jupyter notebook with all scripts and comments on analysis and modeling can be found in forecasting_initial_analysis_and_modeling_lisa_vandervoort.ipynb.  Finally, a final model can be run using the script python_analysis.py.  

## **Featured Techniques:**
- Exploratory data analysis
- Time series forecasting
- Facebook Prophet
- Docker
- bash

## **Data:**
Data from regular motor gasoline retail prices from January 1992 to January 2018 was used. Data is located in the Notebooks folder.

## **Results Summary:**
Data from 2016-2018 was held out as a test set and data from 1992-2015 was used as training data. A Facebook Prophet model with INSERT hyperparameters and interesting things here was chosen. Detailed information regarding the decisions made during modeling can be found in forecasting_take_home_lisa_vandervoort.pdf.  When I evaluated this modeling on my training dataset, I obtained an average MAE of 0.357 and RMSE of 0.519 across the forecasted horizon.  Evaluating my model on my test dataset,  I obtained an average MAE of 0.353 and RMSE of 0.417.

## **How to Run the Code Through Docker:**
**To run forecasting_initial_analysis_and_modeling_lisa_vandervoort.ipynb:**
- Build the image:
```
bash driver.sh build
```
- Start Jupter notebook
```
bash driver.sh jupyter
```
- Go to http://localhost:8888/notebooks/notebooks/forecasting_initial_analysis_and_modeling_lisa_vandervoort.ipynb
- Stop the container when done
```
bash driver.sh stop
```

**To run python_model.py:**
- Build the image:
```
bash driver.sh build
```
- Run the scripts/python_model.py
```
bash driver.sh python-modeling
```
- Stop the container when done
```
bash driver.sh stop
```
