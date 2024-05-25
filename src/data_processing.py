import pandas as pd
import tabula

import os
import sys

from typing import Tuple, List

# Trata o formato dos valores str dos índices das colunas e linhas e os converte para float
def convert_axes_to_float(df: pd.DataFrame) -> pd.DataFrame:

  df.columns = df.columns.str.replace(",", ".")
  df.columns = df.columns.astype(float)
  
  df.index = df.index.str.replace(",", ".")
  df.index = df.index.astype(float)

  return df

def get_database(filepath: str):

  if not os.path.isfile(filepath):

    print("O caminho especificado não corresponde a um arquivo!")
    return None
  
  if not filepath.lower().endswith(".pdf"):

    print("O caminho especificado não se refere a um 'PDF'!")
    return None

  return tabula.read_pdf(filepath, encoding="latin-1")

# Pega a porcentagem correspondente ao z percentil passado como argumento
def get_percentage_value(z_percentile: str, df: pd.DataFrame):

  percentage = df.loc[*process_input(z_percentile)]

  if isinstance(percentage, pd.Series):

    percentage = percentage.values[0]
  
  return percentage

# Verifica se existe a porcentagem exata e, caso não, retorna uma lista contendo
def verify_percentage_situations(percentage: str, 
                                 df: pd.DataFrame, 
                                 row_index: float, 
                                 column_pos_index: int) -> List | float:
  
  iter_percentage_value = df.loc[row_index][df.columns[column_pos_index]]

  iter_percentage_value = (

    iter_percentage_value if not isinstance(iter_percentage_value, pd.Series) else iter_percentage_value.values[0]

  )

  if iter_percentage_value == percentage:

    return [row_index, df.columns[column_pos_index]] if row_index > 0 else [row_index, -df.columns[column_pos_index]]
  
  if iter_percentage_value > percentage:

    return (
      [row_index, df.columns[column_pos_index - 1], df.columns[column_pos_index]] if row_index > 0 
      else [row_index, -df.columns[column_pos_index + 1], -df.columns[column_pos_index]]
    )

def get_z_value(percentage: str, df: pd.DataFrame) -> float:

  possible_values = list() # Caso não tenha o valor exato da porcentagem
  percentage = process_percentage_value(percentage)

  for index in df.index:

    if index < 0:

      for pos_column in range(len(df.columns) - 1, -1, -1):

        possible_values = verify_percentage_situations(percentage, df, index, pos_column)

        if possible_values: break
      
      if possible_values: break
    
    else:

      for pos_column in range(0 ,len(df.columns), 1):

        possible_values = verify_percentage_situations(percentage, df, index, pos_column)

        # print(f"Linha: {index}\nColuna: {df.columns[pos_column]}\nValores possíveis: {possible_values}\n")

        if possible_values: break
      
      if possible_values: break
  
  # O primeiro valor não é considerado pois se refere ao indice da linha selecionada
  distances = list(map(lambda x: abs(df.loc[possible_values[0]][abs(x)] - percentage), possible_values[1:]))
  minor_dist = 100000 # Representa a menor distância entre os valores

  for i in range(len(distances)):

    if minor_dist > distances[i]:

      minor_dist = distances[i]
      more_close_value = possible_values[1:][i]
  
  return possible_values[0] + more_close_value

def process_percentage_value(percentage: str) -> float:

  percentage = float(percentage.replace(',', '.'))

  percentage = float("{:.4f}".format(percentage))

  return percentage

def process_input(input_value: str) -> float:

  # Altera a vírgula no número (caso tenha) para um ponto, e converte para float
  input_value = float(input_value.replace(",", "."))

  # Adiciona 2 casas decimais no número, caso não tenha, e retorna a ser str
  input_value = "{:.2f}".format(input_value)

  # Decompoe o número em duas partes: a primeira sendo o inteiro e a primeira casa decimal e o segundo a segunda casa decimal
  return (float(input_value[:-1]), float("0.0" + input_value[-1]))

filepaths = list(map(lambda x: os.path.join("files", x), os.listdir("files")))

df_z_values_1 = get_database(filepaths[0])[0]
df_z_values_2 = get_database(filepaths[1])[0]

if sys.platform == "win32":
  os.system("cls")
else:
  os.system("clear")

# Removendo a coluna (e a Series que a reprensta) com valores nulos
df_z_values_1 = df_z_values_1.drop("0", axis=1)

# Definindo o nome das colunas e guardando-as em uma variável auxiliar
column_values = df_z_values_1.loc[0].values[1:]

df_z_values_1 = df_z_values_1.set_index(df_z_values_1["Unnamed: 0"].values)

df_z_values_1 = df_z_values_1.drop("Unnamed: 0", axis=1)
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

# Modificando os valores dos indíces a partir de uma series que representa um coluna
df_z_values_2 = df_z_values_2.set_index(df_z_values_2['z'].values)

# Removendo a coluna (e Series) com o name 'z'
df_z_values_2 = df_z_values_2.drop('z', axis=1)

df_z_values_2 = convert_axes_to_float(df_z_values_2)

# Concatena as duas partes da tabela, obtidas no livro do Devore
Z_VALUES = pd.concat((df_z_values_1, df_z_values_2))

Z_VALUES = Z_VALUES.apply(lambda x: x.str.replace(",", ".").astype(float))