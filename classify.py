# -*- coding: utf-8 -*-
"""Ecometrica programming exercise"""
import numpy as np
import pandas as pd
import argparse
from IPython.display import display

LANDCOVER_VALUE_TO_TYPE = {
    0: 'water',
    1: 'evergreen needleleaf forest',
    2: 'evergreen broadleaf forest',
    3: 'deciduous needleleaf forest',
    4: 'deciduous broadleaf forest',
    5: 'mixed forest',
    6: 'closed shrublands',
    7: 'open shrublands',
    8: 'woody savannas',
    9: 'savannas',
    10: 'grasslands',
    11: 'permanent wetlands',
    12: 'croplands',
    13: 'urban and built-up',
    14: 'cropland/natural vegetation mosaic',
    15: 'snow and ice',
    16: 'barren or sparsely vegetated',
    255: 'unclassified',
}

# LANDCOVER is a numpy array of (x, y, landcover value)
LANDCOVER = np.array([
    [2, 0, 0],
    [3, 0, 0],
    [4, 0, 0],
    [5, 0, 0],
    [4, 1, 0],
    [4, 5, 0],
    [5, 5, 0],
    [0, 0, 4],
    [0, 1, 4],
    [5, 1, 4],
    [3, 2, 4],
    [4, 2, 4],
    [5, 2, 4],
    [3, 3, 4],
    [2, 4, 6],
    [3, 5, 6],
    [3, 4, 7],
    [2, 5, 7],
    [0, 2, 8],
    [2, 3, 8],
    [0, 4, 8],
    [0, 3, 9],
    [1, 3, 9],
    [1, 4, 9],
    [0, 5, 9],
    [1, 5, 9],
    [1, 0, 10],
    [1, 2, 10],
    [4, 3, 10],
    [4, 4, 10],
    [5, 4, 10],
    [3, 1, 11],
    [1, 1, 12],
    [2, 2, 12],
    [2, 1, 13],
    [5, 3, 13]
])

# CARBON is a numpy array of (x, y, carbon content)
CARBON = np.array([
    [0, 0, 207],
    [1, 0, 26],
    [2, 0, 0],
    [3, 0, 0],
    [4, 0, 0],
    [0, 1, 135],
    [1, 1, 96],
    [2, 1, 156],
    [3, 1, 47],
    [4, 1, 0],
    [0, 2, 196],
    [1, 2, 70],
    [2, 2, 106],
    [3, 2, 126],
    [4, 2, 48],
    [0, 3, 255],
    [1, 3, 225],
    [2, 3, 54],
    [3, 3, 125],
    [4, 3, 230],
    [0, 4, 140],
    [1, 4, 175],
    [2, 4, 48],
    [3, 4, 215],
    [4, 4, 46]
])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--landcover', type=str, help='landcover type')
    parser.add_argument('-s', '--stddev', action='store_true', help='standard deviation')
    return parser.parse_args()


def merge_landcover_carbon():
    landcover_df = pd.DataFrame({'x': LANDCOVER[:, 0],
                                 'y': LANDCOVER[:, 1],
                                 'type': LANDCOVER[:, -1]})
    carbon_df = pd.DataFrame({'x': CARBON[:, 0],
                              'y': CARBON[:, 1],
                              'carbon': CARBON[:, -1]})
    return landcover_df.merge(carbon_df, how='left').drop(['x', 'y'], axis=1)


'''
def convert_type_from_dict_to_numpy(landcover_arg):
    if landcover_arg is None:
        type_list = list(LANDCOVER_VALUE_TO_TYPE.items())
    else:

        # Create a list containing only the landcover arg item
        type_list = list((key, item) for key, item in LANDCOVER_VALUE_TO_TYPE.items() if item == landcover_arg)

    # Create numpy array from list
    return np.asarray(type_list)
'''


def convert_type_from_dict_to_numpy(landcover_arg):
    # Create a list containing only the landcover arg item or all the landcover
    type_list = list((key, item) if (landcover_arg is not None and item == landcover_arg) else item
                     for key, item in LANDCOVER_VALUE_TO_TYPE.items())

    # Create numpy array from list
    return np.asarray(type_list)


def merge_landcover_carbon_type(type_np, landcover_carbon_df):
    type_df = pd.DataFrame({'type': type_np[:, 0],
                            'type_text': type_np[:, -1]})
    type_df.type = type_df.type.astype(int)
    return landcover_carbon_df.merge(type_df, how='right').drop(['type'], axis=1)


def groupby_type_and_calculate(stddev, landcover_carbon_type):
    return landcover_carbon_type.groupby("type_text").apply(calculate(stddev))


def calculate(stddev):
    return pd.DataFrame.agg(['mean', 'std']) if stddev else pd.DataFrame.mean()


'''
def prepare_df_to_display(stddev, landcover_carbon_type_group_df):
    if stddev:
        results_df = landcover_carbon_type_group_df.agg(['mean', 'std'])
        results_df.rename(index=str, columns={results_df.columns[1]: 'Landcover type',
                                              results_df.columns[2]: 'Mean carbon',
                                              results_df.columns[3]: 'Std carbon'})
    else:
        results_df = landcover_carbon_type_group_df.mean()
        print(results_df)

    # Fill nan with 0
    return results_df.fillna(0)
'''


def main():
    args = get_args()
    landcover_carbon_df = merge_landcover_carbon()
    type_np = convert_type_from_dict_to_numpy(args.landcover)
    landcover_carbon_type_df = merge_landcover_carbon_type(type_np, landcover_carbon_df)
    landcover_carbon_type_df = groupby_type_and_calculate(landcover_carbon_type_df)
    print()


if __name__ == '__main__':
    main()
