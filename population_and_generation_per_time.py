import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('3d_test.csv')

df_grouped = df.groupby(['Algorithm', 'Population Size', 'Generations']).mean().reset_index()

for algorithm in df_grouped['Algorithm'].unique():
    subset_algorithm = df_grouped[df_grouped['Algorithm'] == algorithm]
    plt.figure(figsize=(12, 8))

    for population_size in subset_algorithm['Population Size'].unique():
        subset_population = subset_algorithm[subset_algorithm['Population Size'] == population_size]
        plt.plot(subset_population['Generations'], subset_population['Time'], marker='o', linestyle='--',
                 label=f'Rozmiar populacji: {population_size}', linewidth=2, markersize=8)

    plt.title(f'{algorithm} - Średni czas trwania ewolucji modelu 3D w zależności od liczby generacji', fontsize=16)
    plt.xlabel('Liczba generacji', fontsize=14)
    plt.ylabel('Czas [s]', fontsize=14)
    plt.legend(fontsize=12)

    x_ticks = np.arange(start=subset_algorithm['Generations'].min(),
                        stop=subset_algorithm['Generations'].max() + 5, step=5)
    plt.xticks(x_ticks, fontsize=12)

    max_time_algorithm = subset_algorithm['Time'].max()
    y_ticks = np.arange(start=0, stop=max_time_algorithm + 50, step=50)
    plt.yticks(y_ticks, fontsize=12)

    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.show()
