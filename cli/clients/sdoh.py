import grpc
from cli.constants import SDOH
from proto.python.uwbionlp_pb2 import PredictionInput
from proto.python.uwbionlp_pb2_grpc import SdohStub


class SdohPredictorChannelManager():
    def __init__(self, container):
        self.name = SDOH
        self.host = container.host
        self.port = container.port
        self.wait_secs = 30

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self, args):
        return SdohPredictorClient(self.channel, args)

class SdohPredictorClient():
    def __init__(self, channel, args):
        self.name           = SDOH
        self.stub           = SdohStub(channel)
        self.channel        = channel
        self.args           = args

    def process(self, doc):
        response = self.stub.Predict(PredictionInput(id=doc.id, text=doc.text, device=self.args.gpu))
        return response

    def to_dict(self, response):
        output = { 'predictions': [] }
        for pred in response.predictions:
            prediction = { 'type': pred.type, 'arguments': [] }
            for arg in pred.arguments:
                argument = {
                    'charStartIdx': arg.char_start_idx,
                    'charEndIdx': arg.char_end_idx,
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
