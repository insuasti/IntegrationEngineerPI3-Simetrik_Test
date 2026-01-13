import polars as pl
import glob
import os
import re
import time

from validaciones import validaciones


def clean_text(text):
    """Limpia caracteres especiales tanto en headers como en datos"""
    if not isinstance(text, str): 
        return text
    # Para headers: quitar ~, $ y convertir a alfanumérico
    text = re.sub(r'[~$]', '', text)
    text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    # Para datos: quitar caracteres no imprimibles
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip('_').strip()


def extract_positional_data(txt_file, excel_file, sheet_name='Body'):
    start_total = time.perf_counter()  # ⏱️ inicio total

    # 1. Cargar la documentación con Polars
    t0 = time.perf_counter()
    # Leer Excel con pandas y convertir columnas a tipos simples
    import pandas as pd
    doc_pd = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Convertir todas las columnas a tipos numpy básicos para evitar error de pyarrow
    for col in doc_pd.columns:
        if doc_pd[col].dtype == 'object':
            doc_pd[col] = doc_pd[col].astype(str)
    
    doc = pl.from_pandas(doc_pd)
    print(f"   ⏱️ Lectura Excel: {(time.perf_counter() - t0) * 1000:.2f} ms")
    
    # Filtrar y limpiar
    t0 = time.perf_counter()
    doc = doc.filter(pl.col('Elm') != 'N°')
    
    # Filtrar filas donde "Formato" sea "Grupo" o "GROUP"
    if 'Formato' in doc.columns:
        doc = doc.filter(
            ~pl.col('Formato').str.to_uppercase().is_in(['GRUPO', 'GROUP'])
        )
        print(f"   ℹ️ Filas filtradas por Formato='Grupo'/'GROUP'. Filas restantes: {len(doc)}")
    
    # Convertir a numérico y ordenar
    doc = doc.with_columns([
        pl.col('Pos Inicial').cast(pl.Int32),
        pl.col('Pos. Final').cast(pl.Int32)
    ]).sort(['Elm', 'Pos Inicial', 'Pos. Final'])
    print(f"   ⏱️ Filtrado y ordenamiento: {(time.perf_counter() - t0) * 1000:.2f} ms")
    
    # 2. Leer archivo TXT
    t0 = time.perf_counter()
    with open(txt_file, 'r', encoding='latin-1') as f:
        lineas = f.readlines()
    
    # Ignorar primera y última línea
    if len(lineas) > 2:
        lineas = lineas[1:-1]
        print(f"   ℹ️ Procesando {len(lineas)} Transacciones (ignorando primera y última)")
    print(f"   ⏱️ Lectura TXT: {(time.perf_counter() - t0) * 1000:.2f} ms")
    
    # 3. Procesar líneas (versión optimizada)
    t0 = time.perf_counter()
    # Pre-extraer la información de doc a listas de Python (más rápido)
    campos = doc['Campo'].to_list()
    pos_inicial = doc['Pos Inicial'].to_list()
    pos_final = doc['Pos. Final'].to_list()
    
    registros = []
    for linea in lineas:
        if len(linea.strip()) < 10: 
            continue
        
        # Extraer todos los campos de una vez usando list comprehension
        data = {
            clean_text(campo): clean_text(linea[start-1:end])
            for campo, start, end in zip(campos, pos_inicial, pos_final)
        }
        registros.append(data)
    
    print(f"   ⏱️ Procesamiento líneas TXT: {(time.perf_counter() - t0) * 1000:.2f} ms")
    
    # 4. Crear DataFrame de Polars
    t0 = time.perf_counter()
    df = pl.DataFrame(registros)
    print(f"   ⏱️ Creación DataFrame: {(time.perf_counter() - t0) * 1000:.2f} ms")

    total_ms = (time.perf_counter() - start_total) * 1000
    print(f"   ⏱️ Tiempo total extract_positional_data: {total_ms:.2f} ms")

    return df


# Ejecución
if __name__ == "__main__":
    start_main = time.perf_counter()  # ⏱️ inicio main
    
    # Ejecutar validaciones
    validaciones()
    
    print("\n--- Procesando datos ---")
    df_resultado = extract_positional_data(
        'data/transacciones_1.txt', 
        'data/Documentación prueba.xlsx', 
        sheet_name='Body'
    )
    
    t0 = time.perf_counter()
    df_resultado.write_csv('output/transacciones_final_polars.csv', include_bom=True)
    print(f"   ⏱️ Escritura CSV: {(time.perf_counter() - t0) * 1000:.2f} ms")

    print(f"\n⏱️ Tiempo total script: {(time.perf_counter() - start_main) * 1000:.2f} ms")