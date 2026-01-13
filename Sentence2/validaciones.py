import pandas as pd
import glob
import os


# para revisar y verificar los archivos CSV descargados.
def validaciones():
    """
    Valida la existencia y estructura de los archivos necesarios para el procesamiento.
    """
    print("=== INICIANDO VALIDACIONES ===\n")
    # Validación 1: Archivos de transacciones TXT
    
    print("1. Validando archivos de transacciones (.txt)...")
    
    try:
        archivos_transacciones_txt = glob.glob("data/transacciones_*.txt")
        if archivos_transacciones_txt:
            print(f"   ✓ Archivos encontrados: {len(archivos_transacciones_txt)}")
            for archivo in sorted(archivos_transacciones_txt):
                print(f"     - {os.path.basename(archivo)}")
        else:
            print("   ✗ No se encontraron archivos de transacciones TXT.")
            print("     Deberías tener: transacciones_*.txt en el directorio 'data/'")
    except Exception as e:
        print(f"   ✗ Error al buscar archivos de transacciones: {e}")
    
    print()

    # Validación 2: Archivo de metadatos XLSX
    print("2. Validando archivo de metadatos (.xlsx)...")
    try:
        archivo_metadatos_xlsx = glob.glob("data/Documentación prueba.xlsx")
        if archivo_metadatos_xlsx:
            print(f"   ✓ Archivo encontrado: {len(archivo_metadatos_xlsx)}")
            for archivo in sorted(archivo_metadatos_xlsx):
                print(f"     - {os.path.basename(archivo)}")
        else:
            print("   ✗ No se encontró el archivo de metadatos XLSX.")
            print("     Deberías tener: 'Documentación prueba.xlsx' en el directorio 'data/'")
    except Exception as e:
        print(f"   ✗ Error al buscar archivo de metadatos: {e}")
    
    print()

    # Validación 3: Lectura y estructura del archivo Excel
    print("3. Validando estructura del archivo Excel...")
    try:
        xl = pd.ExcelFile('data/Documentación prueba.xlsx')
        print(f"   ✓ Archivo Excel leído correctamente")
        print(f"   ✓ Hojas encontradas: {xl.sheet_names}")
        
        # Validación adicional: verificar que existe la hoja 'Body'
        if 'Body' in xl.sheet_names:
            print(f"   ✓ Hoja 'Body' encontrada")
            
            # Intentar cargar la hoja para verificar su estructura
            try:
                df_body = pd.read_excel(xl, sheet_name='Body')
                print(f"   ✓ Hoja 'Body' cargada: {len(df_body)} filas, {len(df_body.columns)} columnas")
                
                # Verificar columnas esperadas
                columnas_esperadas = ['Elm', 'Pos Inicial', 'Pos. Final', 'Campo']
                columnas_faltantes = [col for col in columnas_esperadas if col not in df_body.columns]
                
                if columnas_faltantes:
                    print(f"   ⚠ Advertencia: Columnas faltantes en 'Body': {columnas_faltantes}")
                else:
                    print(f"   ✓ Todas las columnas esperadas están presentes")
                    
            except Exception as e:
                print(f"   ✗ Error al cargar la hoja 'Body': {e}")
        else:
            print(f"   ⚠ Advertencia: La hoja 'Body' no fue encontrada")
            
    except FileNotFoundError:
        print("   ✗ Error: El archivo 'Documentación prueba.xlsx' no existe")
        print("     Verifica que el archivo esté en el directorio 'data/'")
    except Exception as e:
        print(f"   ✗ Error al leer el archivo Excel: {e}")
    
    print()

    # Validación 4: Verificar que el directorio 'data/' existe
    print("4. Validando directorio de datos...")
    try:
        if os.path.exists('data'):
            print("   ✓ Directorio 'data/' existe")
            archivos_en_data = os.listdir('data')
            print(f"   ✓ Archivos en 'data/': {len(archivos_en_data)}")
        else:
            print("   ✗ El directorio 'data/' no existe")
            print("     Crea el directorio y coloca los archivos necesarios")
    except Exception as e:
        print(f"   ✗ Error al verificar el directorio 'data/': {e}")
    
    print("\n=== VALIDACIONES COMPLETADAS ===")