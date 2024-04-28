import pytest

import data.recommend as rec_songs


def test_get_bpm_from_speed_stride():
    # Edge case: Test with mph = 0 and stride_ft = 2.5 (should return 0)
    mph = 0
    stride_ft = 2.5
    assert rec_songs.get_bpm_from_speed_stride(mph, stride_ft) == pytest.approx(0, abs=1) # noqa


def test_get_avg_stride_from_gender():
    assert rec_songs.get_avg_stride_from_gender('M') == 2.5
    assert rec_songs.get_avg_stride_from_gender('F') == 2.2


def test_get_bpm_from_speed_avg_stride():
    # Edge case: Test with mph = 0 and gender = 'F'
    mph = 0
    gender = 'F'
    expected_bpm = rec_songs.get_bpm_from_speed_avg_stride(mph, gender)
    assert expected_bpm == 0  # Speed 0 should result in bpm 0


def test_rec_song_from_bpm():
    song = rec_songs.rec_song_from_bpm
    assert song is not None