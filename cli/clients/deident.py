import grpc
from cli.constants import DEIDENT
from proto.python.uwbionlp_pb2 import PredictionInput
from proto.python.uwbionlp_pb2_grpc import DeidentificationStub


class DeidentificationChannelManager():
    def __init__(self, container):
        self.name = DEIDENT
        self.host = container.host
        self.port = container.port
        self.wait_secs = 30

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self, args):
        return DeidentificationClient(self.channel, args)

class DeidentificationClient():
    def __init__(self, channel, args):
        self.name           = DEIDENT
        self.stub           = DeidentificationStub(channel)
        self.channel        = channel
        self.args           = args

    def process(self, doc):
        response = self.stub.Deidentify(PredictionInput(id=doc.id, text=doc.text, device=self.args.gpu))
        return response

    def to_dict(self, response):
        output = { 'named_entities': [], 'deidentText': response.deident_text }
        for ent in response.named_entities:
            entity = {   
                'charStartIdx': ent.char_start_idx,
                'charEndIdx': ent.char_end_idx,
                'label': ent.label,
                'text': ent.text,
                'type': ent.type
            }
            output['named_entities'].append(entity)
        return output

    def merge(self, base_json, client_json):
        base_json[self.name] = client_json
        return base_json
