import pytest

import data.recommend as recommended_songs


def test_get_avg_stride_from_gender():
    assert recommended_songs.get_avg_stride_from_gender('M') == 2.5
    assert recommended_songs.get_avg_stride_from_gender('F') == 2.2
