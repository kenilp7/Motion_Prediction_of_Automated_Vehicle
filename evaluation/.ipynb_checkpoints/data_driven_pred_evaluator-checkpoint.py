import xlsxwriter
import numpy as np

class dataDrivenEvaluation:
    def __init__(self):
        self.selected_data = []
        self.xCenter_gt = list()
        self.yCenter_gt = list()
        self.heading_gt = list()

        self.xCenter_prediction = []
        self.yCenter_prediction =  []
        self.heading_prediction = []

        self.t_raw_Ids = []
        self.t_in_raw = []
        self.t_out_raw = []
        self.min_max_scalar_list = []
        self.y_hat = []
        self.n_predict = 15
        self.row_counter = 1
        self.interim_result = []

    def get_ground_truth(self):
        for idx_ in range(0, len(self.t_out_raw)):
            self.xCenter_gt.append(self.t_out_raw[idx_][0])
            self.yCenter_gt.append(self.t_out_raw[idx_][1])
            self.heading_gt.append(self.t_out_raw[idx_][2])
        return self.xCenter_gt, self.yCenter_gt, self.heading_gt

    def get_prediction(self):
        # gather the predicted future sequences
        for idx_ in range(0, len(self.y_hat)):
            self.xCenter_prediction.append(self.y_hat[idx_, :self.n_predict])
            self.yCenter_prediction.append(self.y_hat[idx_, self.n_predict:2 * self.n_predict])
            self.heading_prediction.append(self.y_hat[idx_, 2 * self.n_predict:3 * self.n_predict])
        
        self.xCenter_prediction = self.min_max_scalar_list[0].inverse_transform(self.xCenter_prediction)
        self.yCenter_prediction = self.min_max_scalar_list[1].inverse_transform(self.yCenter_prediction)
        self.heading_prediction = self.min_max_scalar_list[2].inverse_transform(self.heading_prediction)

        return self.xCenter_prediction, self.yCenter_prediction, self.heading_prediction


    ################# JUST COPIED FROM PREVIOUS #################

    def create_evaluation_workbook(self):
        self.workbook = xlsxwriter.Workbook(self.wb_filename)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, 'recordingId')
        self.worksheet.write(0, 1, 'frame')
        self.worksheet.write(0, 2, 'trackId')
        self.worksheet.write(0, 3, 'xCenterPred')
        self.worksheet.write(0, 3 + self.n_predict, 'yCenterPred')
        self.worksheet.write(0, 3 + 2 * self.n_predict, 'headingPred')
        self.worksheet.write(0, 3 + 3 * self.n_predict, 'xCenterGroundTruth')
        self.worksheet.write(0, 3 + 4 * self.n_predict, 'yCenterGroundTruth')
        self.worksheet.write(0, 3 + 5 * self.n_predict, 'headingGroundTruth')

    def write_to_workbook(self):
        self.create_evaluation_workbook()

        for i in range(len(self.t_in_raw)):
            # store results in excel
            self.interim_result = np.concatenate(([self.t_raw_Ids[i][0][0], self.t_raw_Ids[i][0][2],
                                                    self.t_raw_Ids[i][0][1], ], self.xCenter_prediction[i],
                                                    self.yCenter_prediction[i], self.heading_prediction[i],
                                                    self.xCenter_gt[i], self.yCenter_gt[i], self.heading_gt[i]))
            self.xls_writer()
            self.row_counter += 1
            x = np.array(self.interim_result)[np.newaxis]
        self.workbook.close()

    def xls_writer(self):
        for col_num, data in enumerate(self.interim_result):
            self.worksheet.write(self.row_counter, col_num, data)
