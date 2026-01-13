# 📤🗂️📥 Integration Engineer Test PI3/Simetrik 📤🗂️📥


Integration Enginner to resolve the test

## 🗂️ Aspectos sobre la solución

Para este punto se opto por hacer los siguientes pasos para resolver el ejercicio:

1. Se creo un Script de validaciones que verifica:
  * Validación 1: Archivos de transacciones TXT
  * Validación 2: Archivo de metadatos XLSX
  * Validación 3: Lectura y estructura del archivo Excel
  * Validación 4: Verificar que el directorio 'data/' existe

2. Procesar el archivo TXT de transacciones:
  * Cargar la documentación completa en un DataFrame, teniendo en cuenta Pos Inicial y Pos. Final.
  * Filtrar de la documentación aquellas filas donde "Formato" sea "Grupo" o "GROUP", ya que es información redundante.
  * Ignorar primera y última línea del archivo TXT.
  * Procesar cada línea del archivo TXT, teniendo en cuenta la posición inicial y final de cada campo.

## 🗂️ Adicionales

3. Se realizó un conteo del tiempo que tarda hacer el procesamiento del archivo TXT:

=== VALIDACIONES COMPLETADAS PANDAS===

--- Procesando datos ---
   ⏱️ Lectura Excel: 24.77 ms
   ℹ️ Filas filtradas por Formato='Grupo'/'GROUP'. Filas restantes: 202
   ℹ️ Procesando 15006 Transacciones (ignorando primera y última)
   ⏱️ Procesamiento TXT: 70912.98 ms
   ⏱️ Tiempo total extract_positional_data: 71009.13 ms
   ⏱️ Escritura CSV: 748.71 ms

⏱️ Tiempo total script: 72590.67 ms

Esto se realizó ya que se quiso hacer una prueba piloto con la librería polars para ver si daba mejores resultados en cuanto al tiempo de procesamiento, hubo una mejora significativa *al rededor de 7x*, en el tiempo total de procesamiento

=== VALIDACIONES COMPLETADAS POLARS ===

--- Procesando datos ---
   ⏱️ Lectura Excel: 101.41 ms
   ℹ️ Filas filtradas por Formato='Grupo'/'GROUP'. Filas restantes: 202
   ⏱️ Filtrado y ordenamiento: 407.96 ms
   ℹ️ Procesando 15006 Transacciones (ignorando primera y última)
   ⏱️ Lectura TXT: 213.43 ms
   ⏱️ Procesamiento líneas TXT: 8093.97 ms
   ⏱️ Creación DataFrame: 302.23 ms
   ⏱️ Tiempo total extract_positional_data: 9119.19 ms
   ⏱️ Escritura CSV: 158.30 ms

⏱️ Tiempo total script: 10433.65 ms


## 🗂️ Aspectos a tener en cuenta en el analisis de transacciones.

El archivo parece ser un layout de archivo plano COBOL, típico en conciliaciones bancarias.
De acuerdo a la documentación esta podría ser una posible explicación de las columnas:

Columna	          Significado
Elm	              Índice del campo (documentación, no COBOL real)
Campo	            Nombre lógico/documental
Niv.	            Nivel COBOL (01, 02, 03, 04, 05…)
Formato	          PICTURE (PIC) en COBOL
Tipo	            Tipo lógico/documental
Pos Inicial	      Posición inicial en el archivo plano
Pos Final	        Posición final en el archivo plano
Long.	            Longitud total

Se realizó un análisis revisando inconsistencias, duplicados y solapamientos y se encontró:

1. DUPLICADOS  (MISMA POSICIÓN)

32  9(06) ND 138–143
33  9(06) ND 138–143


2. REDEFINICIONES

Caso crítico: Posición 204–223 (20 bytes)

Aparece redefinida al menos 9 veces

Bloques repetidos
49  X(20)        204–223
50  Grupo        204–223
53  GROUP        204–223
57  Grupo        204–223
59  GROUP        204–223
65  GROUP        204–223
71  GROUP        204–223
75  GROUP        204–223
80  Grupo        204–223

3. CAMPOS QUE SE PISAN (SOLAPAMIENTO)

144 X(04) AN 424–427
145 S9(03) SIGN LEADING SEPARATE 424–427

4. POSICIONES NUMÉRICAS DECLARADAS COMO AN

136 9(22) AN 342–362


5. LONGITUDES QUE NO CUADRAN
79 X(04) AN 220–223 15

Sobre estos hallazgos se solo se realizó la eliminación de todos los campos que tenian el formato GROUP o GRUPO, ya que se eliminaba con esto mucha información repetida(al reededor de 49 campos).

Sobre los otros no se tomaron mas decisiones ya que no se encontraba una explicación clara de que significaba cada campo, ni de la información que estaba siendo almacenada.

## 🗂️ Project Organization

```
├──Sentence2    <- Folder with the solution of Extraction Exercise based on Documentacion.
|   ├── README.md <- Readme about the solution of the sentence/exercise
│   ├── requirements.py <- libraries required to run de project
│   ├── sentence2.py    <- Principal solution with Pandas solution
│   ├── sentence2_polars.py <- Auxiliar solution to test Polars solution
│   ├── validaciones.py   <- Do validations over the input files before to start.
│   ├── data 
│   │   ├── Documentación prueba.xlsx
│   │   └── transacciones_1.txt
│   │
│   └── output
│       ├── transacciones_final_polars.csv
│       └── transacciones_final.csv
│
│



```

## 🔖 Commit Conventions

Este es una convención que utiliza prefijos específicos en los mensajes de commit para indicar el tipo de cambio que se realizó en el código.

**Recomendaciones:**

* Usar el mismo idioma dentro del mismo repositorio para mayor coherencia y claridad, se recomienda inglés por universalidad.

* Escribir los commits iniciando con verbos en presente simple, es decir, crear, actualizar, administrar o *create, update, manage* en inglés.

* Cuando se va a realizar un cambio que podría ser muy grande o "rompedor", usar el formato **BREAKING CHANGE** en el que si se va a realizar un gran cambio, se deja un ! luego del prefijo y el alcance/contexto, ejemplo:  	```
fix(lambda)!: Change of the orchestration to step functions.	```
-
<table>
  <tr>
    <th colspan="4" align="center">🚀CONVENTIONAL COMMIT🚀</th>
  </tr>
  
  <tr>
    <th align="center"><strong>Tipo (prefijo)</strong></th>
    <th align="center"><strong>Contexto</strong></th>
    <th align="center"><strong>Descripción</strong></th>
    <th align="center"><strong>Ejemplo</strong></th>
  </tr>
  <tr>
    <td align="center">feat</td>
    <td align="center">classes</td>
    <td>Añadir clase para limpieza de datos</td>
    <td><code>feat (classes): Add functions to clean data</code></td>
  </tr>
  <tr>
    <td align="center">fix</td>
    <td align="center">data</td>
    <td>Corregir repositorio de datos actualizado</td>
    <td><code>fix (data): Fix the clients data repository</code></td>
  </tr>
  <tr>
    <td align="center">docs</td>
    <td align="center">docs</td>
    <td>Crear la documentación inicial del proyecto</td>
    <td><code>docs (docs): Create README.md file of the project</code></td>
  </tr>
  <tr>
    <td align="center">chore</td>
    <td align="center">Models</td>
    <td>Adicionar nueva variable “edad” al modelo</td>
    <td><code>chore (models): Add new variable age, to the model</code></td>
  </tr>
  <tr>
    <td align="center">test</td>
    <td align="center">notebooks</td>
    <td>Pruebas sobre el resultado del notebook generado</td>
    <td><code>test (notebooks): Create unit test of a notebook component</code></td>
  </tr>
  <tr>
    <td colspan="4"  align="center"><strong>Source:</strong> <a href="https://www.conventionalcommits.org/en/v1.0.0/">https://www.conventionalcommits.org/en/v1.0.0/</a></td>    
  </tr>
  <tr>    
    <td colspan="4" align="center"><strong>Created by:</strong> Daniel Insuasti</td>
  </tr>
</table>


## 💻 Tech Stack

**Programming Language:** Python 🐍

**Principal Libraries Used Sentence1** 

* et_xmlfile==2.0.0
* numpy==2.2.6
* openpyxl==3.1.5
* pandas==2.3.3
* polars==1.37.1
* polars-runtime-32==1.37.1
* pyarrow==22.0.0
* python-dateutil==2.9.0.post0
* pytz==2025.2
* six==1.17.0
* tzdata==2025.3

**Principal Libraries Used Sentence2** 

* requests==2.25.1
* numpy==2.2.6
* openpyxl==3.1.5
* pandas==2.3.3
* polars==1.37.1
* polars-runtime-32==1.37.1
* pyarrow==22.0.0
* python-dateutil==2.9.0.post0
* pytz==2025.2
* six==1.17.0
* tzdata==2025.3

For more details go to *requirements.txt* in each folder/sentence.

## 🚀 Run OnPremise / Locally

Clone the project

```bash
  git clone git@github.com:insuasti/IntegrationEngineerPI3-Simetrik_Test.git
```

Go to the project directory

```bash
  cd IntegrationEngineerPI3-Simetrik_Test
```
Enter to every folder/sentence and create the virtual enviroment and  activate it
```bash
  cd Sentence2
  python3 -m venv .venv_sentence2
  source .venv_sentence2/Scripts/activate
```
Install python libraries in the virtual enviroment

```bash
  pip install -r .\requirements.txt
```
Execute the solution of the sentence

```bash
  python .\sentence2.py
```


--------