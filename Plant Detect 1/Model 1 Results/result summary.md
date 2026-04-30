## Layout
- The first row shows the results of the model training and how it progressed with each iteration.
- The second row shows results for model validation. 

## Training Graph Descriptions
- **train/box_loss**– Measures how accurately the predicted bounding boxes match the actual object locations. Lower values indicate better localization performance.
- **train/cls_loss** – Measures how accurately the model predicts the correct vegetation class labels. Lower values indicate improved classification accuracy.
- **train/dfl_loss**– Distribution Focal Loss; helps the model more precisely predict bounding box boundaries. The gradual decrease shows improvement in localization accuracy over training.
- **metrics/precision(B)** – Measures how often detected objects are classified correctly. Higher precision means fewer false detections. The model reaches values around 0.7.
- **metrics/recall(B)** – Measures how many actual objects in the images are successfully detected by the model. Recall improves from about 0.2 to 0.7 throughout training.

## Testing Graph Descriptions
- **val/box_loss** – Validation version of box loss. The final value stabilizes around 1.55, indicating moderate localization accuracy on unseen images.
- **val/cls_loss** – Validation classification loss. The graph is initially noisy but becomes more stable over time, suggesting improving generalization.
- **val/dfl_loss**– Validation Distribution Focal Loss. Similar to the classification loss, it shows early instability before stabilizing later in training.
- **metrics/mAP50(B)**– Mean Average Precision at 50%. A prediction is considered correct if the predicted and actual bounding boxes overlap by at least 50%.
- **metrics/mAP50-95(B)** – A stricter version of mAP measured across overlap thresholds from 50% to 95%. Higher values indicate more precise object localization and detection accuracy.

##Other Graphs
- **Box FI** - Helps determine whether the model is balanced, whether it misses vegetation too often, and whether it creates too many false detections A smoother, higher F1 curve usually means better dataset quality, more stable training and better generalization.
- **Box PR** - Precision-Recall curve for object detection. It shows the relationship between precision and recall at different confidence thresholds. A curve closer to the top-right corner indicates better overall detection performance.
- **Box P** - Precision curve. Shows how precision changes as the confidence threshold changes. Higher precision means the model produces fewer false positive detections.
- **Box R **- Recall curve. Shows how recall changes with different confidence thresholds. Higher recall means the model successfully detects more actual objects in the images.
- **Confusion matrix **- A table that compares predicted classes with actual classes. It shows how often each vegetation category was correctly classified and where misclassifications occurred. Values along the diagonal represent correct predictions, while off-diagonal values represent classification errors between classes.

## Summary
* Overall, we see significant improvements in box loss, classification loss and DFL loss, meaning that the model is able to accurately create bounding boxes on detected vegetation'
* The results for box, cls and dfl loss in the validation images are worse than in training. This can be improved with a larger dataset and maybe more cycles of training. 

