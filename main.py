from src.data_processing import get_percentage_value, get_z_value, Z_VALUES

import argparse

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(prog="FDA de Distribuição Normal Padrão", description="Programa que adquire a probabilidade de um elemento de Z ser menor que outro elemento de Z (chamado de 'valor z', ou 'z value'), no qual Z é uma variável aleatória contínua que tem distribuição normal padrão.")

  action_subcommand = parser.add_subparsers(description="Seleciona qual funcionalidade do programa deseja escolher: Converter um valor z para porcentagem (z_to_per) ou converter uma porcentagem para um valor z (per_to_z)", required=True)

  subparser = action_subcommand.add_parser("z_to_per")
  subparser.add_argument("z_value", action="store", type=str, help="O valor z que deseja descobrir a FDA pela distribuição normal padrão.")
  subparser.add_argument("-n", "--negative", dest="negative", action="store_true", help="Indica se o valor é negativo ou não.")
  subparser.set_defaults(func=get_percentage_value)

  subparser = action_subcommand.add_parser("per_to_z")
  subparser.add_argument("percentage", action="store", type=str, help="A porcentagem que deseja descobrir o valor Z correspondente (entre 0 e 1)")
  subparser.set_defaults(func=get_z_value)

  namespace = parser.parse_args()

  if namespace.func == get_percentage_value:

    response = namespace.func(namespace.z_value, Z_VALUES) if not namespace.negative else namespace.func('-' + namespace.z_value, Z_VALUES)

    print(f"\u03c6({namespace.z_value}) = {str(response).replace('.', ',')}")

  else:

    response = namespace.func(namespace.percentage, Z_VALUES)
    print(f"Z({namespace.percentage}) = {str(response).replace('.', ',')}")