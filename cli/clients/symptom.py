import grpc
from cli.constants import SYMPTOM
from proto.python.uwbionlp_pb2 import PredictionInput
from proto.python.uwbionlp_pb2_grpc import SymptomStub


class SymptomPredictorChannelManager():
    def __init__(self, container):
        self.name = SYMPTOM
        self.host = container.host
        self.port = container.port
        self.wait_secs = 30

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self, args):
        return SymptomPredictorClient(self.channel, args)

class SymptomPredictorClient():
    def __init__(self, channel, args):
        self.name           = SYMPTOM
        self.stub           = SymptomStub(channel)
        self.channel        = channel
        self.args           = args

    def process(self, doc):
        response = self.stub.Predict(PredictionInput(id=doc.id, text=doc.text, sentences=doc.sentences, device=self.args.gpu))
        return response

    def to_dict(self, response):
        output = { 'predictions': [] }
        for pred in response.predictions:
            prediction = { 
                'type': pred.type, 
                'arguments': [],
                'tokStartIdx': pred.arguments[0].char_start_idx,
                'tokEndIdx': pred.arguments[0].char_end_idx,
                'text': pred.arguments[0].text
            }

            for i, arg in enumerate(pred.arguments):
                if i == 0: continue
                argument = {
                    'tokStartIdx': arg.char_start_idx,
                    'tokEndIdx': arg.char_end_idx,
                    'text': arg.text,
                    'type': arg.type,
                    'label': arg.label
                }
                prediction['arguments'].append(argument)
            output['predictions'].append(prediction)
        return output

    def merge(self, base_json, client_json):
        base_json[self.name] = client_json
        return base_json
