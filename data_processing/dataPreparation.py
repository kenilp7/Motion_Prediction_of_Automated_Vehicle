from numpy import round
from numpy import hstack
import numpy as np
from sklearn.model_selection import train_test_split
from IPython.display import clear_output
import pickle

class dataPrepare:
    def __init__(self):
        self.num_past = 20  # Default values
        self.num_predict = 15  # Default values
        self.sequences = []
        self.splitted_Ids = []
        self.splitted_X = []
        self.splitted_Y = []
        self.tracks_data = []  # Raw tracks data
        self.tracks_data_norm = []  # Data should come from preProcessing
        self.tracksMeta_data = []  # Data should come from readDataset
        self.data_stacking_input = []  # Assigned to either raw data or normalized data
        self.data_len = 0
        self.data_input = ""

        self.xTrain_data = []
        self.xTest_data = []
        self.yTrain_data = []
        self.yTest_data = []
        self.test_size = 0.2  # Default value
        self.random_state = 0  # Default value
        self.track_id_range = 1

    #################################### Data Splitting ##################################################
    # Split a multivariate sequence into samples
    def split_sequences(self):
        for id_ in range(len(self.sequences)):
            # find the end of this pattern
            end_index = id_ + self.num_past
            out_end_index = end_index + self.num_predict
            # check if we are beyond the dataset
            if out_end_index > len(self.sequences):
                break
            # gather input and output parts of the pattern
            seq_Ids, seq_x, seq_y = self.sequences[id_:end_index, 0:3], \
                                    self.sequences[id_:end_index, 3:-3], \
                                    [self.sequences[end_index:out_end_index, -3],
                                     self.sequences[end_index:out_end_index, -2],
                                     self.sequences[end_index:out_end_index, -1]]
            self.splitted_Ids.append(seq_Ids)
            self.splitted_X.append(seq_x)
            self.splitted_Y.append(seq_y)
        #     #################################### Stack Data ##################################################

    def data_stacking(self):
        print("This might take a while!")
        new_array = []

        if self.data_input == "raw_data":
            self.data_stacking_input = self.tracks_data
        elif self.data_input == "normalized_data":
            self.data_stacking_input = self.tracks_data_norm

        new_array = np.where(np.roll(self.data_stacking_input['trackId'][1:], 1) != self.data_stacking_input['trackId'][1:])[0]

        for x in range(self.track_id_range):  # loop through the selected number of trackIds
            #clear_output(wait=True)

            recordingId_sequence = self.data_stacking_input.recordingId[new_array[x]:new_array[x + 1]]
            recordingId_sequence = recordingId_sequence.values.reshape((len(recordingId_sequence), 1))

            track_Id_sequence = self.data_stacking_input.trackId[new_array[x]:new_array[x + 1]]
            track_Id_sequence = track_Id_sequence.values.reshape((len(track_Id_sequence), 1))

            frame_sequence = self.data_stacking_input.frame[new_array[x]:new_array[x + 1]]
            frame_sequence = frame_sequence.values.reshape((len(frame_sequence), 1))

            lonVel_sequence = self.data_stacking_input.lonVelocity[new_array[x]:new_array[x + 1]]
            lonVel_sequence = lonVel_sequence.values.reshape((len(lonVel_sequence), 1))

            xCenter_sequence = self.data_stacking_input.xCenter[new_array[x]:new_array[x + 1]]
            xCenter_sequence = xCenter_sequence.values.reshape((len(xCenter_sequence), 1))

            yCenter_sequence = self.data_stacking_input.yCenter[new_array[x]:new_array[x + 1]]
            yCenter_sequence = yCenter_sequence.values.reshape((len(yCenter_sequence), 1))

            heading_sequence = self.data_stacking_input.heading[new_array[x]:new_array[x + 1]]
            heading_sequence = heading_sequence.values.reshape((len(heading_sequence), 1))

            self.sequences = hstack((recordingId_sequence, track_Id_sequence, frame_sequence, xCenter_sequence,
                                     yCenter_sequence, heading_sequence, lonVel_sequence, xCenter_sequence,
                                     yCenter_sequence, heading_sequence))

            self.split_sequences()

            if self.track_id_range > 1:
                print("Current progress:", round((x / (self.track_id_range-1)) * 100, 2), "%")

        print("Done! ")
        return self.splitted_Ids, self.splitted_X, self.splitted_Y

    #################################### Train Test Data #################################################
    # Splitting the data into training and validation
    def get_test_train_split(self):
        self.data_stacking()

        self.xTrain_data, self.xTest_data, self.yTrain_data, self.yTest_data = \
            train_test_split(self.splitted_X, self.splitted_Y, test_size=self.test_size, random_state=self.random_state)

        return self.xTrain_data, self.xTest_data, self.yTrain_data, self.yTest_data

    #################################### Save in a pickel format #################################################
    # Save the xTrain, xTest, yTrain, xTest in pickle format
    def save_test_train_data_pickle(self):
        if not self.xTrain_data and self.xTest_data and self.yTrain_data and self.yTest_data:
            print("Train and Test data missing!")
        else:
            # save train and test data in a single pickle file
            with open('train_test.pickle', 'wb') as train_test_file:
                pickle.dump([self.xTrain_data, self.xTest_data, self.yTrain_data, self.yTest_data], train_test_file)

    ####################################  Reload from a pickel format ###########################################
    # Load the xTrain, xTest, yTrain, xTest from a pickle format
    def load_test_train_data_pickle(self):
        # reload saved train and test data pickle file
        with open('train_test.pickle', 'rb') as train_test_file:
            self.xTrain_data, self.xTest_data, self.yTrain_data, self.yTest_data = pickle.load(train_test_file)
        return self.xTrain_data, self.xTest_data, self.yTrain_data, self.yTest_data
