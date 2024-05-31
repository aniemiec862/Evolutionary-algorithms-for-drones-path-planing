import pandas as pd

csv_file = 'test_3d_params.csv'

data = pd.read_csv(csv_file)

results = data.groupby('Algorithm').agg(['mean'])

columns_to_multiply = results.columns.levels[0].difference(['ENCOUNTERED_OBSTACLES'])

for col in columns_to_multiply:
    results[(col, 'mean')] *= 3

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

results.to_csv('grouped_results_3d.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

results.to_csv('grouped_results_3d.csv')
