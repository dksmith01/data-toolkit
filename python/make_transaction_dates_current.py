import pandas as pd
from datetime import datetime, timedelta
import argparse


def adjust_dates(df, date_column, base_date=None):
    """
    Adjusts all dates in the dataframe by adding the number of days between
    the maximum date in the specified column and today.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the dates.
    - date_column (str): The name of the column containing date values.
    - base_date (datetime, optional): The date to compare against the max date. Defaults to today.

    Returns:
    - pd.DataFrame: A DataFrame with adjusted dates.
    """
    if base_date is None:
        base_date = datetime.today()
    else:
        base_date = pd.to_datetime(base_date)

    # Ensure the date column is in datetime format
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
    else:
        return pd.DataFrame()

    # Find the max date in the specified column
    max_date = df[date_column].max()

    # Calculate the difference in days from today
    if max_date.tz is None:
        delta_days = (base_date - max_date).days
    else:
        base_date = pd.to_datetime(base_date).tz_localize('UTC')
        delta_days = (base_date - max_date).days

    print('base_date', base_date, 'max_date', max_date)

    # Add the delta to all date columns in the DataFrame
    for col in df.select_dtypes(include=['datetime64']):
        df[col] = df[col] + timedelta(days=delta_days)

    return df



def adjust_transaction_dates(filename, date_col_name, base_date=None):
    relpath_filename = f'../data/{filename}'
    t = pd.read_csv(relpath_filename)
    if len(t) > 0:
        t_adjusted = adjust_dates(t, date_col_name, base_date)
    else:
        t_adjusted = pd.DataFrame()
    return t_adjusted


def write_adjusted_dates_to_file(input_filename, 
                                 output_filename, 
                                 date_col_name,
                                 base_date=None):
    relpath_output_filename = f'../data/{output_filename}'
    output_df = adjust_transaction_dates(input_filename, 
                                         date_col_name,
                                         base_date)
    if len(output_df) > 0:
        output_df.to_csv(relpath_output_filename, index=False)
    else:
        print(f'There was a problem reading {input_filename}. No overwriting done.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sets the end date of the datasets to a date you choose (or today)')
    parser.add_argument('--base_date', type=str, required=True, help='The last date of the datasets')
    
    args = parser.parse_args()     

    files = [    
            {'fn': 'SmileCo_transactions.csv', 'date_col_name': 'activity_date'},
            {'fn': 'ServBiz_transactions.csv', 'date_col_name': 'date'},
            {'fn': 'growco_transactions.csv', 'date_col_name': 'date'},
            {'fn': 'monthly_subscriptions.csv', 'date_col_name': 'activity_date'},
            {'fn': 'retailco_transactions.csv', 'date_col_name': 'activity_date'},
            {'fn': 'volatile_revenue.csv', 'date_col_name': 'activity_date'},
            {'fn': 'saas_transactions_with_customer_type_segments.csv', 'date_col_name': 'date'}
            ]

    for file in files:
        print('Overwriting', file['fn'], 'with this new date:', args.base_date)
        write_adjusted_dates_to_file(input_filename=file['fn'], 
                                    output_filename=file['fn'],
                                    date_col_name=file['date_col_name'],
                                    base_date=args.base_date
                                    )
    print('All done!')


