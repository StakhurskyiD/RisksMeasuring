import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_weekly_returns(file_path):
    data = pd.read_excel(file_path)
    if data['S&P 500'].dtype == 'object':
        data['S&P 500'] = data['S&P 500'].str.replace(',', '').astype(float)
    weekly_returns = data.iloc[:, 1:].pct_change().dropna()
    return weekly_returns


def calculate_volatility_metrics(returns):
    metrics = pd.DataFrame()
    metrics['Mean'] = returns.mean()
    metrics['Std'] = returns.std()
    metrics['Skew'] = returns.skew()
    metrics['Kurtosis'] = returns.kurtosis()
    return metrics


def plot_mean_std_diagram(metrics):
    plt.figure(figsize=(10, 6))
    for i in metrics.index:
        plt.scatter(metrics.loc[i, 'Std'], metrics.loc[i, 'Mean'], label=i)
    plt.title('Mean vs. Standard Deviation')
    plt.xlabel('Standard Deviation (Risk)')
    plt.ylabel('Mean Return')
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_var_cvar(returns, alpha=0.1):
    var_cvar = pd.DataFrame(index=returns.columns, columns=['VaR', 'CVaR'])
    for col in returns.columns:
        var_cvar.loc[col, 'VaR'] = norm.ppf(alpha, returns[col].mean(), returns[col].std())
        below_var = returns[returns[col] <= var_cvar.loc[col, 'VaR']][col]
        var_cvar.loc[col, 'CVaR'] = below_var.mean() if not below_var.empty else np.nan
    return var_cvar

def calculate_beta_coefficients(returns, market_col='S&P 500'):
    cov_matrix = returns.cov()
    market_var = returns[market_col].var()
    betas = cov_matrix[market_col] / market_var
    return betas.drop(market_col)

# Setup all rows view for pandas
pd.set_option('display.max_rows', None)

# Excel file path
file_path = '../data/stoks.xlsx'

# Calculating Weekly Returns
weekly_returns = calculate_weekly_returns(file_path)

volatility_metrics = calculate_volatility_metrics(weekly_returns)

# Building diagram
plot_mean_std_diagram(volatility_metrics)

var_cvar = calculate_var_cvar(weekly_returns)

betas = calculate_beta_coefficients(weekly_returns)

export_file_path = '../data/weekly_returns.xlsx'

weekly_returns.to_excel(export_file_path, index=True)

print(f'Results exported to {export_file_path}')
# Вивід аналізу варіативності, VaR, CVaR та бета-коефіцієнтів
print("Volatility Metrics:\n", volatility_metrics)
print("\nVaR and CVaR:\n", var_cvar)
print("\nBeta Coefficients:\n", betas)
