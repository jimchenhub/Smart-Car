# Smart Car
We plan to make a smart car which can avoid obstacles automatically by using image processing and machine learning skills.

## Core technique
* OpenCV for image processing
* Convolutional Neural Network for machine learning
* Raspberry PI et al for hardware design

## Divectory structure
 
    ├── document                   - All the document are placed here. (Progess reports and some introduction document) 
    ├── source                     - All source codes
    │   ├── component              - Some common component for car running and learning.
    │   ├── config                 - Configuration about car. Also store weights and biases of network, etc. 
    │   ├── implementation         - Code for car's normal movement   
    │   ├── test                   - Test code for move accuracy 
    │   └── training               - Training code 
    └── README.md                  - Some explanation for Smart Car project 
