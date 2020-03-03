import os
from flask import current_app
from conf.default import CODEBITS_IMAGE_DIR, DATE_LONG_FORMAT

DATETIME_FORMAT = "%Y_%m_%dT%H-%M"

def delete_images(codebit_id):
    ipath = os.path.join(CODEBITS_IMAGE_DIR, str(codebit_id))
    if not os.path.exists(ipath):
        return

    for file in os.listdir(ipath):
        os.remove(os.path.join(ipath, file))
    os.rmdir(os.path.join(CODEBITS_IMAGE_DIR, str(codebit_id)))

def get_image_paths(codebit_id):
    dir_path = '/'.join([CODEBITS_IMAGE_DIR, str(codebit_id)])
    if os.path.exists(dir_path):
        return ['/'.join([dir_path, ipath]) for ipath in os.listdir(dir_path)]
    else:
        return []

def store_images(codebit_id, image_files):
    ipath = os.path.join(CODEBITS_IMAGE_DIR, str(codebit_id))
    if not os.path.isdir(ipath):
        os.mkdir(ipath)

    image_count = 0
    for key in image_files:
        file = image_files[key]
        file.save(os.path.join(ipath, 'image_%d.%s' % (image_count, file.filename.split('.')[1])))
        image_count += 1


delete_images('5e5de4f0bea72412e9c0f4d2')
