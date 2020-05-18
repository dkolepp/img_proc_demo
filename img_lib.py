import os
import logging
import csv
import numpy as np
import cv2
from imageai.Detection import ObjectDetection

LOGGER = logging.getLogger(__name__)
THIS_DIR = os.path.dirname(__file__)

model = os.path.join(THIS_DIR, "yolo.h5")
detector = None

def initialize():
    global detector
    LOGGER.info("Creating Object Detector")
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model)
    LOGGER.info("Object Detector created")


    LOGGER.info("Loading model: %s", model)
    detector.loadModel()
    LOGGER.info("Model loaded")
####

def get_out_file(fullname):
    if not detector:
        initialize()
    ####
    fname = os.path.basename(fullname)

    reldir = os.path.dirname(fullname)
    output_dir = reldir
    cat_dir = os.path.join(output_dir, 'processed')
    if not os.path.exists(cat_dir):
        os.mkdir(cat_dir)
    ####
    return os.path.join(cat_dir, fname)
####


def process_file(fname):
    fullname = os.path.realpath(fname)
    basename = os.path.basename(fullname)
    outfile = get_out_file(fullname)
    outfile_csv = os.path.splitext(outfile)[0] + ".txt"

    LOGGER.info("Processing file: %s", fullname)

    detections = detector.detectObjectsFromImage(
        input_image=fullname,
        output_image_path=outfile,
        minimum_percentage_probability=30)

    objectsFound=[]
    headers=["filename","object_type","probability","x0","y0","x1","y1"]
    for eachObject in detections:
        record = {
            headers[0]: basename,
            headers[1]: eachObject["name"],
            headers[2]: eachObject["percentage_probability"],
            headers[3]: eachObject["box_points"][0],
            headers[4]: eachObject["box_points"][1],
            headers[5]: eachObject["box_points"][2],
            headers[6]: eachObject["box_points"][3]
        }
        objectsFound.append(record)
        LOGGER.info("%s", record)


    if len(objectsFound) > 0:
        LOGGER.info("Writing CSV file: %s", outfile_csv)
        with open(outfile_csv, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, headers)
            #csvwriter.writeheader()
            csvwriter.writerows(objectsFound)
    else:
        LOGGER.info("No object detections for: %s", fullname)

####


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    for item in sys.argv[1:]:
        process_file(sys.argv[1])
