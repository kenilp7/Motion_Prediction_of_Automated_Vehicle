from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import math
import numpy as np
import pandas as pd

class preProcess:
    def __init__(self):
        #self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.min_max_scaler_list = [MinMaxScaler(feature_range=(0, 1))] * 13
        self.label_encoder = LabelEncoder()
        self.tracks_data = []                             # Raw tracks data
        self.tracks_data_down_sampled = []  # Down Sampled tracks data
        self.tracks_data_norm = []          # Normalized tracks data
        self.tracks_meta_data = []
        self.data_len = 0
        self.act_sampling_rate = 0.04
        self.frames_skipped = 5
        self.recording_ids = []
        self.act_data_rec_freq = 1/self.act_sampling_rate

    #################################### Down Sampling Data ##################################################

    def get_down_sampled_data(self):
        if not self.data_len:
            self.data_len = len(self.tracks_data)

        tracks_meta_data_merged = pd.DataFrame()
        for id_ in range(self.data_len):
            self.tracks_data[id_] = self.tracks_data[id_].sort_values(["frame", "trackId"], axis = 0, ascending = True)
            max_frame_len = max(self.tracks_data[id_]["frame"])

            # Skipping every nth frame
            for skip_frame_idx in range(0, max_frame_len, self.frames_skipped):
                track_data_subset = self.tracks_data[id_][self.tracks_data[id_]["frame"] == skip_frame_idx]
                self.tracks_data_down_sampled.append(track_data_subset)

            tracks_meta_data_merged = pd.concat([tracks_meta_data_merged, self.tracks_meta_data[id_]], axis=0)

        self.tracks_meta_data = tracks_meta_data_merged

        test_track_data_merged = pd.DataFrame()
        for item in range(len(self.tracks_data_down_sampled)):
            test_track_data_merged = pd.concat([test_track_data_merged, self.tracks_data_down_sampled[item]], axis=0)

        self.tracks_data_down_sampled = test_track_data_merged

        # Resort them back to original format
        self.tracks_data_down_sampled = self.tracks_data_down_sampled.sort_values(["trackId", "frame"], axis=0, ascending=True)
#       self.tracks_data_down_sampled = self.tracks_data_down_sampled.reset_index(drop=True)

        return self.tracks_data_down_sampled, self.tracks_meta_data


#################################### Class Label Encoding ##################################################
    # Converting class labels to integers

    def label_encoding(self):
        if not self.data_len:
            self.data_len = len(self.tracks_data)

        self.label_encoder = LabelEncoder()

        self.tracks_meta= self.tracks_meta_data.assign(classObjEnum=self.label_encoder.fit_transform
                                                                    (self.tracks_meta_data["class"]))

    # To print class labels and their corresponding encoding
    def print_label_encoder_classes(self):
        print("Labels Encoded")
        for id_, item in enumerate(self.label_encoder.classes_):
            print(id_, ":", item)

    #################################### Data Normalization ##################################################

    def normalize_data(self):
        if not self.data_len:
            self.data_len = len(self.tracks_data)

        self.tracks_data_norm = self.tracks_data.copy()
        for item_num, item in enumerate(self.tracks_data.keys()[4:]):
            new_min_max_scalar = MinMaxScaler(feature_range=(0, 1))
            new_min_max_scalar = new_min_max_scalar.fit((self.tracks_data[item].values).
                                                                reshape((len(self.tracks_data[item]), 1)))
            self.tracks_data_norm[item] = (new_min_max_scalar.transform(self.tracks_data[item].values.
                                                                reshape((len(self.tracks_data[item]), 1)))).flatten()
            self.min_max_scaler_list[item_num] = new_min_max_scalar
        return self.tracks_data_norm, self.min_max_scaler_list