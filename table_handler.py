import os
import sys
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

# ------ [ Constants - BT ] --------------------------------------

TRANSMIT_POWER = 4
SPEED_OF_LIGHT = 3 * 10 ** 8
BT_FREQUENCY = 2.4 * 10 ** 9
BT_WAVELENGTH = SPEED_OF_LIGHT / BT_FREQUENCY

# ------ [ Constants - Path Loss Model ] --------------------------------------

FSPL_EXPONENT = 1.7

# ------ [ Constants - Path Loss Model - Path Loss Exponent ] -----------------

# Corridor - 1.15 - 1.63
# 1.15
# MODEL_PATH_LOSS_EXPONENT = 1.15
# 1.246
# MODEL_PATH_LOSS_EXPONENT = 1.246
# 1.342
# MODEL_PATH_LOSS_EXPONENT = 1.342
# 1.438
# MODEL_PATH_LOSS_EXPONENT = 1.438
# 1.534
# MODEL_PATH_LOSS_EXPONENT = 1.534
# 1.63
# MODEL_PATH_LOSS_EXPONENT = 1.63

# Rooms - 2.14 - 2.55
# 2.14
# MODEL_PATH_LOSS_EXPONENT = 2.14
# 2.222
# MODEL_PATH_LOSS_EXPONENT = 2.222
# 2.
# MODEL_PATH_LOSS_EXPONENT = 2.304
# 2.
# MODEL_PATH_LOSS_EXPONENT = 2.386
# 2.
# MODEL_PATH_LOSS_EXPONENT = 2.468
# 2.55
# MODEL_PATH_LOSS_EXPONENT = 2.55

# ------ [ Constants - Path Loss Model - Old Values ] -------------------------

# Current
MODEL_PATH_LOSS_EXPONENT = 2.6
MODEL_PATH_LOSS_STANDARD_DEVIATION = 14.1
MODEL_PATH_LOSS_REFERENCE_DISTANCE = 1


# ------ [ Constants - Data Handle ] ------------------------------------------


NEEDED_MEASUREMENTS = 9


# ------ [ Constants - Table Design ] -----------------------------------------


COL_BT_ADDR = "Bluetooth Address"
COL_SPOT_FROM = "From"
COL_SPOT_TO = "To"
COL_RSSI = "RSSI (dBm)"
COL_AVG_RSSI = "Average RSSI (dBm)"
COL_EST_RSSI_LOG_NORM = "Log Normal - Estimated RSSI (dBm)"
COL_EST_RSSI_ITU = "ITU - Estimated RSSI (dBm)"
COL_EST_RSSI_FTPS = "FSPL - Estimated RSSI (dBm)"
COL_DIST = "Distance (m)"


# ------ [ Constants - Spot Distance ] ----------------------------------------


SPOT_DISTANCES: Dict[str, Dict[str, float]] = {
    "B1": {},
    "B3": {},
    "B4": {"B15": 32.85},  # Reference Distance
    "B5": {},
    "B6": {},
    "B7": {},
    "B8": {},
    "B9": {},
    "B10": {},
    "B11": {},
    "B12": {},
    "B13": {},
    "B14": {},
    "B15": {}
}

SPOT_DISTANCES["B1"]["B6"] = 23.56
SPOT_DISTANCES["B1"]["B13"] = 12.15

SPOT_DISTANCES["B3"]["B5"] = 10.94

SPOT_DISTANCES["B4"]["B5"] = 17.01
SPOT_DISTANCES["B4"]["B7"] = 24.09
SPOT_DISTANCES["B4"]["B8"] = 26.16
SPOT_DISTANCES["B4"]["B14"] = 32.91

SPOT_DISTANCES["B5"]["B3"] = SPOT_DISTANCES["B3"]["B5"]
SPOT_DISTANCES["B5"]["B4"] = SPOT_DISTANCES["B4"]["B5"]
SPOT_DISTANCES["B5"]["B6"] = 14.56

SPOT_DISTANCES["B6"]["B1"] = SPOT_DISTANCES["B1"]["B6"]
SPOT_DISTANCES["B6"]["B5"] = SPOT_DISTANCES["B5"]["B6"]
SPOT_DISTANCES["B6"]["B9"] = 11.96
SPOT_DISTANCES["B6"]["B10"] = 26.98

SPOT_DISTANCES["B7"]["B4"] = SPOT_DISTANCES["B4"]["B7"]
SPOT_DISTANCES["B7"]["B8"] = 16.42
SPOT_DISTANCES["B7"]["B11"] = 22.42

SPOT_DISTANCES["B8"]["B4"] = SPOT_DISTANCES["B4"]["B8"]
SPOT_DISTANCES["B8"]["B7"] = SPOT_DISTANCES["B7"]["B8"]
SPOT_DISTANCES["B8"]["B9"] = 15.36
SPOT_DISTANCES["B8"]["B10"] = 11.20
SPOT_DISTANCES["B8"]["B11"] = 19.05

SPOT_DISTANCES["B9"]["B6"] = SPOT_DISTANCES["B6"]["B9"]
SPOT_DISTANCES["B9"]["B8"] = SPOT_DISTANCES["B8"]["B9"]
SPOT_DISTANCES["B9"]["B10"] = 17.19
SPOT_DISTANCES["B9"]["B12"] = 24.49

SPOT_DISTANCES["B10"]["B8"] = SPOT_DISTANCES["B8"]["B10"]
SPOT_DISTANCES["B10"]["B9"] = SPOT_DISTANCES["B9"]["B10"]
SPOT_DISTANCES["B10"]["B11"] = 10.88
SPOT_DISTANCES["B10"]["B12"] = 11.09

SPOT_DISTANCES["B11"]["B7"] = SPOT_DISTANCES["B7"]["B11"]
SPOT_DISTANCES["B11"]["B8"] = SPOT_DISTANCES["B8"]["B11"]
SPOT_DISTANCES["B11"]["B10"] = SPOT_DISTANCES["B10"]["B11"]
SPOT_DISTANCES["B11"]["B12"] = 11.66

SPOT_DISTANCES["B12"]["B9"] = SPOT_DISTANCES["B9"]["B12"]
SPOT_DISTANCES["B12"]["B10"] = SPOT_DISTANCES["B10"]["B12"]
SPOT_DISTANCES["B12"]["B11"] = SPOT_DISTANCES["B11"]["B12"]

SPOT_DISTANCES["B13"]["B1"] = SPOT_DISTANCES["B1"]["B13"]
SPOT_DISTANCES["B13"]["B14"] = 21.19

SPOT_DISTANCES["B14"]["B4"] = SPOT_DISTANCES["B4"]["B14"]
SPOT_DISTANCES["B14"]["B13"] = SPOT_DISTANCES["B13"]["B14"]
SPOT_DISTANCES["B14"]["B15"] = 10.04

SPOT_DISTANCES["B15"]["B14"] = SPOT_DISTANCES["B14"]["B15"]
SPOT_DISTANCES["B15"]["B4"] = SPOT_DISTANCES["B4"]["B15"]

# Summed Distances
SPOT_DISTANCES["B6"]["B12"] = \
    SPOT_DISTANCES["B6"]["B9"] + SPOT_DISTANCES["B9"]["B12"]
SPOT_DISTANCES["B6"]["B13"] = \
    SPOT_DISTANCES["B1"]["B13"] + SPOT_DISTANCES["B1"]["B6"]

SPOT_DISTANCES["B7"]["B15"] = \
    SPOT_DISTANCES["B4"]["B7"] + SPOT_DISTANCES["B4"]["B15"]

SPOT_DISTANCES["B8"]["B12"] = \
    SPOT_DISTANCES["B8"]["B10"] + SPOT_DISTANCES["B10"]["B12"]

SPOT_DISTANCES["B9"]["B11"] = \
    SPOT_DISTANCES["B9"]["B10"] + SPOT_DISTANCES["B10"]["B11"]

SPOT_DISTANCES["B10"]["B6"] = SPOT_DISTANCES["B6"]["B10"]

SPOT_DISTANCES["B11"]["B9"] = SPOT_DISTANCES["B9"]["B11"]

SPOT_DISTANCES["B12"]["B6"] = SPOT_DISTANCES["B6"]["B12"]
SPOT_DISTANCES["B12"]["B8"] = SPOT_DISTANCES["B8"]["B12"]

SPOT_DISTANCES["B13"]["B6"] = SPOT_DISTANCES["B6"]["B13"]
SPOT_DISTANCES["B13"]["B15"] = \
    SPOT_DISTANCES["B13"]["B14"] + SPOT_DISTANCES["B14"]["B15"]

SPOT_DISTANCES["B15"]["B13"] = SPOT_DISTANCES["B13"]["B15"]
SPOT_DISTANCES["B15"]["B7"] = SPOT_DISTANCES["B7"]["B15"]

# ------ [ Helper Methods ] ---------------------------------------------------


def print_program_usage() -> None:
    """Print information about how to execute the program.

    :return: Nothing
    """
    print("usage: python3 table_parser.py <table_file>")


# ------ [ Imported Methods - Path Loss ] -------------------------------------

def free_space_path_loss(distance: float) -> float:
    """Free space path loss

    :param distance:
    :return:
    """
    return TRANSMIT_POWER - (-20 * np.log10(BT_WAVELENGTH) + 10 * FSPL_EXPONENT * np.log10(distance) + np.log10(21.98))


def itu_path_loss(distance: float) -> float:
    """ITU model for the same floor where reference distance is 1 meter.

    :param distance: Distance in meters
    :return:
    """

    return TRANSMIT_POWER - (20 * np.log10(BT_FREQUENCY) - 28 +
                             30 * np.log10(distance / MODEL_PATH_LOSS_REFERENCE_DISTANCE))


def log_distance_path_loss(transmitted_power: float, distance: float) -> float:
    """Calculates the received power using the Log-Distance Path Loss model
    for BLE communications.

    :param transmitted_power: The transmitted power (in dBm).
    :param distance: The distance between the transmitter and the receiver
    (in meters).
    :return: The received power (in dBm).
    """
    path_loss_at_ref_dist = (4 * np.pi * MODEL_PATH_LOSS_REFERENCE_DISTANCE / BT_WAVELENGTH) ** 2
    path_loss_at_ref_dist_dbm = 10 * np.log10(path_loss_at_ref_dist)

    path_loss_exponent = MODEL_PATH_LOSS_EXPONENT
    standard_deviation_log_normal_shadowing_dbm = \
        MODEL_PATH_LOSS_STANDARD_DEVIATION
    # standard_deviation_log_normal_shadowing = \
    #    10 ** (standard_deviation_log_normal_shadowing_dbm / 10)
    path_loss_dbm = \
        path_loss_at_ref_dist_dbm + 10 * path_loss_exponent * \
        np.log10(distance / MODEL_PATH_LOSS_REFERENCE_DISTANCE) + \
        np.random.normal(0, standard_deviation_log_normal_shadowing_dbm)

    return transmitted_power - path_loss_dbm  # received power in dBm


def estimate_received_power(distance: float) -> float:
    """Estimate the received power for BLE communications.

    :param distance: The distance between the transmitter and the receiver
    (in meters).
    :return: The estimated received power (in dBm).
    """
    samples = 100
    rpi_ble_transmitted_power_dbm = 4

    received_power_dbm = {}
    for i in range(samples):
        received_power_dbm[i] = \
            log_distance_path_loss(rpi_ble_transmitted_power_dbm, distance)

    average_received_power_dbm = 0
    for k in range(samples):
        average_received_power_dbm += received_power_dbm[k]

    return average_received_power_dbm / samples


# ------ [ Spot Handling ] ----------------------------------------------------


def get_missing_pairs(df: DataFrame) -> List[Tuple[str, str]]:
    """Check for missing pairs of measurements

    :return: The missing pars.
    """
    seen_pairs = []
    needed_pairs = []
    missing_pairs = []

    for index, row in get_spot_first_rows(df).iterrows():
        seen_pairs.append((row[COL_SPOT_FROM], row[COL_SPOT_TO]))
        needed_pairs.append((row[COL_SPOT_TO], row[COL_SPOT_FROM]))

    for spot_from, spot_to in needed_pairs:
        found_pair = \
            list(filter(lambda x: x[0] == spot_from and x[1] == spot_to,
                        seen_pairs))

        if len(found_pair) == 0:
            missing_pairs.append((spot_from, spot_to))

    return missing_pairs


# ------ [ Table Sorting ] ----------------------------------------------------


def spot_sorting() -> Dict[str, int]:
    """Custom table sorting by spot names.

    :return: The custom sorting dict containing the order each spot should have
    in a sort.
    """
    custom_sort = {}
    for spot in range(100):
        custom_sort[f"A{spot + 1}"] = spot
    for spot in range(100):
        custom_sort[f"B{spot}"] = spot + 100

    return custom_sort


# ------ [ Table Handling ] ---------------------------------------------------


def convert_spots_to_uppercase(df: DataFrame) -> DataFrame:
    """Convert all spot names to uppercase

    :param df: The table containing all data.
    :return: The table with spots now in uppercase.
    """
    df[COL_SPOT_FROM] = df[COL_SPOT_FROM].str.upper()
    df[COL_SPOT_TO] = df[COL_SPOT_TO].str.upper()
    return df


def get_spot_first_rows(df: DataFrame) -> DataFrame:
    """The first rows for each measurement spot in order to find all
    unique combinations of spots.

    :param df: The raw table with measurements.
    :return: A table only containing one row for each measurement spot.
    """
    return df.drop_duplicates(subset=[COL_SPOT_FROM, COL_SPOT_TO],
                              keep='first')


def get_rows_for_measurement(df: DataFrame, row: Series):
    """Select needed number rows for each measurement spot to be used in
    the analysis.

    :param df: The raw table.
    :param row: The row containing the information about which spots to
    select measurements for.
    :return: The number of needed rows for each spot measurement.
    """
    available_measurements = len(df.loc[
            (df[COL_SPOT_FROM] == row[COL_SPOT_FROM]) &
            (df[COL_SPOT_TO] == row[COL_SPOT_TO])])
    if available_measurements < NEEDED_MEASUREMENTS:
        raise Exception(
            f"There's not enough rows for spot {row[COL_SPOT_FROM]} to "
            f"{row[COL_SPOT_TO]}. Wanted {NEEDED_MEASUREMENTS} but only have "
            f"{available_measurements} measurement(s).")

    return \
        df.loc[
            (df[COL_SPOT_FROM] == row[COL_SPOT_FROM]) &
            (df[COL_SPOT_TO] == row[COL_SPOT_TO])][:NEEDED_MEASUREMENTS]


def make_table_of_average_rssi(df: DataFrame) -> DataFrame:
    """Make a table containing the average RSSI between spots.

    :param df: The table to calculate RSSI averages from.
    :return: The new table containing the RSSI averages.
    """
    averages_table_df = \
        pd.DataFrame({COL_BT_ADDR: [], COL_SPOT_FROM: [], COL_SPOT_TO: [], COL_AVG_RSSI: []})

    for index, row in get_spot_first_rows(df).iterrows():
        chosen_rows = get_rows_for_measurement(df, row)
        chosen_rows_average = chosen_rows.loc[:, COL_RSSI].mean()

        new_row = \
            pd.DataFrame(
                {COL_BT_ADDR: row[COL_BT_ADDR],
                 COL_SPOT_FROM: row[COL_SPOT_FROM],
                 COL_SPOT_TO: row[COL_SPOT_TO],
                 COL_AVG_RSSI: chosen_rows_average}, index=[0])

        averages_table_df = \
            pd.concat([averages_table_df.loc[:], new_row]
                      ).reset_index(drop=True)

    return averages_table_df


def add_spot_distances_to_table(df: DataFrame) -> DataFrame:
    """Add distances between spots to table containing spot names named
    'From' and 'To'.

    :param df: The table to insert spot distances to.
    :return:
    """
    if COL_SPOT_FROM not in df or COL_SPOT_TO not in df:
        raise Exception(
            f"Need columns '{COL_SPOT_FROM}' and '{COL_SPOT_TO}"
            f"' to add distances")

    spot_distances: List[float] = []

    for index, row in df.iterrows():
        if row[COL_SPOT_FROM] in SPOT_DISTANCES and \
                row[COL_SPOT_TO] in SPOT_DISTANCES[row[COL_SPOT_FROM]]:
            spot_distances.append(
                SPOT_DISTANCES[row[COL_SPOT_FROM]][row[COL_SPOT_TO]])
        else:
            raise Exception(
                f"Missing distance information for spot "
                f"{row[COL_SPOT_FROM]} to {row[COL_SPOT_TO]}!")

    df.insert(len(df.columns), COL_DIST, spot_distances, allow_duplicates=True)

    return df


def add_estimated_rssi_to_table(df: DataFrame) -> DataFrame:
    if COL_DIST not in df:
        raise Exception(
            f"Need columns '{COL_DIST}' to add RSSI estimations.")

    log_normal_rssi_estimations: List[float] = []
    itu_rssi_estimations: List[float] = []
    fspl_rssi_estimations: List[float] = []

    #  COL_EST_RSSI_ITU

    for index, row in df.iterrows():
        log_normal_rssi_estimations.append(estimate_received_power(row[COL_DIST]))
        itu_rssi_estimations.append(itu_path_loss(row[COL_DIST]))
        fspl_rssi_estimations.append(free_space_path_loss(row[COL_DIST]))

    df.insert(len(df.columns), COL_EST_RSSI_LOG_NORM, log_normal_rssi_estimations,
              allow_duplicates=True)

    df.insert(len(df.columns), COL_EST_RSSI_ITU, itu_rssi_estimations,
              allow_duplicates=True)

    df.insert(len(df.columns), COL_EST_RSSI_FTPS, fspl_rssi_estimations,
              allow_duplicates=True)

    return df


# ------ [ Main Program ] -----------------------------------------------------


def run_handle_table(file_path: str):
    df = pd.read_csv(file_path)
    df = convert_spots_to_uppercase(df)
    df = make_table_of_average_rssi(df)\
        .sort_values(by=[COL_SPOT_FROM, COL_SPOT_TO],
                     key=lambda x: x.map(spot_sorting()))\
        .reset_index(drop=True)

    add_spot_distances_to_table(df)
    add_estimated_rssi_to_table(df)

    # Check for missing pairs
    missing_pairs = get_missing_pairs(df)

    if len(missing_pairs) > 0:
        print(f"There are pairs missing: {missing_pairs}")
        sys.exit(1)

    # Reorder columns
    col_average_rssi = df.pop(COL_AVG_RSSI)
    df.insert(3, COL_AVG_RSSI, col_average_rssi)

    print(df.to_csv(index=False))


if __name__ == '__main__':
    # Program Execution
    if len(sys.argv) != 2:
        print_program_usage()
        sys.exit(1)

    file = ""
    if not os.path.exists(sys.argv[1]):
        print(f"File '{sys.argv[1]}' cannot be found.")
        print_program_usage()
        sys.exit(1)
    else:
        file = sys.argv[1]

    run_handle_table(file)




