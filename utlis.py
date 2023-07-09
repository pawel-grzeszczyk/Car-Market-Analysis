import pandas as pd


def rm_units_and_conv_dtype(arr, units, dtype):
    """
      Removes units from each element in the input array and converts them to the specified data type.

      Args:
          arr (pandas.Series): A pandas Series containing elements with units.
          units (str): The unit string to be removed from each element.
          dtype (str): The data type to convert the elements to. Valid options: 'float', 'int'.

      Returns:
          pandas.Series: A new pandas Series with units removed and elements converted to the specified data type.

      Example:
          >>> import pandas as pd
          >>> arr = pd.Series(['10 kg', '5,3 kg', '15.5 kg', '20 kg', None])
          >>> rm_units_and_conv_dtype(arr, 'kg', 'float')
          0    10.0
          1     5.3
          2    15.5
          3    20.0
          4  None
          dtype: object
    """
    # Remove units from each element in the array
    arr = arr.map(lambda x: (x.split(' ' + units)[0]
                             .replace(' ', '')
                             .replace(',', '.')) if pd.notnull(x) else x)

    # Convert to the specified data type
    if dtype == 'float':
        return arr.astype(float)
    elif dtype == 'int':
        return arr.astype(int)
    return arr
