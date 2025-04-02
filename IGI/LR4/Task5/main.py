"""
Developer: Mahiliavets Dzianis
Lab: 2
Task: NumPy Array Operations
Version: 1.0
Date: 2025-03-16

"""

import numpy as np

# 1. Создание целочисленной матрицы A[n, m]
n = 4  # строки
m = 5  # столбцы
A = np.random.randint(0, 100, size=(n, m))
print("Исходная матрица:\n", A)

# 2. Функции создания массивов
zeros_array = np.zeros((2, 3))  # Массив нулей
ones_array = np.ones((3, 2))    # Массив единиц
diag_array = np.eye(3)          # Единичная матрица 3x3
print("\nНулевой массив:\n", zeros_array)
print("Массив единиц:\n", ones_array)
print("Единичная матрица:\n", diag_array)

# 3. Индексирование и срезы
first_row = A[0]               # Первая строка
last_col = A[:, -1]            # Последний столбец
sub_matrix = A[1:3, 1:4]       # Подматрица
print("\nПервая строка:", first_row)
print("Последний столбец:", last_col)
print("Подматрица:\n", sub_matrix)

# 4. Поэлементные операции
A_squared = A ** 2             # Квадрат каждого элемента
A_plus_10 = A + 10             # Увеличение на 10
print("\nМатрица в квадрате:\n", A_squared)
print("Матрица +10:\n", A_plus_10)

# 5. Статистические операции
mean_val = np.mean(A)          # Среднее арифметическое
median_val = np.median(A)      # Медиана
corr_matrix = np.corrcoef(A)   # Матрица корреляций
variance = np.var(A)           # Дисперсия
std_dev = np.std(A)            # Стандартное отклонение

print("\nСреднее значение:", mean_val)
print("Медиана:", median_val)
print("Матрица корреляций:\n", corr_matrix)
print("Дисперсия:", variance)
print("Стандартное отклонение:", std_dev)

# 6. Элементы, превосходящие среднее
above_mean = A[A > mean_val]
count_above_mean = len(above_mean)
print("\nКоличество элементов выше среднего:", count_above_mean)

# 7. Стандартное отклонение двумя способами
# Способ 1: Встроенная функция
std_method1 = np.std(above_mean)

# Способ 2: Ручной расчет
mean_above = np.mean(above_mean)
squared_diff = (above_mean - mean_above) ** 2
std_method2 = np.sqrt(np.mean(squared_diff))

# Округление
std_method1_rounded = round(std_method1, 2)
std_method2_rounded = round(std_method2, 2)

print("\nСтандартное отклонение (метод 1):", std_method1_rounded)
print("Стандартное отклонение (метод 2):", std_method2_rounded)