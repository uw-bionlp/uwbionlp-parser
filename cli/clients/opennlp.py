import grpc
from cli.constants import OPENNLP
from proto.python.uwbionlp_pb2 import SentenceDetectionInput
from proto.python.uwbionlp_pb2_grpc import OpenNLPStub


class OpenNLPChannelManager():
    def __init__(self, container):
        self.name = OPENNLP
        self.host = container.host
        self.port = container.port
        self.wait_secs = 2

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self):
        return OpenNLPClient(self.channel)

class OpenNLPClient():
    def __init__(self, channel):
        self.name    = OPENNLP
        self.stub    = OpenNLPStub(channel)
        self.channel = channel

    def process(self, doc_id, text):
        response = self.stub.DetectSentences(SentenceDetectionInput(id=doc_id, text=text))
        for error in response.errors:
            print(error)
        return response

    def to_dict(self, response):
        output = { 'id': response.id, 'sentences': [], 'text': response.text }
        for sent in response.sentences:
            sentence = { 
                'id': sent.id, 
                'text': sent.text, 
                'beginCharIndex': sent.begin_char_index,
                'endCharIndex': sent.end_char_index,
            }
            output['sentences'].append(sentence)
        return output