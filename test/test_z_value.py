from src.data_processing import get_percentage_value, Z_VALUES
import pytest

#@pytest.mark.skip(reason="")
def test_get_percentage_value():

  Z_VALUE = "2,47"

  print(f"Z value of {Z_VALUE} is {get_percentage_value(Z_VALUE, Z_VALUES)}")