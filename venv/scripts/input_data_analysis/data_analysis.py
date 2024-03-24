import pandas as pd


def calculate_weekly_close_prices(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Convert the 'Price' column to a float, removing commas
    data['Price'] = data['Price'].str.replace(',', '').astype(float)

    # Set the 'Date' column as the index
    data.set_index('Date', inplace=True)

    # Write the series to a CSV file

    # Resample the data to get weekly closing prices
    weekly_close_prices = data['Price'].resample('W').last()

    return weekly_close_prices


def calculate_daily_close_prices(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Convert the 'Price' column to a float, removing commas
    data['Price'] = data['Price'].str.replace(',', '').astype(float)

    # Set the 'Date' column as the index
    data.set_index('Date', inplace=True)

    # The daily closing prices are directly represented by the 'Price' column
    daily_close_prices = data['Price']

    return daily_close_prices


# Usage example:
file_path = '/Users/dstakhurskyi/Downloads/Bovespa Historical Data.csv'
# weekly_close_prices = calculate_weekly_close_prices(file_path)
# weekly_close_prices.to_csv('weekly_close_prices.csv', header=True)
#
# print(weekly_close_prices)


daily_close_prices = calculate_daily_close_prices(file_path)
daily_close_prices.to_csv('daily_close_prices.csv', header=True)

print(daily_close_prices)
