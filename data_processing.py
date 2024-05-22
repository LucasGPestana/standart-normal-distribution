import pandas as pd
import tabula

import os
import sys

def get_database(filepath: str):

  if not os.path.isfile(filepath):

    print("O caminho especificado não corresponde a um arquivo!")
    return None
  
  if not filepath.lower().endswith(".pdf"):

    print("O caminho especificado não se refere a um 'PDF'!")
    return None

  return tabula.read_pdf(filepath, encoding="latin-1")

df_z_values_1 = get_database("z-table-part-1.pdf")[0]
df_z_values_2 = get_database("z-table-part-2.pdf")[0]

if sys.platform == "win32":
  os.system("cls")
else:
  os.system("clear")

# Removendo coluna (e Series) com valores nulos
df_z_values_1 = df_z_values_1.drop("0", axis=1)

# Alterando os labels das Series de coluna para os valores correspondentes a 2a casa decimal de z
df_z_values_1.columns = df_z_values_1.loc[0].values

# Alterando os índices do DataFrama para os valores correspondentes ao inteiro e 1a casa decimal de z
df_z_values_1 = df_z_values_1.set_index(df_z_values_1['z'].values)

# Removendo a Series linha e Series coluna de label z, usada anteriormente para definir os índices
df_z_values_1 = df_z_values_1.drop('z', axis=1)
df_z_values_1 = df_z_values_1.drop('z', axis=0)

# Pegando a parte dos valores negativos na tabela, e adicionando o sinal de negativo neles
negative_indexes = list(map(lambda x: str(-float(x.replace(",", "."))).replace(".", ","), df_z_values_1.index[:-5]))

# Pegando a parte dos valores positivos
positive_indexes = list(df_z_values_1.index[-5:])

# Alterando os índices do DataFrame para os valores obtidos anteriormente
df_z_values_1.index = negative_indexes + positive_indexes

# Modificando os valores dos indíces a partir de uma series que representa um coluna
df_z_values_2 = df_z_values_2.set_index(df_z_values_2['z'].values)

# Removendo a coluna (e Series) com o name 'z'
df_z_values_2 = df_z_values_2.drop('z', axis=1)

# Concatena as duas partes da tabela, obtidas no livro do Devore
Z_VALUES = pd.concat((df_z_values_1, df_z_values_2))

# Pega a porcentagem correspondente ao z percentil passado como argumento
def get_percentage_value(z_percentile: str, df: pd.DataFrame=Z_VALUES):

  return df.loc[*process_input(z_percentile)]

def process_input(input_value):

  # Altera a vírgula no número (caso tenha) para um ponto, e converte para float
  input_value = float(input_value.replace(",", "."))

  # Adiciona 2 casas decimais no número, caso não tenha, e retorna a ser str
  input_value = "{:.2f}".format(input_value)

  # Volta a ter vírgula em vez do ponto
  input_value = input_value.replace(".", ",")

  # Decompoe o número em duas partes: a primeira sendo o inteiro e a primeira casa decimal e o segundo a segunda casa decimal
  # Caso o número seja negativo, a quantidade de caracteres pegos para a primeira parte acrescenta 1 (referente ao sinal de negativo)
  if input_value.startswith("-"):

    return (input_value[:4], "0,0" + input_value[-1])
  
  else:

    return (input_value[:3], "0,0" + input_value[-1])