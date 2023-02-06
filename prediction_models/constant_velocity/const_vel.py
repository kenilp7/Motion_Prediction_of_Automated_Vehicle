import numpy as np


#################################### Main Model Function ##################################################

def my_constant_vel_model(test_data, pred_horizon, samp_time, frame_range):
    prediction = list()
    for frame_idx in range(frame_range):
        start_frame = frame_idx
        end_frame = frame_idx + pred_horizon
        pred_data = test_data[test_data['frame'] <= frame_idx]

        track_ids = test_data.loc[test_data['frame'] == frame_idx]['trackId']

        for track_id_idx in track_ids:
            prediction.append(my_prediction(pred_data, frame_idx, track_id_idx, pred_horizon, samp_time))

    return prediction


#################################### Predict Function ##################################################

def my_prediction(predData, currFrame, trackID, predHorizon, samplingTime):
    # xCenter prediction
    xVelInit = float(predData.loc[(predData['frame'] == currFrame) &
                                  (predData['trackId'] == trackID), 'xVelocity'])
    xCenterInit = float(predData.loc[(predData['frame'] == currFrame) &
                                     (predData['trackId'] == trackID), 'xCenter'])
    x0 = np.ones(predHorizon) * xCenterInit
    a = np.arange(1, predHorizon + 1, 1)
    b = np.identity(predHorizon) * xVelInit * samplingTime
    xCenter = list(x0 + np.matmul(a, b))
    # yCenter prediction
    yVelInit = float(predData.loc[(predData['frame'] == currFrame) &
                                  (predData['trackId'] == trackID), 'yVelocity'])
    yCenterInit = float(predData.loc[(predData['frame'] == currFrame) &
                                     (predData['trackId'] == trackID), 'yCenter'])
    y0 = np.ones(predHorizon) * yCenterInit
    b = np.identity(predHorizon) * yVelInit * samplingTime
    yCenter = list(y0 + np.matmul(a, b))
    # heading prediction
    heading = list(predData.loc[(predData['frame'] == currFrame) &
                                (predData['trackId'] == trackID), 'heading']) * predHorizon

    prediction = xCenter + yCenter + heading

    return prediction
