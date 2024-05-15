import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('2d_test.csv')
df_population_grouped = df.groupby(['Algorithm', 'Population Size']).mean().reset_index()

df_generations_grouped = df.groupby(['Algorithm', 'Generations']).mean().reset_index()

plt.figure(figsize=(12, 6))
for algorithm in df_population_grouped['Algorithm'].unique():
    subset = df_population_grouped[df_population_grouped['Algorithm'] == algorithm]
    plt.plot(subset['Population Size'], subset['Time'], marker='o', linestyle='--', label=f'{algorithm}')
plt.title('Czas trwania ewolucji modelu 2D w zależności od rozmiaru populacji')
plt.xlabel('Rozmiar populacji')
plt.ylabel('Czas [s]')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
for algorithm in df_generations_grouped['Algorithm'].unique():
    subset = df_generations_grouped[df_generations_grouped['Algorithm'] == algorithm]
    plt.plot(subset['Generations'], subset['Time'], marker='o', linestyle='--', label=f'{algorithm}')
plt.title('Czas trwania ewolucji modelu 2D w zależności od liczby generacji')
plt.xlabel('Liczba generacji')
plt.ylabel('Czas [s]')
plt.legend()
plt.grid(True)
plt.show()
