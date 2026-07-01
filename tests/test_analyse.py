from unittest.mock import Mock


def test_analyse_data_mock_source():
    from inflammation.compute_data import analyse_data
    data_source = Mock()
    data_source.load_inflammation_data.return_value = [
        [[0, 2, 0]],
        [[0, 1, 0]]
    ]

    analyse_data(data_source)