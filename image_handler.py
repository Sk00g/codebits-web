import os
from flask import current_app
from conf.default import CODEBITS_IMAGE_DIR


def get_image_paths(codebit_data):
    return [os.path.join(CODEBITS_IMAGE_DIR, ipath) for ipath in codebit_data['images']]

def store_images(codebit_id, image_files):
    pass



