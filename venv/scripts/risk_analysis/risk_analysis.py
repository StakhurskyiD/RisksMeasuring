import numpy as np
import pandas as pd

# Initialize constants and utility functions
PRIZES = np.array([1426000, 28791, 353, 25])
PROBABILITIES = np.array([0.000082, 0.000164, 0.006410, 0.083333])
COST_OF_TICKET = 20

def utility_risk_averse(x):
    return np.log(x + 1)

def utility_risk_loving(x):
    return (x + 1) ** 0.5

# Perform calculations
expected_win = np.sum(PRIZES * PROBABILITIES)
variance = np.sum(PROBABILITIES * (PRIZES - expected_win) ** 2)
std_deviation = np.sqrt(variance)
coefficient_of_variation = std_deviation / expected_win
expected_utility_averse = np.sum(PROBABILITIES * utility_risk_averse(PRIZES))
expected_utility_loving = np.sum(PROBABILITIES * utility_risk_loving(PRIZES))
ce_averse = np.exp(expected_utility_averse) - 1
ce_loving = (expected_utility_loving ** 2) - 1
rp_averse = ce_averse - COST_OF_TICKET
rp_loving = ce_loving - COST_OF_TICKET

# Prepare DataFrame for display
results_df = pd.DataFrame({
    "Parameter": [
        "Expected Win", "Variance", "Standard Deviation", "Coefficient of Variation",
        "Risk-Averse: Expected Utility", "Risk-Averse: CE", "Risk-Averse: RP",
        "Risk-Loving: Expected Utility", "Risk-Loving: CE", "Risk-Loving: RP"
    ],
    "Value": [
        f"{expected_win:.2f} UAH", f"{variance:.2f}", f"{std_deviation:.2f}", f"{coefficient_of_variation:.2f}",
        f"{expected_utility_averse:.2f}", f"{ce_averse:.2f} UAH", f"{rp_averse:.2f} UAH",
        f"{expected_utility_loving:.2f}", f"{ce_loving:.2f} UAH", f"{rp_loving:.2f} UAH"
    ],
    "Description": [
        "The average amount of money won based on the probabilities and prize amounts.",
        "The measure of the spread of prize amounts.",
        "The square root of variance, indicating the deviation from the expected win.",
        "A normalized measure of the dispersion of the prize distribution.",
        "", "", "",
        "", "", ""
    ]
})

# Enhance display settings
pd.set_option("display.max_colwidth", None)
pd.set_option("display.precision", 2)
pd.set_option('display.expand_frame_repr', False)

# Display the results with clear separation
print("Detailed Results Table with Clear Separation for Risk Preferences:")
print(results_df)
