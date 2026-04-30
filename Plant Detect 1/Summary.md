## General
- Most information about the steps in the training process are found in the Train_YOLO_Models_mine file.
- Combining datasets from different sources? Can we use regular vegetation images to help the model identify vegetation?
- You can run the Train_YOLO_Models...ipynb file to get all outputs and run locally

More photos
https://www.pexels.com/search/train%20tracks%20with%20vegetation/

- YOLO --> High speed computer vision algorithm used to detect and classify objects in images and videos. 
1. The algorithm divides an image into a grid. 
2. Each grid cell acts simultaneously, predicting bounding boxes and class probabilities for objects, which allows for fast, end-to-end detection.
- Deployment on drone needs a mobile computer/processor. Analysis of drone video footage externally/on laptop would not need any additional components. 

## Steps Taken
1. I labeled the dataset using Label Studio, following this tutorial -- https://youtu.be/r0RspiLG260. 
- I labeled the train track region using 1 big bounding box. 
- I labeled various vegetation levels -- no vegetation (just track photos), some vegetation, heavy vegetation. I included the track shape outline photos as well. 

2. I trained the YOLO model using the code in the tutorial in step 1. Results are in the 'val_batch0_pred.jpg' file in the Model 1 Training and Prediction folder.
- Graphs of testing metrics are in Model 1 Results --> results.png.  A summary/description of these is found in Model 1 Results --> Result Description 
- The training/testing photos with bounding boxes applied are found in the Model 1 Training and Prediction folder. 

3. I exported the trained YOLO model to my laptop (you can find it in (Plant Detect 1/Model 1). 
- Got a test video (https://www.pexels.com/video/a-train-tracks-with-a-power-line-and-grass-27315436/)
- I tested this model on Test video --> seemed okay. Can detect some vegetation. 
- I expected it to detect the vegetation on the tracks but it couldn't. It mostly detected large plants outside of track area. 
- May be because of the small dataset size, or because I also labeled the plants outside of the track boundaries? 
- Maybe I should make new model without including the track outline photos. 
