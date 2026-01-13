# 📤🗂️📥 Integration Engineer Test PI3/Simetrik 📤🗂️📥


Integration Enginner to resolve the test



## 🗂️ Project Organization

```
├── README.md   <- The top-level README for developers using this project.
│
├── Sentence1    <- Folder with the solution of API Rest consume Exercise
|   ├── README.md <- Readme about the solution of the sentence/exercise
|   ├── requirements.py <- libraries required to run de project
│   ├── sentence1.py <- Solution with OOP of consume Deezer API and retrieve the top Global
│   └── output 
│       ├── top_generoMusical1.csv
│       └── top_generoMusical2.csv
│       └── ...
│       └── top_generoMusicaln.csv
│
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
├── gitignore.txt
│ 				
│
└── requirements.txt  <- The requirements file for reproducing the analysis environment, e.g.
                          generated with `pip freeze > requirements.txt`

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
  cd Sentence1
  python3 -m venv .venv_sentence1
  source .venv_sentence1/Scripts/activate
```
Install python libraries in the virtual enviroment

```bash
  pip install -r .\requirements.txt
```
Execute the solution of the sentence

```bash
  python .\sentence1.py
```


--------