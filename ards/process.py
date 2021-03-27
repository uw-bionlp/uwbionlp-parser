import os
import json

from config.constants import DOC_LABELS
from models.model_xray import ModelXray
from layers.pretrained import load_pretrained
from proto.python.uwbionlp_pb2 import PredictionOutput, PredictionEvent, PredictionEventArgument

class DocumentProcessor():

    def __init__(self):
        self.model = load_pretrained(ModelXray, 'model', param_map=None)

    def predict(self, text, device=-1):
        prediction = self.extractor.predict(text, device, 'json')

        # Return Protobuf Result object.
        result = PredictionOutput()

        return result

def val_else_empty_list(val):
    if val: return val
    return []

def val_else_empty_str(val):
    if val: return val
    return ''

def val_else_default_int(val):
    if val != None: return val
    return -1