import os
import json

from docker.extractor import Extractor
from proto.python.uwbionlp_pb2 import PredictionOutput, PredictionEvent, PredictionEventArgument

class DocumentProcessor():

    def __init__(self):
        self.model_dir      = os.path.join('model','sdoh')
        self.word_embed_dir = os.path.join('model','word2vec')
        self.extractor      = Extractor('sdoh', self.model_dir, self.word_embed_dir)

    def predict(self, text, device=-1):
        if not len(text.strip()):
            prediction = []
        else:
            prediction = self.extractor.predict(text, device, 'json')

        # Return Protobuf Result object.
        result = PredictionOutput()
        for ev in prediction:
            pred_ev = PredictionEvent()
            pred_ev.type = val_else_empty_str(ev['type'])
            for arg in ev['arguments']:
                pred_arg = PredictionEventArgument()
                pred_arg.char_start_idx = arg['indices'][0] if arg['indices'] else -1
                pred_arg.char_end_idx = arg['indices'][1] if arg['indices'] else -1
                pred_arg.label = val_else_empty_str(arg['label'])
                pred_arg.text = val_else_empty_str(arg['text'])
                pred_arg.type = val_else_empty_str(arg['type'])
                pred_ev.arguments.append(pred_arg)
            result.predictions.append(pred_ev)

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