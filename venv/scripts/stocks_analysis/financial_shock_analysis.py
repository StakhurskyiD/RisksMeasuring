import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def preprocess_value(value):
    if isinstance(value, (int, float)):
        # If the value is already numeric, return it as is.
        return value
    elif isinstance(value, str):
        # If the value is a string, try to split and convert to float.
        try:
            # Attempt to convert the value to float if it's a string.
            # Here we assume that the first number before a comma is the correct value,
            # which may need adjustment if your data is different.
            return float(value.split(',')[0].replace(',', ''))
        except ValueError:
            # If conversion fails, return NaN to indicate an invalid value.
            return np.nan
    else:
        # If the value is neither numeric nor string (e.g., datetime), return NaN.
        return np.nan


def calculate_price_stats(combined_data, interval, index_name, stat_func):
    start, end = interval
    relevant_data = combined_data.loc[start:end, index_name]
    return stat_func(relevant_data)


def calculate_indicators(average_price_a, minimal_price_b, average_price_c):
    deepness_of_shock = (minimal_price_b - average_price_a) / average_price_a
    indicator_of_renovation = average_price_c / average_price_a
    return deepness_of_shock, indicator_of_renovation


def plot_results(combined_data, index_name, average_price_a, minimal_price_b, average_price_c):
    plt.figure(figsize=(10, 6))
    plt.plot(combined_data.index, combined_data[index_name], label=f'{index_name} Price')
    plt.axhline(y=average_price_a, color='g', linestyle='-', label='Avg Price A')
    plt.axhline(y=minimal_price_b, color='r', linestyle='--', label='Min Price B')
    plt.axhline(y=average_price_c, color='b', linestyle='-.', label='Avg Price C')
    plt.legend()
    plt.title(f'Financial Risk Analysis of {index_name}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()


def perform_analysis(file_path, indices, Xa, Xb, Xc):
    data = pd.read_excel(file_path, index_col=None)
    results = []

    for index_name in indices:
        date_column = 'Date'  # Adjust if necessary
        data[date_column] = pd.to_datetime(data[date_column])
        index_data = data[index_name].apply(preprocess_value)
        combined_data = pd.concat([data[date_column], index_data], axis=1).dropna()
        combined_data.set_index(date_column, inplace=True)
        combined_data.sort_index(inplace=True)

        average_price_a = calculate_price_stats(combined_data, Xa, index_name, np.mean)
        minimal_price_b = calculate_price_stats(combined_data, Xb, index_name, np.min)
        average_price_c = calculate_price_stats(combined_data, Xc, index_name, np.mean)

        deepness, renovation = calculate_indicators(average_price_a, minimal_price_b, average_price_c)

        plot_results(combined_data, index_name, average_price_a, minimal_price_b, average_price_c)

        results.append({
            'Index': index_name,
            'Deepness of Shock': deepness,
            'Indicator of Renovation': renovation
        })

    # Return results as a DataFrame for tabular display
    return pd.DataFrame(results)

# Inputs for intervals as tuples of ('YYYY-MM-DD', 'YYYY-MM-DD')
Xa = ('2019-12-01', '2020-01-15')
Xb = ('2020-01-16', '2020-05-01')
Xc = ('2020-05-01', '2020-06-15')

indices = ['DJI', 'SPX', 'GDAXI', 'FCHI', 'Nikkei', 'FTSE China', 'WIG20', 'BVSP', 'Nifty 50']
file_path = '/Users/dstakhurskyi/Downloads/HW1.xlsx'

try:
    results_df = perform_analysis(file_path, indices, Xa, Xb, Xc)
    print(results_df.to_string(index=False))
    results_df.to_csv('results_df.csv', header=True)
except Exception as e:
    print(f"An error occurred: {e}")
