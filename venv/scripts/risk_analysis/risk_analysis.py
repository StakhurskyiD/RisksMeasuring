import pandas as pd
import numpy as np

# Load the dataset
data_loto = pd.read_csv('/Users/dstakhurskyi/Downloads/LotoData.csv')

# Calculate average prize amounts for each category
average_prize_5_5 = data_loto['prize in the category 5х5'].mean()
average_prize_4_5 = data_loto['prize in the category 4х5'].mean()
average_prize_3_5 = data_loto['prize in the category 3х5'].mean()
average_prize_2_5 = data_loto['prize in the category 2х5'].mean()

# Updated prizes based on the average prize amounts
prizes_updated = np.array([average_prize_2_5, average_prize_3_5, average_prize_4_5, average_prize_5_5])

# Updated probabilities based on the provided odds
probabilities_updated = np.array([1/12, 1/156, 1/6108, 1/1221759])

# Assume the cost of a ticket remains the same
COST_OF_TICKET = 20

# Utility functions remain unchanged
def utility_risk_averse(x):
    return np.log(x + 1)

def utility_risk_loving(x):
    return (x + 1) ** 0.5

# Perform calculations with updated prizes and probabilities
expected_win_updated = np.sum(prizes_updated * probabilities_updated)
variance_updated = np.sum(probabilities_updated * (prizes_updated - expected_win_updated) ** 2)
std_deviation_updated = np.sqrt(variance_updated)
coefficient_of_variation_updated = std_deviation_updated / expected_win_updated
expected_utility_averse = np.sum(probabilities_updated * utility_risk_averse(prizes_updated - COST_OF_TICKET))
expected_utility_loving = np.sum(probabilities_updated * utility_risk_loving(prizes_updated - COST_OF_TICKET))
ce_averse_updated = np.exp(expected_utility_averse) - 1
ce_loving_updated = (expected_utility_loving ** 2) - 1
rp_averse_updated = ce_averse_updated - COST_OF_TICKET
rp_loving_updated = ce_loving_updated - COST_OF_TICKET

# Prepare DataFrame for display with updated results
results_df_updated = pd.DataFrame({
    "Parameter": [
        "Expected Win", "Variance", "Standard Deviation", "Coefficient of Variation",
        "Risk-Averse: Expected Utility", "Risk-Averse: CE", "Risk-Averse: RP",
        "Risk-Loving: Expected Utility", "Risk-Loving: CE", "Risk-Loving: RP"
    ],
    "Value": [
        f"{expected_win_updated:.2f} UAH", f"{variance_updated:.2f}", f"{std_deviation_updated:.2f}", f"{coefficient_of_variation_updated:.2f}",
        f"{expected_utility_averse:.2f}", f"{ce_averse_updated:.2f} UAH", f"{rp_averse_updated:.2f} UAH",
        f"{expected_utility_loving:.2f}", f"{ce_loving_updated:.2f} UAH", f"{rp_loving_updated:.2f} UAH"
    ],
    "Description": [
        "The average amount of money won based on the updated probabilities and prize amounts.",
        "The measure of the spread of prize amounts using updated data.",
        "The square root of variance, indicating the deviation from the expected win with updated probabilities.",
        "A normalized measure of the dispersion of the prize distribution using updated data.",
        "", "", "",
        "", "", ""
    ]
})

# Enhance display settings
pd.set_option("display.max_colwidth", None)
pd.set_option("display.precision", 2)
pd.set_option('display.expand_frame_repr', False)

# Display the results with clear separation for risk preferences
print("Detailed Results Table with Clear Separation for Risk Preferences (Updated):")
print(results_df_updated)

filename = 'lottery_analysis_results.csv'
results_df_updated.to_csv(filename, index=False)

print(f"Results have been successfully exported to {filename}.")
