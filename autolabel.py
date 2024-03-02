from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM
import os
ontology = CaptionOntology({
    "red square" : None
})

CURRENT_DIR = os.getcwd()
DATASET_DIR_PATH = os.path.join(CURRENT_DIR, "dataset_test")
os.makedirs(DATASET_DIR_PATH, exist_ok = True)
os.makedirs(DATASET_DIR_PATH, exist_ok = True)

# run base model.
base_model = GroundedSAM(ontology=ontology)
dataset = base_model.label(
    input_folder="images_test/",
    extension=".png",
    output_folder=DATASET_DIR_PATH)


