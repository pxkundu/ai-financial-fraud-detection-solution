# Feature Engineering Test Output

## Test Results
```

=== Testing Feature Engineering ===
Generated 1000 test transactions
Number of unique customers: 99
Number of unique merchants: 49
Fraud rate: 10.40%

Processed features shape: (1000, 21)

=== Feature Validation ===
WARNING: Missing values found:
time_since_last_tx    99
dtype: int64
✓ No infinite values found
✓ No negative amounts found

Top 5 features correlated with fraud:
customer_risk_score    0.349778
merchant_risk_score    0.190831
time_since_last_tx     0.100273
amount_log             0.060882
amount_zscore          0.044895
Name: is_fraud, dtype: float64

=== Feature Distributions ===

=== Detailed Statistics ===

Amount Statistics:
            amount   amount_log  amount_zscore
count  1000.000000  1000.000000   1.000000e+03
mean     89.250324     4.027851   6.572520e-17
std     111.907198     0.963349   1.000000e+00
min       3.039609     1.396148  -7.703769e-01
25%      27.441741     3.347858  -5.523200e-01
50%      55.865685     4.040667  -2.983243e-01
75%     105.009780     4.663530   1.408261e-01
max    1058.925879     6.965954   8.664997e+00

Time-based Statistics:
              hour  day_of_week   is_weekend
count  1000.000000  1000.000000  1000.000000
mean     11.524000     3.016000     0.288000
std       6.945046     2.000937     0.453058
min       0.000000     0.000000     0.000000
25%       5.000000     1.000000     0.000000
50%      12.000000     3.000000     0.000000
75%      18.000000     5.000000     1.000000
max      23.000000     6.000000     1.000000

Behavioral Statistics:
       merchant_risk_score  customer_risk_score  location_change  device_change
count          1000.000000          1000.000000       1000.00000    1000.000000
mean              0.104000             0.104000          0.95400       0.880000
std               0.058282             0.106827          0.20959       0.325124
min               0.000000             0.000000          0.00000       0.000000
25%               0.058824             0.000000          1.00000       1.000000
50%               0.100000             0.083333          1.00000       1.000000
75%               0.136364             0.150000          1.00000       1.000000
max               0.266667             0.666667          1.00000       1.000000

Aggregate features shape: (99, 10)

Customer-level Statistics:
       amount_mean  amount_std  amount_min  ...  location_change_sum  device_change_sum  is_fraud_mean
count    99.000000   99.000000   99.000000  ...            99.000000          99.000000      99.000000
mean     88.401804   92.551340   13.610814  ...             9.636364           8.888889       0.110756
std      31.784757   60.304129    7.742036  ...             3.366869           2.989399       0.122220
min      33.816209   21.438734    3.039609  ...             3.000000           3.000000       0.000000
25%      66.428293   50.630735    8.063884  ...             7.000000           7.000000       0.000000
50%      82.093263   74.694203   11.708716  ...             9.000000           9.000000       0.083333
75%     106.042447  106.044281   17.700552  ...            12.000000          11.000000       0.174242
max     198.374244  297.537311   46.462040  ...            19.000000          19.000000       0.666667

[8 rows x 9 columns]

Test completed successfully!

Plots have been saved to: /home/artha_undu/aws-repo/ai-financial-fraud-detection-solution/dataiku/plots

```

## Generated Plots
The following plots were generated during the test:
1. `amount_distribution.png` - Transaction amount distribution by fraud status
2. `time_features.png` - Time-based feature distributions
3. `risk_scores.png` - Risk score distributions
4. `customer_statistics.png` - Customer-level statistics

## Test Summary
- Number of transactions processed: 1000
- Number of unique customers: 99
- Number of features generated: 21
- Number of aggregate features: 10
- Fraud rate in test data: 10.40%

## Feature Statistics
### Amount Features
|       |     amount |   amount_log |   amount_zscore |
|:------|-----------:|-------------:|----------------:|
| count | 1000       |  1000        |  1000           |
| mean  |   89.2503  |     4.02785  |     6.57252e-17 |
| std   |  111.907   |     0.963349 |     1           |
| min   |    3.03961 |     1.39615  |    -0.770377    |
| 25%   |   27.4417  |     3.34786  |    -0.55232     |
| 50%   |   55.8657  |     4.04067  |    -0.298324    |
| 75%   |  105.01    |     4.66353  |     0.140826    |
| max   | 1058.93    |     6.96595  |     8.665       |

### Time Features
|       |       hour |   day_of_week |   is_weekend |
|:------|-----------:|--------------:|-------------:|
| count | 1000       |    1000       |  1000        |
| mean  |   11.524   |       3.016   |     0.288    |
| std   |    6.94505 |       2.00094 |     0.453058 |
| min   |    0       |       0       |     0        |
| 25%   |    5       |       1       |     0        |
| 50%   |   12       |       3       |     0        |
| 75%   |   18       |       5       |     1        |
| max   |   23       |       6       |     1        |

### Behavioral Features
|       |   merchant_risk_score |   customer_risk_score |   location_change |   device_change |
|:------|----------------------:|----------------------:|------------------:|----------------:|
| count |          1000         |          1000         |        1000       |     1000        |
| mean  |             0.104     |             0.104     |           0.954   |        0.88     |
| std   |             0.0582823 |             0.106827  |           0.20959 |        0.325124 |
| min   |             0         |             0         |           0       |        0        |
| 25%   |             0.0588235 |             0         |           1       |        1        |
| 50%   |             0.1       |             0.0833333 |           1       |        1        |
| 75%   |             0.136364  |             0.15      |           1       |        1        |
| max   |             0.266667  |             0.666667  |           1       |        1        |

### Customer-Level Aggregates
|       |   amount_mean |   amount_std |   amount_min |   amount_max |   amount_sum |   transaction_count_24h_mean |   location_change_sum |   device_change_sum |   is_fraud_mean |
|:------|--------------:|-------------:|-------------:|-------------:|-------------:|-----------------------------:|----------------------:|--------------------:|----------------:|
| count |       99      |      99      |     99       |      99      |       99     |                     99       |              99       |            99       |      99         |
| mean  |       88.4018 |      92.5513 |     13.6108  |     303.328  |      901.518 |                      5.55051 |               9.63636 |             8.88889 |       0.110756  |
| std   |       31.7848 |      60.3041 |      7.74204 |     209.732  |      459.384 |                      1.68501 |               3.36687 |             2.9894  |       0.12222   |
| min   |       33.8162 |      21.4387 |      3.03961 |      60.1255 |      135.265 |                      2       |               3       |             3       |       0         |
| 25%   |       66.4283 |      50.6307 |      8.06388 |     165.349  |      594.125 |                      4.5     |               7       |             7       |       0         |
| 50%   |       82.0933 |      74.6942 |     11.7087  |     233.881  |      790.039 |                      5.5     |               9       |             9       |       0.0833333 |
| 75%   |      106.042  |     106.044  |     17.7006  |     348.625  |     1113.11  |                      6.5     |              12       |            11       |       0.174242  |
| max   |      198.374  |     297.537  |     46.462   |    1058.93   |     2602.44  |                     10.5     |              19       |            19       |       0.666667  |
