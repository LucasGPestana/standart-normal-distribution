import pandas as pd
import tabula

import os
import sys
import subprocess

from typing import List

# Trata o formato dos valores str dos índices das colunas e linhas e os converte para float
def convert_axes_to_float(df: pd.DataFrame) -> pd.DataFrame:

  df.columns = df.columns.str.replace(",", ".")
  df.columns = df.columns.astype(float)
  
  df.index = df.index.str.replace(",", ".")
  df.index = df.index.astype(float)

  return df

def get_value_if_series(value: float | pd.Series) -> bool:

  if isinstance(value, pd.Series):

    return value.values[0]
  
  return value

def get_database(filepath: str):

  if not os.path.isfile(filepath):

    print("O caminho especificado não corresponde a um arquivo!")
    return None
  
  if not filepath.lower().endswith(".pdf"):

    print("O caminho especificado não se refere a um 'PDF'!")
    return None
  
  while True:

    try:

      return tabula.read_pdf(filepath, encoding="latin-1")

    except PermissionError:

      completed_process = subprocess.run(["java", "--version"], stdout=subprocess.PIPE)

      if not completed_process.stdout.startswith(b"java"):

        os.system("sudo apt install openjdk-11-jdk")
        os.system("clear")

# Pega a porcentagem correspondente ao z percentil passado como argumento
def get_percentage_value(z_percentile: str, df: pd.DataFrame):

  row_index, column_index = process_z_input(z_percentile)

  percentage = get_value_if_series(df.loc[row_index, column_index])
  
  return percentage

# Verifica se a porcentagem passada existe, de forma exata, no DataFrame
# Caso não, são pegos o maior valor menor que a porcentagem e o menor valor maior que a porcentagem no DataFrame
def verify_percentage_situations(percentage: str, 
                                 df: pd.DataFrame, 
                                 row_index: float, 
                                 column_pos_index: int) -> List:
  
  iter_percentage_value = get_value_if_series(df.loc[row_index][df.columns[column_pos_index]])

  # A verificação do sinal do "row_index" garante que a operação aritmética de soma, para obter o valor z, seja feita corretamente
  if iter_percentage_value == percentage:

    return [row_index, df.columns[column_pos_index]] if row_index > 0 else [row_index, -df.columns[column_pos_index]]
  
  # A mesma verificação é feita aqui
  if iter_percentage_value > percentage:

    return (
      [row_index, df.columns[column_pos_index - 1], df.columns[column_pos_index]] if row_index > 0 
      else [row_index, -df.columns[column_pos_index + 1], -df.columns[column_pos_index]]
    )

# Pega o valor z correspondente a porcentagem passada como argumento
def get_z_value(percentage: str, df: pd.DataFrame) -> float:

  possible_values_parts = list() # Representa as partes que constituem o valor z, ou seja, o indice da linha e os possíveis indices de coluna
  percentage = process_percentage_value(percentage)

  # A tabela z segue um padrão no qual, caso o índice da linha seja positivo, o indice da coluna é diretamente proporcional ao valor da porcentagem. No caso de indices de linha negativos, essas grandezas são inversas
  for index in df.index:

    if index < 0:

      # Devido a característica de proporcionalidade e a lógica de pegar os índices de coluna a partir da próxima porcentagem da tabela que passar de "percentage", é necessário iterar o objeto range dos indices posicionais das colunas de trás para frente
      for pos_column in range(len(df.columns) - 1, -1, -1):

        possible_values_parts = verify_percentage_situations(percentage, df, index, pos_column)

        if possible_values_parts: break
      
      if possible_values_parts: break
    
    else:

      # Como aqui o indice da coluna e a porcentagem são diretamente proporcionais, a iteração é feita de frente para trás
      for pos_column in range(0 ,len(df.columns), 1):

        possible_values_parts = verify_percentage_situations(percentage, df, index, pos_column)

        if possible_values_parts: break # Evita que novas iterações no loop interno sejam feitas depois que os valores são achados
      
      if possible_values_parts: break # Mesmo objetivo do de cima, só que para o loop externo
  
  # São pegos as distâncias entre os valores de porcentagem correspondentes àquele valor z com relação a "percentage"
  # O primeiro valor não é considerado pois se refere ao indice da linha selecionada
  # A troca de sinais feita na função verify_percentage_situations para o índice das colunas será "corrigida" com a função abs (módulo)
  distances = list(
    map(lambda x: abs(
      get_value_if_series(df.loc[possible_values_parts[0]][abs(x)]) - percentage
      ), possible_values_parts[1:])
      )
  minor_dist = 100000 # Representa a menor distância entre os valores

  # Pega o índice da coluna que possui a menor distância de porcentagem em relação a "percentage"
  for i in range(len(distances)):

    if minor_dist > distances[i]:

      minor_dist = distances[i]
      more_close_value = possible_values_parts[1:][i]
  
  return possible_values_parts[0] + more_close_value

# Trata a entrada de porcentagem do usuário via linha de comando
def process_percentage_value(percentage: str) -> float:

  percentage = float(percentage.replace(',', '.'))

  percentage = float("{:.4f}".format(percentage))

  return percentage

# Trata a entrada de valor z do usuário via linha de comando
def process_z_input(input_value: str) -> float:

  # Altera a vírgula no número (caso tenha) para um ponto, e converte para float
  input_value = float(input_value.replace(",", "."))

  # Adiciona 2 casas decimais no número, caso não tenha, e retorna a ser str
  input_value = "{:.2f}".format(input_value)

  # Decompoe o número em duas partes: a primeira sendo o inteiro e a primeira casa decimal e o segundo a segunda casa decimal
  return (float(input_value[:-1]), float("0.0" + input_value[-1]))

def verify_if_index_exists(index: str, df: pd.DataFrame, axis: int=0):

  match axis:

    case 0:

      return index in list(df.index.values)

    case 1:

      return index in list(df.columns.values)
    
    case _:

      raise ValueError("'axis' value must be 0 or 1")

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
filepaths = list(map(lambda x: os.path.join("files", x), sorted(os.listdir("files"))))

df_z_values_1 = get_database(filepaths[0])[0]
df_z_values_2 = get_database(filepaths[1])[0]

if sys.platform == "win32":
  os.system("cls")
else:
  os.system("clear")

# Removendo a coluna (e a Series que a reprensta) com valores nulos
if verify_if_index_exists("0", df_z_values_1, 1):

  df_z_values_1 = df_z_values_1.drop("0", axis=1)

# Definindo o nome das colunas e guardando-as em uma variável auxiliar
column_values = df_z_values_1.loc[0].values[1:]

if verify_if_index_exists("Unnamed: 0", df_z_values_1, 1):

  df_z_values_1 = df_z_values_1.set_index(df_z_values_1["Unnamed: 0"].values)

  df_z_values_1 = df_z_values_1.drop("Unnamed: 0", axis=1)

if verify_if_index_exists('z', df_z_values_1, 0):

  df_z_values_1 = df_z_values_1.drop('z', axis=0)

# Alterando os nomes das colunas para os valores correspondentes a 2a casa decimal de z
df_z_values_1.columns = column_values

df_z_values_1 = convert_axes_to_float(df_z_values_1)

# Gerando índices negativos que não foram lidos do pdf
negative_indexes = list(map(lambda x: -x, df_z_values_1.index[:-5]))

# Pegando a parte dos valores positivos
positive_indexes = list(df_z_values_1.index[-5:])

# Alterando os índices do DataFrame para os valores correspondentes ao inteiro e 1a casa decimal de z
df_z_values_1.index = negative_indexes + positive_indexes

if verify_if_index_exists('z', df_z_values_2, 1):

  # Modificando os valores dos indíces a partir de uma series que representa um coluna
  df_z_values_2 = df_z_values_2.set_index(df_z_values_2['z'].values)

  # Removendo a coluna (e Series) com o name 'z'
  df_z_values_2 = df_z_values_2.drop('z', axis=1)

df_z_values_2 = convert_axes_to_float(df_z_values_2)

# Concatena as duas partes da tabela, obtidas no livro do Devore
Z_VALUES = pd.concat((df_z_values_1, df_z_values_2))

Z_VALUES = Z_VALUES.apply(lambda x: x.str.replace(",", ".").astype(float))