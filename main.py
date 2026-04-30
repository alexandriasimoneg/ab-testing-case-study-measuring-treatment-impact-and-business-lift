# Project: A/B Testing Case Study – Measuring Treatment Impact and Business Lift
# Author: Alexandria Green
# Description: End-to-end A/B testing analysis including statistical hypothesis testing,
# effect size calculation, confidence intervals, power analysis, bootstrapping,
# and data visualization to evaluate treatment performance and business impact.
# -------------------------------

# 1. Setup & Imports
# -------------------------------
import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns



# 2. Simulate A/B Test Data
# (May swap this with a real dataset later)
# -------------------------------
np.random.seed(42)

control = np.random.normal(loc=50, scale=10, size=1000)
treatment = np.random.normal(loc=55, scale=10, size=1000)

df = pd.DataFrame({
    "group": ["control"] * 1000 + ["treatment"] * 1000,
    "value": np.concatenate([control, treatment])
})

print("Preview of data:")
print(df.head())



# 3. Split into Groups
# -------------------------------
control_group = df[df["group"] == "control"]["value"]
treatment_group = df[df["group"] == "treatment"]["value"]



# 4. Statistical Testing (T-Test)
# -------------------------------
t_stat, p_value = stats.ttest_ind(control_group, treatment_group)

print("\n--- Statistical Test ---")
print("T-statistic:", t_stat)
print("P-value:", p_value)



# 5. Business Metrics
# -------------------------------
control_mean = control_group.mean()
treatment_mean = treatment_group.mean()

lift = (treatment_mean - control_mean) / control_mean

mean_diff = treatment_mean - control_mean
pooled_std = np.sqrt((control_group.std()**2 + treatment_group.std()**2) / 2)
cohens_d = mean_diff / pooled_std

print("\n--- Business Metrics ---")
print("Control Mean:", control_mean)
print("Treatment Mean:", treatment_mean)
print("Percent Lift:", lift * 100)
print("Cohen's d:", cohens_d)



# 6. Confidence Interval (95%)
# -------------------------------
n1, n2 = len(control_group), len(treatment_group)
se_diff = np.sqrt(control_group.var()/n1 + treatment_group.var()/n2)

ci_low = mean_diff - 1.96 * se_diff
ci_high = mean_diff + 1.96 * se_diff

print("\n--- Confidence Interval (95%) ---")
print(f"CI: [{ci_low:.2f}, {ci_high:.2f}]")

# Interpretation note: 
# #If CI does not include 0 → difference is statistically significant



# 7. Power Analysis (approximate)
# -------------------------------
# How likely we are to detect an effect of this size

effect_size = cohens_d
power = stats.norm.cdf(
    (np.sqrt(n1) * effect_size) - stats.norm.ppf(0.975)
)

print("\n--- Power Analysis ---")
print("Approximate Power:", power)

# Interpretation:
# > 0.8 = strong test
# < 0.8 = may be underpowered



# 8. Bootstrapping (Non-parametric)
# -------------------------------
# Resampling to estimate distribution of mean difference

boot_diffs = []
n_boot = 1000

for _ in range(n_boot):
    sample_control = np.random.choice(control_group, size=n1, replace=True)
    sample_treatment = np.random.choice(treatment_group, size=n2, replace=True)
    boot_diffs.append(sample_treatment.mean() - sample_control.mean())

boot_ci_low = np.percentile(boot_diffs, 2.5)
boot_ci_high = np.percentile(boot_diffs, 97.5)

print("\n--- Bootstrap Confidence Interval ---")
print(f"Bootstrap CI: [{boot_ci_low:.2f}, {boot_ci_high:.2f}]")

# Interpretation:
# More robust than t-test if distributions are non-normal



# 9. Visualization
# -------------------------------
plt.figure(figsize=(8,5))

sns.histplot(control_group, kde=True, label="Control", stat="density", alpha=0.5)
sns.histplot(treatment_group, kde=True, label="Treatment", stat="density", alpha=0.5)

plt.axvline(control_mean, linestyle='--', label='Control Mean')
plt.axvline(treatment_mean, linestyle='--', label='Treatment Mean')

plt.legend()

# Title with lift
plt.title(f"A/B Test Comparison (Lift: {lift*100:.2f}%)")

plt.xlabel("Metric Value")
plt.ylabel("Density")

plt.savefig("ab_testing_plot.png")

print("\nPlot saved as ab_testing_plot.png")