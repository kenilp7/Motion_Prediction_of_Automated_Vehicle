from animate_plot import animateClass

# TURN OFF plots in tool windows
# Settings => Tools => Python Scientific => unmark 'Show plots in tool windows'


if __name__ == '__main__':
    pred_horizon = 3
    plot_xaxis_limits = [0, 20]
    plot_yaxis_limits = [0, 20]

    car_x = [*range(0, 20, 1)]
    car_y = [*range(0, 20, 1)]
    car_position = list(zip(car_x, car_y))

    car_position_pred = list(
        zip([*range(pred_horizon, (20 + pred_horizon), 1)], [*range(pred_horizon, (20 + pred_horizon), 1)]))

    obst_x = [*range(0, 20, 1)]
    obst_y = [*range(20, 0, -1)]
    obstacle_position = list(zip(obst_x, obst_y))
    obstacle_position_pred = list(
        zip([*range(pred_horizon, (20 + pred_horizon), 1)], [*range((20 - pred_horizon), -pred_horizon, -1)]))

    num_obstacles = 1

    animate_obj = animateClass(car_position, car_position_pred, num_obstacles, obstacle_position,
                               obstacle_position_pred)
    animate_obj.frame_num = 20
    animate_obj.frame_interval = 300
    animate_obj.plot_xaxis_limits = plot_xaxis_limits
    animate_obj.plot_yaxis_limits = plot_xaxis_limits
    animate_obj.prediction_horizon = pred_horizon

    animate_obj.animate_function()
