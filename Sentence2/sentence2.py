import pandas as pd
import glob
import os
import re
import time  


from validaciones import validaciones


def clean_text(text):
    """Limpia caracteres especiales tanto en headers como en datos"""
    if not isinstance(text, str): return text
    # Para headers: quitar ~, $ y convertir a alfanumérico
    text = re.sub(r'[~$]', '', text)
    text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    # Para datos: quitar caracteres no imprimibles
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip('_').strip()

def extract_positional_data(txt_file, excel_file, sheet_name='Body'):
    start_total = time.perf_counter()  # ⏱️ inicio total

    # 1. Cargar la documentación completa (TODAS las filas, exceptuando la de Elm = N°)
    t0 = time.perf_counter()
    doc = pd.read_excel(excel_file, sheet_name=sheet_name)
    doc = doc[doc['Elm'] != 'N°'].copy()
    print(f"   ⏱️ Lectura Excel: {(time.perf_counter() - t0) * 1000:.2f} ms")


    # Filtrar filas donde "Formato" sea "Grupo" o "GROUP"
    if 'Formato' in doc.columns:
        doc = doc[~doc['Formato'].str.upper().isin(['GRUPO', 'GROUP'])].copy()
        print(f"   ℹ️ Filas filtradas por Formato='Grupo'/'GROUP'. Filas restantes: {len(doc)}")
    
    doc['Pos Inicial'] = pd.to_numeric(doc['Pos Inicial'])
    doc['Pos. Final'] = pd.to_numeric(doc['Pos. Final'])
    
    # Ordenar por posiciones para procesamiento consistente
    doc = doc.sort_values(by=['Elm','Pos Inicial', 'Pos. Final'])
    
    
    # 2. Procesar el archivo TXT
    t0 = time.perf_counter()
    registros = []
    with open(txt_file, 'r', encoding='latin-1') as f: # latin-1 suele ser mejor para estos TXT
        lineas = f.readlines()
    
        # Ignorar primera y última línea
        if len(lineas) > 2:
            lineas = lineas[1:-1]
            print(f"   ℹ️ Procesando {len(lineas)} Transacciones (ignorando primera y última)")
    
        
        for linea in lineas:
            if len(linea.strip()) < 10: continue
            data = {}

            for idx, row in doc.iterrows():
                col_name = clean_text(row['Campo'])
                start = int(row['Pos Inicial']) - 1
                end = int(row['Pos. Final'])
                val = clean_text(linea[start:end])
                data[col_name] = val
            
            registros.append(data)

    print(f"   ⏱️ Procesamiento TXT: {(time.perf_counter() - t0) * 1000:.2f} ms")

    total_ms = (time.perf_counter() - start_total) * 1000
    print(f"   ⏱️ Tiempo total extract_positional_data: {total_ms:.2f} ms")

    return pd.DataFrame(registros)

    

# Ejecución

# Ejecución
if __name__ == "__main__":
    start_main = time.perf_counter()  # ⏱️ inicio main
    # Ejecutar validaciones
    validaciones()
    
    print("\n--- Procesando datos ---")
    df_resultado = extract_positional_data('data/transacciones_1.txt', 'data/Documentación prueba.xlsx', sheet_name='Body')
    
    t0 = time.perf_counter()
    df_resultado.to_csv('output/transacciones_final.csv', index=False, encoding='utf-8-sig')

    print(f"   ⏱️ Escritura CSV: {(time.perf_counter() - t0) * 1000:.2f} ms")

    print(f"\n⏱️ Tiempo total script: {(time.perf_counter() - start_main) * 1000:.2f} ms")
