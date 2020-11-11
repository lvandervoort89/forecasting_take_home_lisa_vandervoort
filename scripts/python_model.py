'''
This scripts loads the gas data, splits the data into training and test sets, fits a
Facebook Prophet model, and returns the average MAE and RMSE of the training and test
sets over the forecasted period.
'''
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics

def is_great_recession(ds):
    '''
    A helper function that takes in a date and returns a value of 0 or 1 if the
    date is during the Great Recession (December 2007-June 2009).

    Parameters
    ----------
    date : The monthly gas average.

    Returns
    -------
    False if the month did not take place during the Great Recession and True if it did.
    '''
    day_to_check = pd.to_datetime(ds)
    if datetime(year=2007, month=12, day=1) <= day_to_check <= datetime(year=2009, month=6, day=1):
        return 1
    return 0

def rename_and_train_test_split(dataframe):
    '''
    Takes in the gas dataframe and renames the columns from gas_price to y and month_and_year
    to ds, as is required by Prophet modeling.  Then separates the data into a train and
    test set.  The test set is composed of the data from 2016-2018 and the train set is
    the data from 1992-2015.

    Parameters
    ----------
    df : A dataframe containing monthly average gasoline prices from January 1992-January 2018.

    Returns
    -------
    train_data : A dataframe containing data from 1992-2015
    test_data : A dataframe containing data from 2016-2018
    '''
    # Rename the columns to match what is needed for Prophet modeling
    dataframe = dataframe.rename(columns={'gas_price': 'y', 'month_and_year': 'ds'})

    # Add great_recession additional regressor column
    dataframe['great_recession'] = dataframe['ds'].apply(is_great_recession)

    # Indicate the start and end date of the test dataset
    start_date = pd.Timestamp(2016, 1, 1)
    last_date = pd.Timestamp(2018, 1, 1)

    # Separate train and test data
    train_data = dataframe[(dataframe.ds < start_date)]
    test_data = dataframe[(dataframe.ds >= start_date) & (dataframe.ds <= last_date)]

    return train_data, test_data

def final_prophet_model(train_data, test_data):
    '''
    A function that takes in the train and test data, fits a model to the train data,
    and returns the average MAE and RMSE for the train and test sets to provide information
    about the model performance.

    Parameters
    ----------
    train_data : A dataframe containing data from 1992-2015
    test_data : A dataframe containing data from 2016-2018

    Returns
    -------
    A print statement containing the MAE and RMSE for the train and test set across
    the horizon period. 
    '''
    # Concatenate train and test data together for final forecast
    all_data = pd.concat([train_data, test_data], ignore_index=True)

    # Initiate model with optimized hypterparameters from analysis
    model = Prophet(yearly_seasonality=False,
                    changepoint_prior_scale=.1,
                    changepoint_range=0.85)

    # Add custom yearly seasonality
    model.add_seasonality(name='yearly', period=365.25, fourier_order=3,
                          prior_scale=20, mode='additive')

    # Add great recession seasonality
    model.add_seasonality(name='great_recession',
                          period=365.25,
                          fourier_order=4,
                          condition_name='great_recession')

    # Fit the model to the training data
    model.fit(train_data)

    # Generate the future dataframe for monthly predictions 2 years out
    future = model.make_future_dataframe(periods=24, freq='MS')

    # Add great recession column to future dataframe
    future['great_recession'] = future['ds'].apply(is_great_recession)

    # Forecast the future based on the model
    forecast = model.predict(all_data)

    # Plot the forecast
    fig1 = model.plot(forecast)

    # Utilize built in cross_validation in Prophet
    cv_results = cross_validation(model, initial='730 days', period='180 days', horizon='365 days')

    # Utilize built in performance_metrics in Prophet
    performance_results = performance_metrics(cv_results, metrics=['mae', 'rmse'])

    # Average MAE and RMSE on train set
    train_mae = np.mean(performance_results.mae)
    train_rmse = np.mean(performance_results.rmse)

    # Get actual versus predicted values
    y_actual = test_data.y
    y_predicted = forecast.iloc[288:, -1]

    # Assess on test data
    test_mae = np.mean(np.abs(y_predicted - y_actual))
    test_rmse = np.sqrt(mean_squared_error(y_actual, y_predicted))

    print('Results from train set are:\n'
          f'MAE mean for horizon: {train_mae},\n'
          f'RMSE mean for horizon: {train_rmse},\n'

          'Results from train set are:\n'
          f'MAE mean for horizon: {test_mae},\n'
          f'RMSE mean for horizon: {test_rmse},\n')
    return forecast, fig1

def main():
    '''
    Loads the gas dataset, separates the training and test data, and outputs a Facebook
    Prophet model.
    '''
    # Load in data
    dataframe = pd.read_csv('scripts/forecasting_take_home_data.csv',
                            index_col=False, usecols=[0, 1], parse_dates=[0])
    # Separate train and test data
    train_data, test_data = rename_and_train_test_split(dataframe)

    # Build final model
    final_prophet_model(train_data, test_data)

main()
