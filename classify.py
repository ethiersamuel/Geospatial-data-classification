# -*- coding: utf-8 -*-
"""Ecometrica programming exercise"""
import argparse
import numpy as np
import pandas as pd
from tabulate import tabulate

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
    '''
    Get the command line arguments.
    :return: Arguments parse
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--landcover', action='store', nargs='*', type=str, help='landcover type')
    parser.add_argument('-s', '--stddev', action='store_true', help='standard deviation')
    args = parser.parse_args()
    if type(args.landcover) == list: args.landcover = ' '.join(args.landcover)
    return args


def create_type_np(landcover):
    '''
    Create ndarray of landcover type. Exit the program if the value of landcover
    is not a valid type.
    :param landcover: Landcover value of the landcover command line argument
    :return: ndarray of the landcover type
    '''
    if landcover is None:
        type_list = create_landcover_list()
    elif validate_landcover(landcover):
        type_list = create_specific_landcover_list(landcover)
    else:
        exit_program(landcover)
    return np.asarray(type_list)


def create_landcover_list():
    '''
    Create a list from the landcover type dictionnay items.
    :return: List of landcover type
    '''
    return list(LANDCOVER_VALUE_TO_TYPE.items())


def validate_landcover(landcover):
    '''
    Validate that the landcover exist in the landcover type dictionnary.
    :param landcover: Landcover value of the landcover command line argument
    :return: Boolean
    '''
    return landcover in LANDCOVER_VALUE_TO_TYPE.values()


def create_specific_landcover_list(landcover):
    '''
    Create a list of the landcover type entered to the command line.
    :param landcover: Landcover value of the landcover command line argument
    :return: List of the landcover type
    '''
    return list((key, item) for key, item in LANDCOVER_VALUE_TO_TYPE.items() if item == landcover)


def exit_program(landcover):
    '''
    Stop the program and display a message.
    :param landcover: Landcover value of the landcover command line argument
    '''
    exit('The landcover type %s is not valid.'
         '\nPlease, select one in the list below: %s' % (landcover, print_landcover_values()))


def print_landcover_values():
    '''
    Create a list of the landcover type as a string.
    :return: List of the landcover type as a string
    '''
    values = ''
    for value in LANDCOVER_VALUE_TO_TYPE.values():
        values += '\n - ' + value
    return values


def create_type_landcover_df(type_np):
    '''
    Create a dataframe of landcover type and landcover by merging a dataframe of
    landcover type to a dataframe of landcover.
    :param type_np: ndarray of landcover type
    :return: Dataframe of landcover type and landcover
    '''
    type_df = pd.DataFrame({'type': type_np[:, 0],
                            'type_text': type_np[:, -1]})
    type_df.type = type_df.type.astype(int)
    landcover_df = pd.DataFrame({'x': LANDCOVER[:, 0],
                                 'y': LANDCOVER[:, 1],
                                 'type': LANDCOVER[:, -1]})
    return type_df.merge(landcover_df, how='left')


def create_type_landcover_carbon_df(type_landcover_df):
    '''
    Create a dataframe of landcover type, landcover and carbon by merging a dataframe of
    landcover type and landcover to a dataframe of carbon.
    :param type_landcover_df: Dataframe of landcover type and landcover
    :return: Dataframe of landcover type, landcover and carbon
    '''
    carbon_df = pd.DataFrame({'x': CARBON[:, 0],
                              'y': CARBON[:, 1],
                              'carbon': CARBON[:, -1]})
    return type_landcover_df.merge(carbon_df, how='left').drop(['x', 'y', 'type'], axis=1)


def process_calculation_by_type(stddev, landcover_carbon_type_df):
    '''
    Group the data by landcover type to calculate the mean and
    stddev by landcover type.
    :param stddev: Stddev value of the stddev command line argument
    :param landcover_carbon_type_df: Dataframe of landcover type, landcover and carbon
    :return: GroupByDataframe of landcover type, landcover and carbon
    '''
    return landcover_carbon_type_df.groupby('type_text', sort=False)\
        .agg(calculate(stddev)).fillna(0)


def calculate(stddev):
    '''
    Create a list of the formula.
    :param stddev: Stddev value of the stddev command line argument
    :return: List of formula
    '''
    return ['mean', lambda x: np.std(x, ddof=0)] if stddev else ['mean']


def print_tabulate(stddev, type_landcover_carbon_df):
    '''
    Print a tabulate of the dataframe.
    :param stddev: Stddev value of the stddev command line argument
    :param type_landcover_carbon_df: GroupByDataframe of landcover type, landcover and carbon
    '''
    headers = create_headers_list(stddev)
    print(tabulate(type_landcover_carbon_df, headers=headers))


def create_headers_list(stddev):
    '''
    Create a list of column header.
    :param stddev: Stddev value of the stddev command line argument
    :return: List of column header
    '''
    return ['Landcover Type', 'Mean carbon', 'SD carbon'] \
        if stddev else ['Landcover Type', 'Mean carbon']


def main():
    ''' Execute the main functionnlity. '''
    args = get_args()
    type_np = create_type_np(args.landcover)
    type_landcover_df = create_type_landcover_df(type_np)
    type_landcover_carbon_df = create_type_landcover_carbon_df(type_landcover_df)
    type_landcover_carbon_df = process_calculation_by_type(args.stddev, type_landcover_carbon_df)
    print_tabulate(args.stddev, type_landcover_carbon_df)


if __name__ == '__main__':
    main()
