
from . import BaseObject

class Image(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "imageID"},
        "description": {"type": str, "ls_field": "description"},
        "filename": {"type": str, "ls_field": "filename"},
        "order": {"type": int, "ls_field": "ordering"},
        "public_image_id": {"type": str, "ls_field": "publicID"},
        "item": {"type": 'Item', "ls_field": "Item", "ls_field_id": "itemID", "relationships": ["Item"]},
        "item_matrix": {"type": 'ItemMatrix', "ls_field": "ItemMatrix", "ls_field_id": "itemMatrixID", "relationships": ["ItemMatrix"]},
    }

    # TODO: build API that can upload images
    # TODO: build function that can download images (with settings for height/width/scale/etc.)