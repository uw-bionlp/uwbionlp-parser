import grpc
from cli.utils import get_containers, get_env_var
from cli.constants import ASSERTION_CLASSIFIER
from proto.python.uwbionlp_pb2 import AssertionClassifierInput, AssertionClassifierOutput
from proto.python.uwbionlp_pb2_grpc import AssertionClassifierStub

def get_assertion_classifier_containers():
    return [ container for key, container in get_containers().items() if ASSERTION_CLASSIFIER in container.name ]

class AssertionClassifierChannelManager():
    def __init__(self):
        self.name = 'assertion_classifier'
        self.host = '0.0.0.0'
        self.port = get_env_var('ASRTCLA_PORT')

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self):
        return AssertionClassifierClient(self.channel)

class AssertionClassifierClient():
    def __init__(self, channel):
        self.name    = 'assertion_classifier'
        self.stub    = AssertionClassifierStub(channel)
        self.channel = channel

    def process(self, text, start_char_index, end_char_index):
        response = self.stub.PredictAssertion(AssertionClassifierInput(text=text, start_char_index=start_char_index, end_char_index=end_char_index))
        return response.prediction