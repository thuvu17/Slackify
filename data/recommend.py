"""
recommend.py: the interface to song recommendation interaction data.
"""
import data.db_connect as dbc
import data.songs as songs

SONGS_COLLECT = 'songs'

AVG_STRIDE_WOMAN_FT = 2.2
AVG_STRIDE_MAN_FT = 2.5
AVG_STRIDE_OVER_HEIGHT_IN_WOMAN = 0.413
AVG_STRIDE_OVER_HEIGHT_IN_MAN = 0.415
FT_PER_MILE = 5280
IN_PER_FT = 12

YOGA_ENERGY = [0.0, 0.3]
PILATES_ENERGY = [0.1, 0.4]
CYCLING_ENERGY = [0.5, 0.7]
HEAVIER_ENERGY = [0.6, 0.8]


# Calculate the BPM (Beats Per Minute) based on running speed
# and stride length
def get_bpm_from_speed_stride(mph, stride_ft):
    steps_per_mile = 1/stride_ft * FT_PER_MILE
    return mph / 60 * steps_per_mile


# Get average stride length (ft) from gender
def get_avg_stride_from_gender(gender):
    if gender == 'M':
        return AVG_STRIDE_MAN_FT
    else:
        return AVG_STRIDE_WOMAN_FT


# Get speed (bpm) from speed (mph) using average stride length (ft)
def get_bpm_from_speed_avg_stride(mph, gender):
    avg_stride_ft = get_avg_stride_from_gender(gender)
    return get_bpm_from_speed_stride(mph, avg_stride_ft)


# Get speed (bpm) from height (in) using average stride over height
def get_bpm_from_speed_height(mph, height_in, gender):
    if gender == 'M':
        stride_in = height_in * AVG_STRIDE_OVER_HEIGHT_IN_MAN
    else:
        stride_in = height_in * AVG_STRIDE_OVER_HEIGHT_IN_WOMAN
    stride_ft = stride_in / IN_PER_FT
    return get_bpm_from_speed_stride(mph, stride_ft)


# Return song based on suitable bpm
def rec_song_from_bpm(bpm):
    buffer = 5
    print(bpm)
    filter = {songs.BPM: {"$gte": bpm - buffer, "$lte": bpm + buffer}}
    return dbc.fetch_one(SONGS_COLLECT, filter)


# Return song based on suitable energy
def rec_song_from_exercise(exercise):
    if exercise == "yoga":
        min_val, max_val = YOGA_ENERGY[0], YOGA_ENERGY[1]
    elif exercise == "pilates":
        min_val, max_val = PILATES_ENERGY[0], PILATES_ENERGY[1]
    elif exercise == "cycling":
        min_val, max_val = CYCLING_ENERGY[0], CYCLING_ENERGY[1]
    else:
        min_val, max_val = HEAVIER_ENERGY[0], HEAVIER_ENERGY[1]
    filter = {songs.ENERGY: {"$gte": min_val, "$lte": max_val}}
    return dbc.fetch_one(SONGS_COLLECT, filter)