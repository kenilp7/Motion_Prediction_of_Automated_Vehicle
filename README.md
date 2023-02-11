
# Motion Prediction of Automated Vehicle

### Goal of Motion Prediction

It aims to forecast the upcoming headings, velocities, and positions of moving objects in the surrounding environment over a limited time. The expected trajectories also help us to ensure that the ego vehicle's planned path won't collide with any other objects in the future.

image slide 1-5

<img src="https://user-images.githubusercontent.com/108230926/218283884-c539a167-efcc-454c-82e8-0e645784d08c.png" width="250" height="250">

-- The goal of this project is to forecast the trajectory of an ego vehicle depending on the objects in its immediate environment such as cars, pedestrians, motorbikes or bicycles.

- **Libraries** - Numpy, Tensorflow, PyTorch, Scikit learn, Pandas, MatplotLib, Plotly

- **Language** - Python

### Dataset used -  [inD Dataset](https://www.ind-dataset.com/)

 - The drone recorded the road users' naturalistic behavior at 4 different German intersections over a certain period of time. 

 - 33 Recordings at four different recording locations

- One recording is ~ 15 minutes

 - The dataset included more than 13,500 objects such as vehicles, bikes, and pedestrians at junctions in the following [format](https://www.ind-dataset.com/format).

images of junctions

### Types of Motion Prediciton algorithm

Image slide 9

For the project, the interaction aware motion model was used which consisted of neural network architecture.

### Neural Network-Based Motion Prediction

- **Data Normalization**
image 1-12

- **Splitting Train-Test data**
image1-16

- **Training the neural network model**
image 1-17

- **Testing the model using test data**

### Our Approach

Image 21

### Our Neural Network Model Architecture
image 21

### Result

image 24

- The validation (test) dataset line is stable after 40 epochs
- The prediction of test dataset (unseen) will be close to accurate

--> The average displacement error (average Euclidean distance between the position prediction and ground truth) is found to be 0.9 m

--> The average absolute heading error (average absolute deviation of the heading of the ego vehicle from the ground truth value) is 3.62 degrees

### Future Scope

- Using ConvLSTM as it captures the spatio temporal features simultaneously throughout the model.
- Graph neural networks (GNNs) show the promising results using attention mechanism.
- One aspect that can be considered while collecting data is the usage of vehicle auditory data like horn and other visual data like signalling lights for inferring the future behavior of the vehicle.
