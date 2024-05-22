from src.data_processing import get_percentage_value, Z_VALUES

import argparse

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(prog="FDA de Distribuição Normal Padrão", description="Programa que adquire a probabilidade de um elemento de Z ser menor que outro elemento de Z (chamado de 'valor z', ou 'z value'), no qual Z é uma variável aleatória contínua que tem distribuição normal padrão.")

  parser.add_argument("z_value", action="store", type=str, help="O valor z que deseja descobrir a FDA pela distribuição normal padrão.")
  parser.add_argument("-n", "--negative", dest="negative", action="store_true", help="Indica se o valor é negativo ou não.")

  namespace = parser.parse_args()

  response = f"\u03c6({namespace.z_value}) = {str(get_percentage_value(namespace.z_value, Z_VALUES)).replace('.', ',')}" if not namespace.negative else f"\u03c6({'-' + namespace.z_value}) = {str(get_percentage_value('-' + namespace.z_value, Z_VALUES)).replace('.', ',')}"

  print(response)