import xlsxwriter


class physicsBasedEvaluation:
    def __init__(self):
        self.worksheet = None
        self.track_id_counter = None
        self.wb_filename = "prediction.xlsx"
        self.x_center, self.y_center, self.heading = list(), list(), list()
        self.ground_truth = list()
        self.selected_data = list()
        self.track_id = 0
        self.curr_frame = 0
        self.pred_horizon = 0
        self.recording_id = 0
        self.max_num_frames = 0
        self.row_counter = 1
        self.workbook = None
        self.wb_data_list = list()
        self.frame_range = 0
        self.frames_skipped = 0
        self.predicted_data, self.ground_truth_data = list(), list()
        self.interim_result = []

    def get_ground_truth(self):
        max_track_id_counter = 0
        for frame_idx in range(0, self.frame_range, self.frames_skipped):
            start_frame = frame_idx
            end_frame = frame_idx + (self.pred_horizon * self.frames_skipped)

            future_data = self.selected_data[(self.selected_data['frame'] >= start_frame) &
                                           (self.selected_data['frame'] <= end_frame)]
            track_ids = self.selected_data.loc[self.selected_data['frame'] == frame_idx]['trackId']

            self.curr_frame = frame_idx
            for track_id_idx in track_ids:
                self.track_id = track_id_idx
                max_track_id_counter += 1

                # xVelocity
                self.x_center = list(future_data.loc[(future_data['trackId'] == self.track_id) &
                                    (future_data['frame'] > self.curr_frame) & (future_data['frame'] <= self.curr_frame
                                    + (self.pred_horizon * self.frames_skipped)), 'xCenter'])
                # yVelocity
                self.y_center = list(future_data.loc[(future_data['trackId'] == self.track_id) &
                                    (future_data['frame'] > self.curr_frame) & (future_data['frame'] <= self.curr_frame
                                    + (self.pred_horizon * self.frames_skipped)), 'yCenter'])
                # heading
                self.heading = list(future_data.loc[(future_data['trackId'] == self.track_id) &
                                    (future_data['frame'] > self.curr_frame) & (future_data['frame'] <= self.curr_frame
                                    + (self.pred_horizon * self.frames_skipped)), 'heading'])
                self.ground_truth.append(self.x_center + self.y_center + self.heading)
        return self.ground_truth, max_track_id_counter

    def create_evaluation_workbook(self):
        self.workbook = xlsxwriter.Workbook(self.wb_filename)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, 'recordingId')
        self.worksheet.write(0, 1, 'frame')
        self.worksheet.write(0, 2, 'trackId')
        self.worksheet.write(0, 3, 'xCenterPred')
        self.worksheet.write(0, 3 + self.pred_horizon, 'yCenterPred')
        self.worksheet.write(0, 3 + 2 * self.pred_horizon, 'headingPred')
        self.worksheet.write(0, 3 + 3 * self.pred_horizon, 'xCenterGroundTruth')
        self.worksheet.write(0, 3 + 4 * self.pred_horizon, 'yCenterGroundTruth')
        self.worksheet.write(0, 3 + 5 * self.pred_horizon, 'headingGroundTruth')

    def write_to_workbook(self):
        self.create_evaluation_workbook()

        self.track_id_counter = 0
        for frame_idx in range(self.frame_range):
            track_ids = self.selected_data.loc[self.selected_data['frame'] == frame_idx]['trackId']
            for track_id_idx in track_ids:
                self.interim_result = [self.recording_id, frame_idx, track_id_idx,] + \
                                      self.predicted_data[self.track_id_counter] + \
                                      self.ground_truth_data[self.track_id_counter]
                self.xls_writer()
                self.track_id_counter += 1
                self.row_counter += 1
        self.workbook.close()

    def xls_writer(self):
        for col_num, data in enumerate(self.interim_result):
            self.worksheet.write(self.row_counter, col_num, data)

