
from os.path import exists

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


class dataGrabber:
    def __init__(self, csv_path):
        self.road_png_image = None
        self.dataset_path = csv_path
        self.location_id = []
        self.recording_id = []
        self.tracks_file_names = []
        self.tracksMeta_file_names = []
        self.recordingMeta_file_names = []
        self.tracks_data = []
        self.tracks_meta = []
        self.recording_meta = []
        self.file_exists_check = False
        self.read_via_loc_id = False
        self.max_track_id = 0           # Maximum number of objects in the scenario
        self.max_record_id = 32         # Maximum number of record id
        # Recording location and mapping
        self.location_recording_dict = {"1": [*range(7, 18, 1)],
                                        "2": [*range(18, 30, 1)],
                                        "3": [*range(30, 33, 1)],
                                        "4": [*range(0, 7, 1)]}

    ######################################## Read csv files ##########################################
    def read_csv_files(self):
        for item in range(len(self.tracks_file_names)):
            self.file_exists_check = exists(self.tracks_file_names[item]) \
                                     and exists(self.tracksMeta_file_names[item]) \
                                     and exists(self.recordingMeta_file_names[item])
            if not self.file_exists_check:
                print("CSV Files Missing or File Names Changed..!")
            else:
                self.tracks_data.append(pd.read_csv(self.tracks_file_names[item]))
                self.tracks_meta.append(pd.read_csv(self.tracksMeta_file_names[item]))
                self.recording_meta.append(pd.read_csv(self.recordingMeta_file_names[item]))

    def update_csv_file_names(self):
        # updating csv filenames
        if self.read_via_loc_id:
            for id_set in self.recording_id:
                for item in id_set:
                    self.tracks_file_names.append(self.dataset_path + str(item) + '' + "_tracks.csv")
                    self.tracksMeta_file_names.append(self.dataset_path + str(item) + "_tracksMeta.csv")
                    self.recordingMeta_file_names.append(self.dataset_path + str(item) + "_recordingMeta.csv")
        else:
            for item in self.recording_id:
                self.tracks_file_names.append(self.dataset_path + str(item) + '' + "_tracks.csv")
                self.tracksMeta_file_names.append(self.dataset_path + str(item) + "_tracksMeta.csv")
                self.recordingMeta_file_names.append(self.dataset_path + str(item) + "_recordingMeta.csv")

        # Consider only the unique items in the list
        self.tracks_file_names = list(set(self.tracks_file_names))
        self.tracksMeta_file_names = list(set(self.tracksMeta_file_names))
        self.recordingMeta_file_names = list(set(self.recordingMeta_file_names))

        # Sorting list in ascending order
        self.tracks_file_names.sort()
        self.tracksMeta_file_names.sort()
        self.recordingMeta_file_names.sort()

    #################################### Read csv fn called from Main file ##################################

    # Read CSV files if selected list is given as location ID ###
    def read_csv_with_location(self):
        self.read_via_loc_id = True
        self.update_recording_id()
        self.rename_recording_id()
        self.update_csv_file_names()
        self.read_csv_files()

    # Read CSV files if selected list is given as recording ID ###
    def read_csv_with_recordingID(self):
        self.read_via_loc_id = False
        self.update_location_id()
        self.rename_recording_id()
        self.update_csv_file_names()
        self.read_csv_files()

    #################################### Return CSV data ##################################################

    def get_tracks_data(self):
        return self.tracks_data

    def get_tracksMeta_data(self):
        return self.tracks_meta

    def get_recordingMeta_data(self):
        return self.recording_meta

    #################################### Updating Location and Recording ID #################################

    # Update location ID if the csv list is requested via recording ID
    def update_location_id(self):
        for item in self.recording_id:
            if int(item) <= self.max_record_id:
                for record_id in self.location_recording_dict.keys():
                    if int(item) in self.location_recording_dict[record_id]:
                        self.location_id.append(record_id)
            else:
                print(f'Error: Invalid Recording ID: {item}')
                print("Other Recording IDs added!")
            self.location_id = list(set(self.location_id))

    # Update recording ID if the csv list is requested via location ID
    def update_recording_id(self):
        for loc in self.location_id:
            if loc in self.location_recording_dict.keys():
                self.recording_id.append(self.location_recording_dict[loc])
            else:
                print(f'Error: Invalid Location ID: {loc}')
                print("Other location IDs added!")

    # Renaming recording ID
    def rename_recording_id(self):
        if self.read_via_loc_id:
            # if csv reading is initiated via location ID
            record_id_temp = [[]] * len(self.recording_id)
            for id_ in range(len(self.recording_id)):
                for item in range(len(self.recording_id[id_])):
                    if self.recording_id[id_][item] < 10:
                        record_id_temp[id_].append('0' + str(self.recording_id[id_][item]))
                    else:
                        record_id_temp[id_].append(str(self.recording_id[id_][item]))
            self.recording_id = record_id_temp
        else:
            # if csv reading is initiated via record ID
            for item in range(len(self.recording_id)):
                if int(self.recording_id[item]) < 10:
                    self.recording_id[item] = '0' + str(self.recording_id[item])

    ######################################### Miscellanious Functions ########################################
    def print_field_names(self):
        print('Tracks Data: ' + ', '.join(field for field in self.tracks_data))
        print('Tracks Meta: ' + ', '.join(field for field in self.tracks_meta))
        print('Recording Meta: ' + ', '.join(field for field in self.recording_meta))

    def plot_background_png(self):
        # Plot the PNG Image
        self.road_png_image = self.dataset_path + str(self.recording_id) + '_background.png'
        road_img = mpimg.imread(self.road_png_image)
        plt.imshow(road_img)
        plt.show()

    def get_object_class(self, track_id):
        # Print Object Class
        print('Object Class: ' + self.tracks_meta["class"][self.tracks_meta["trackId"] == track_id][track_id])
