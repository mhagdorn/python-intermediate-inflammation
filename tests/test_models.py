"""Tests for statistics functions within the Model layer."""
import pytest
import numpy as np
import math
import numpy.testing as npt
import pytest

from inflammation.models import daily_mean
from inflammation.models import daily_max
from inflammation.models import patient_normalise


def test_daily_mean_zeros():
    """Test that mean function works for an array of zeros."""
    

    test_input = np.array([[0, 0],
                           [0, 0],
                           [0, 0]])
    test_result = np.array([0, 0])

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test_input), test_result)


def test_daily_mean_integers():
    """Test that mean function works for an array of positive integers."""

    test_input = np.array([[1, 2],
                           [3, 4],
                           [5, 6]])
    test_result = np.array([3, 4])

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test_input), test_result)

@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [3, 4])
    ]
)
def test_daily_mean(test, expected):
    npt.assert_array_equal(daily_mean(test), expected)


def test_daily_max_string():

    with pytest.raises(TypeError):
        daily_max([["hello", "world"], ["it", "is hot"]])


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]]),
    ])
def test_patient_normalise(test, expected):
    """Test normalisation works for arrays of one and positive integers.
       Test with a relative and absolute tolerance of 0.01."""

    result = patient_normalise(np.array(test))
    npt.assert_allclose(result, np.array(expected), rtol=1e-2, atol=1e-2)

@pytest.mark.parametrize(
    "test, expected, expect_raises",
    [
        # previous test cases here, with None for expect_raises, except for the next one - add ValueError
        # as an expected exception (since it has a negative input value)
        (
            [[-1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[0, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]],
            ValueError,
        ),
        ( [1,2],[2,3], ValueError),
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]],
            None,
        ),
    ])
def test_patient_normalise(test, expected, expect_raises):
    """Test normalisation works for arrays of one and positive integers."""
        
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            patient_normalise(np.array(test))
    else:
        result = patient_normalise(np.array(test))
        npt.assert_allclose(result, np.array(expected), rtol=1e-2, atol=1e-2)

@pytest.mark.parametrize('data,expected_result', [
    ([[[0, 1, 0], [0, 2, 0]]], [0, 0, 0]),
    ([[[0, 2, 0]], [[0, 1, 0]]], [0, math.sqrt(0.25), 0]),
    ([[[0, 1, 0], [0, 2, 0]], [[0, 1, 0], [0, 2, 0]]], [0, 0, 0])
],
ids=['Two patients in same file', 
     'Two patients in different files', 
     'Two identical patients in two different files'])
def test_compute_standard_deviation_by_day(data, expected_result):
    from inflammation.models import compute_standard_deviation_by_day

    result = compute_standard_deviation_by_day(data)
    npt.assert_almost_equal(result, expected_result)
