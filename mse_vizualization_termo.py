import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


# --- Завантаження даних ---
# Файли CSV: населення та кордон
cities_file = 'ua_locations_wiki_cities_villages_settlements_clear.csv'  # Файл з населеними пунктами
border_file = 'Ukraine_coordinates_simplification_25.csv'  # Файл з кордоном України

# Завантаження даних про населені пункти
cities = pd.read_csv(cities_file)
cities = cities.dropna(subset=['lat', 'lng', 'founded'])

# Завантаження даних про кордон України
border = pd.read_csv(border_file)
border = border.dropna()


# --- Налаштування моделювання ---
# Розміри області (за координатами кордону)
Lx = border['Longitude'].max() - border['Longitude'].min()
Ly = border['Latitude'].max() - border['Latitude'].min()
Nx, Ny = 400, 400  # Кількість вузлів сітки
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)

# Створення сітки
x = np.linspace(border['Longitude'].min(), border['Longitude'].max(), Nx)
y = np.linspace(border['Latitude'].min(), border['Latitude'].max(), Ny)
X, Y = np.meshgrid(x, y)


# Початкові умови
T = np.zeros((Ny, Nx))

# --- Джерела (населені пункти) ---
# Ініціалізація вектора джерел
b = np.zeros((Ny, Nx))

# Встановлення джерел тепла (населені пункти)
current_year = 2023  # Поточний рік для обчислення віку міста
for i, (lat, lng, founded) in enumerate(zip(cities['lat'], cities['lng'], cities['founded'])):
    ix = np.argmin(np.abs(x - lng))
    iy = np.argmin(np.abs(y - lat))
    # Інтенсивність джерела пропорційна віку міста
    age = current_year - founded
    intensity = age if age > 0 else 1  # Уникаємо нульового або від'ємного віку
    b[iy, ix] += intensity


# --- Формування матриці A ---
from scipy.sparse import lil_matrix

k = 1.0  # Коефіцієнт теплопровідності
N = Nx * Ny  # Загальна кількість вузлів

A = lil_matrix((N, N))
b_flat = b.flatten()  # Перетворюємо вектор b в одномірний масив

for j in range(Ny):
    for i in range(Nx):
        n = j * Nx + i  # Індекс вузла

        # Перевірка, чи вузол знаходиться на кордоні
        if i == 0 or i == Nx - 1 or j == 0 or j == Ny -1:
            # Граничний вузол, температура задана (наприклад, T = 0)
            A[n, n] = 1.0
            b_flat[n] = 0.0
        else:
            # Внутрішній вузол, застосовуємо оператор Лапласа
            A[n, n] = -2 * (1.0 / dx**2 + 1.0 / dy**2)
            A[n, n - 1] = 1.0 / dx**2  # Лівий сусід
            A[n, n + 1] = 1.0 / dx**2  # Правий сусід
            A[n, n - Nx] = 1.0 / dy**2  # Нижній сусід
            A[n, n + Nx] = 1.0 / dy**2  # Верхній сусід
A = A.tocsr()

# --- Розв'язання системи ---
T_flat = spsolve(A, -b_flat / k)  # Ділимо на k згідно з рівнянням

# Перетворення результату в двовимірний масив
T = T_flat.reshape((Ny, Nx))


# --- Візуалізація ---
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.imshow(T, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='hot')
fig.colorbar(cax, label='Соціальний потенціал')

# Додавання лінії кордону
ax.plot(border['Longitude'], border['Latitude'], color='blue', linewidth=1, label='Кордон України')

ax.set_title('Розподіл соціального потенціалу')
ax.legend()

plt.xlabel('Довгота')
plt.ylabel('Широта')
plt.show()
