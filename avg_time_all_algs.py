import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('2d_test.csv')

df_grouped = df.groupby(['Algorithm', 'Population Size', 'Generations']).mean().reset_index()

df_filtered = df_grouped[df_grouped['Population Size'] == 100]

plt.figure(figsize=(12, 8))

for algorithm in df_filtered['Algorithm'].unique():
    subset_algorithm = df_filtered[df_filtered['Algorithm'] == algorithm]
    plt.plot(subset_algorithm['Generations'], subset_algorithm['Time'], marker='o', linestyle='--',
             label=f'Algorytm: {algorithm}', linewidth=2, markersize=8)

plt.title('Średni czas trwania ewolucji modelu 3D w zależności od liczby generacji dla populacji 100', fontsize=16)
plt.xlabel('Liczba generacji', fontsize=14)
plt.ylabel('Czas [s]', fontsize=14)
plt.legend(fontsize=12)

x_ticks = np.arange(start=df_filtered['Generations'].min(), stop=df_filtered['Generations'].max() + 5, step=5)
plt.xticks(x_ticks, fontsize=12)

max_time = df_filtered['Time'].max()
y_ticks = np.arange(start=0, stop=max_time + 5, step=5)
plt.yticks(y_ticks, fontsize=12)

plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
plt.show()
