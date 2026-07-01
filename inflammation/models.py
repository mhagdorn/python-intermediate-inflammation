"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np
import json


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def load_json(filename):
    """Load a numpy array from a JSON document.
    
    Expected format:
    [
      {
        "observations": [0, 1]
      },
      {
        "observations": [0, 2]
      }    
    ]
    :param filename: Filename of CSV to load
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data_as_json = json.load(file)
        return [np.array(entry['observations']) for entry in data_as_json]


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.
    
    :param data: 2d array containing the inflammation data
    :returns: the daily mean
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.
    
    :param data: 2d array containing the inflammation data
    :returns: the daily maximum"""
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.
    
    :param data: 2d array containing the inflammation data
    :returns: the daily minimum
    """
    return np.min(data, axis=0)

def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array."""

    if not isinstance(data, np.ndarray):
        raise TypeError("expecting a ndarray")

    if len(data.shape) != 2:
        raise ValueError("expected a 2d array")

    if np.any(data < 0):
        raise ValueError("Inflammation values should be non-negative")
    max_data = np.max(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised

def compute_standard_deviation_by_day(data):
    means_by_day = map(daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


