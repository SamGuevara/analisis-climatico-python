import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Verificación de archivo, por medio del modulo os verifico la ruta del archivo
clima = 'Registro_Temperatura_Argentina.csv'

if os.path.exists(clima):
    print(f"Archivo {clima} encontrado.")
else:
    print(f"Archivo {clima} no encontrado.")
    print("Verifique la ruta del archivo.")

print("\n" + "-"*60)
print("Carga del Archivo y Exploración Básica")

# Carga del Archivo y Exploración Básica
df_climaargentina = pd.read_csv(clima)
print("\nDataframe cargado con exito.")
print("."*30)

# Exploración básica
print(f"\nColumnas del DataFrame: ", df_climaargentina.columns.tolist())
print(f"\nLas primera 10 filas del DataFrame:\n", df_climaargentina.head(10))
print(f"\nLas ultimas 10 filas del DataFrame:\n", df_climaargentina.tail(10))
print(f"\nForma del DataFrame (filas, columnas):\n {df_climaargentina.shape}")

# Filtro por Ubicación (columna 'Nombre')
print("\nCantidad de registros por ubicación: ")
registro_por_ubicacion = df_climaargentina['NOMBRE'].value_counts()
print(registro_por_ubicacion)

# Convertir fecha a datetime y creación de columnas derivadas
df_climaargentina['FECHA'] = pd.to_datetime(df_climaargentina['FECHA'], errors='coerce')
print("\nConversion de la columna fecha a datetime para el analisis.")

# Creación de columnas derivadas
df_climaargentina['MES'] = df_climaargentina['FECHA'].dt.month
df_climaargentina['DIA_AÑO'] = df_climaargentina['FECHA'].dt.dayofyear
df_climaargentina['AÑO'] = df_climaargentina['FECHA'].dt.year
print("\nCreación de columnas derivadas: MES, DIA_AÑO, AÑO")

# Definición de nombres de meses
nombres_meses = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', 
                7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}

# Promedio temperatura maxima y minima mensual
df_mensual = df_climaargentina.groupby('MES')[['TMAX','TMIN']].mean()

# Promedio de temperaturas
promedio_temperaturas = (df_mensual['TMAX'] + df_mensual['TMIN']) / 2
promedio_temperaturas.index = promedio_temperaturas.index.map(nombres_meses)
print(f"\nLa temperatura promedio por mes es:\n{promedio_temperaturas}")

# Rango de temperatura
rango_termico = df_mensual['TMAX'] - df_mensual['TMIN']
rango_termico.index = rango_termico.index.map(nombres_meses)
print(f"\nEl rango termico en Argentina es:\n{rango_termico}")

# Temperaturas extremas
muy_caluroso = df_climaargentina[df_climaargentina['TMAX'] > 35]
print(f"\nLos dias mas calurosos son: \n{muy_caluroso}")

muy_frio = df_climaargentina[df_climaargentina['TMIN'] < 0]
print(f"\nLos dias mas frios son: \n{muy_frio}")

# Determinar mes mas caluroso y mes mas frio
print("\nAnalisis de meses extremos")

mes_mas_caluroso_num = df_mensual['TMAX'].idxmax()
mes_mas_caluroso_nombre = nombres_meses[mes_mas_caluroso_num]
temperatura_maxima_promedio = df_mensual['TMAX'].max()
print(f"\nEl mes mas caluroso es {mes_mas_caluroso_nombre} con una temperatura maxima promedio de {temperatura_maxima_promedio:.2f}°C")

mes_mas_frio_num = df_mensual['TMIN'].idxmin()
mes_mas_frio_nombre = nombres_meses[mes_mas_frio_num]
temperatura_minima_promedio = df_mensual['TMIN'].min()
print(f"\nEl mes mas frio es {mes_mas_frio_nombre} con una temperatura minima promedio de {temperatura_minima_promedio:.2f}°C")

# Graficos Diarios y Mensual

#Grafico diario
# 1. Preparar datos para el gráfico diario
# Filtrar y limpiar datos
df_limpio = df_climaargentina.dropna(subset=['FECHA', 'TMAX', 'TMIN'])
df_limpio = df_limpio[(df_limpio['FECHA'] >= '2024-08-11') & (df_limpio['FECHA'] <= '2025-08-11')]
df_limpio = df_limpio.sort_values('FECHA')

# Agrupar por fecha para obtener promedios diarios (ya que hay múltiples estaciones)
df_diario = df_limpio.groupby('FECHA')[['TMAX', 'TMIN']].mean().reset_index()

print(f"\nDatos para gráfico diario: {len(df_diario)} días")
print(f"Fecha inicio: {df_diario['FECHA'].min()}")
print(f"Fecha fin: {df_diario['FECHA'].max()}")

# Gráfico Evolución diaria de temperaturas
plt.figure(figsize=(12, 5))
plt.plot(df_diario['FECHA'], df_diario['TMAX'], label='Temperatura Máxima (°C)', color='red', linewidth=1)
plt.plot(df_diario['FECHA'], df_diario['TMIN'], label='Temperatura Mínima (°C)', color='blue', linewidth=1)
plt.title("Evolución Diaria de Temperaturas en Argentina (Ago 2024 - Ago 2025)", fontsize=12)
plt.xlabel("Fecha", fontsize=10)
plt.ylabel("Temperatura (°C)", fontsize=10)
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Grafico Mensual
# 2. Preparar datos para el gráfico mensual
# Crear una columna de año-mes para agrupar correctamente
df_limpio['AÑO_MES'] = df_limpio['FECHA'].dt.to_period('M')

# Agrupar por año-mes
df_mensual_cronologico = df_limpio.groupby('AÑO_MES')[['TMAX', 'TMIN']].mean().reset_index()

# Crear etiquetas más legibles para los meses
df_mensual_cronologico['ETIQUETA_MES'] = df_mensual_cronologico['AÑO_MES'].astype(str)

print(f"\nDatos para gráfico mensual: {len(df_mensual_cronologico)} meses")
print("Meses disponibles:")
print(df_mensual_cronologico['ETIQUETA_MES'].tolist())

# Gráfico 2: Promedio mensual de temperaturas
plt.figure(figsize=(12, 5))
x_pos = range(len(df_mensual_cronologico))
plt.plot(x_pos, df_mensual_cronologico['TMAX'], marker='o', color='red', label='TMAX Promedio', linewidth=2, markersize=6)
plt.plot(x_pos, df_mensual_cronologico['TMIN'], marker='o', color='blue', label='TMIN Promedio', linewidth=2, markersize=6)
plt.title('Temperatura Promedio Mensual en Argentina (Ago 2024 - Ago 2025)', fontsize=12)
plt.xlabel('Mes', fontsize=10)
plt.ylabel('Temperatura (°C)', fontsize=10)
plt.xticks(x_pos, df_mensual_cronologico['ETIQUETA_MES'], rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Extras 
# Comparación de Estaciones Meteorológicas
print("\nEstaciones meteorológicas con mas registros")
estaciones_disponibles = df_climaargentina['NOMBRE'].value_counts().head(100)
print(estaciones_disponibles)
estacion_1 = estaciones_disponibles.index[0]
estacion_2 = estaciones_disponibles.index[1]
print(f"\nComparando: {estacion_1} vs {estacion_2}")
# Preparando datos Estación 1 para comparar
df_estacion_1 = df_climaargentina[df_climaargentina['NOMBRE'] == estacion_1].copy()
df_estacion_1 = df_estacion_1.dropna(subset=['FECHA', 'TMAX', 'TMIN'])
df_estacion_1 = df_estacion_1[(df_estacion_1['FECHA'] >= '2024-08-11') & (df_estacion_1['FECHA'] <= '2025-08-11')]
df_estacion_1 = df_estacion_1.groupby('FECHA')[['TMAX', 'TMIN']].mean().reset_index()
# Preparando datos Estación 2 para comparar
df_estacion_2 = df_climaargentina[df_climaargentina['NOMBRE'] == estacion_2].copy()
df_estacion_2 = df_estacion_2.dropna(subset=['FECHA', 'TMAX', 'TMIN'])
df_estacion_2 = df_estacion_2[(df_estacion_2['FECHA'] >= '2024-08-11') & (df_estacion_2['FECHA'] <= '2025-08-11')]
df_estacion_2 = df_estacion_2.groupby('FECHA')[['TMAX', 'TMIN']].mean().reset_index()

print(f"\nDatos para {estacion_1}: {len(df_estacion_1)} dias")
print(f"\nDatos para {estacion_2}: {len(df_estacion_2)} dias")

# Grafico para comparar datos
# Uso subplot para visualizar las dos lineas de ambas estaciones en un mismo grafico
# Tamaño para ambos graficos
plt.figure(figsize=(12, 5))
# Subplot temperaturas maximas
plt.subplot(2,1,1)
plt.plot(df_estacion_1['FECHA'], df_estacion_1['TMAX'], color='red', label=f'{estacion_1} - TMAX', linewidth=2)
plt.plot(df_estacion_1['FECHA'], df_estacion_1['TMIN'], color='darkred', label=f'{estacion_2} - TMAX', linewidth=2, linestyle='--')
plt.title('Comparación de temperaturas maximas entre estaciones meterológicas', fontsize=12)
plt.xlabel('Fecha', fontsize=10)
plt.ylabel('Temperatura Maxima (°C)', fontsize=10)
plt.grid(True)
plt.legend()
# Subplot temperaturas minimas
plt.subplot(2,1,2)
plt.plot(df_estacion_2['FECHA'], df_estacion_2['TMAX'], color='blue', label=f'{estacion_1} - TMAX', linewidth=2)
plt.plot(df_estacion_2['FECHA'], df_estacion_2['TMIN'], color='darkblue', label=f'{estacion_2} - TMAX', linewidth=2, linestyle='--')
plt.title('Comparación de temperaturas minimas entre estaciones meterológicas', fontsize=12)
plt.xlabel('Fecha', fontsize=10)
plt.ylabel('Temperatura Minima (°C)', fontsize=10)
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
# Muestro ambos graficos en una imagen
plt.tight_layout()
plt.show()

