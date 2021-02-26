import grpc
from cli.constants import METAMAP
from proto.python.uwbionlp_pb2 import MetaMapInput
from proto.python.uwbionlp_pb2_grpc import MetaMapStub

class MetaMapChannelManager():
    def __init__(self, container):
        self.name = METAMAP
        self.host = container.host
        self.port = container.port
        self.wait_secs = 10

    def open(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

    def close(self):
        self.channel.close()

    def generate_client(self, args):
        return MetaMapClient(self.channel, args)

class MetaMapClient():
    def __init__(self, channel, args):
        self.name           = METAMAP
        self.stub           = MetaMapStub(channel)
        self.channel        = channel
        self.args           = args

    def process(self, doc):
        response = self.stub.ExtractNamedEntities(MetaMapInput(id=doc.id, sentences=doc.sentences, semantic_types=self.args.metamap_semantic_types))
        return response

    def to_dict(self, response):
        output = { 'sentences': [], 'errors': [ err for err in response.errors] }
        for sent in response.sentences:
            sentence = { 
                'id': sent.id, 
                'text': sent.text, 
                'concepts': [], 
                'beginCharIndex': sent.begin_char_index,
                'endCharIndex': sent.end_char_index,
            }
            for con in sent.concepts:
                concept = {
                    'beginSentenceCharIndex': con.begin_sent_char_index,
                    'endSentenceCharIndex': con.end_sent_char_index,
                    'beginDocumentCharIndex': con.begin_doc_char_index,
                    'endDocumentCharIndex': con.end_doc_char_index,
                    'cui': con.cui,
                    'semanticTypes': [ st for st in con.semantic_types ],
                    'sourcePhrase': con.source_phrase,
                    'conceptName': con.concept_name,
                    'prediction': con.prediction
                }
                sentence['concepts'].append(concept)
            output['sentences'].append(sentence)
        return output

    def merge(self, base_json, client_json):
        base_json[self.name] = { 'concepts': [], 'errors': client_json['errors'] }
        for sentence in client_json['sentences']:
            for con in sentence['concepts']:
                base_json[self.name]['concepts'].append(con)

        return base_json

    def to_brat(self, client_json):
        t = 1
        brat_rows = []
        for sentence in client_json['sentences']:
            for con in sentence['concepts']:
                row = f"T{t}    {con['prediction']} {con['beginDocumentCharIndex']} {con['endDocumentCharIndex']}    {con['sourcePhrase']}"
                brat_rows.append(row)
                t += 1
        return brat_rows

semantic_types = [
    'aapp',
    'acab',
    'acty',
    'aggp',
    'amas',
    'amph',
    'anab',
    'anim',
    'anst',
    'antb',
    'arch',
    'bacs',
    'bact',
    'bdsu',
    'bdsy',
    'bhvr',
    'biof',
    'bird',
    'blor',
    'bmod',
    'bodm',
    'bpoc',
    'bsoj',
    'celc',
    'celf',
    'cell',
    'cgab',
    'chem',
    'chvf',
    'chvs',
    'clas',
    'clna',
    'clnd',
    'cnce',
    'comd',
    'crbs',
    'diap',
    'dora',
    'drdd',
    'dsyn',
    'edac',
    'eehu',
    'elii',
    'emod',
    'emst',
    'enty',
    'enzy',
    'euka',
    'evnt',
    'famg',
    'ffas',
    'fish',
    'fndg',
    'fngs',
    'food',
    'ftcn',
    'genf',
    'geoa',
    'gngm',
    'gora',
    'grpa',
    'grup',
    'hcpp',
    'hcro',
    'hlca',
    'hops',
    'horm',
    'humn',
    'idcn',
    'imft',
    'inbe',
    'inch',
    'inpo',
    'inpr',
    'irda',
    'lang',
    'lbpr',
    'lbtr',
    'mamm',
    'mbrt',
    'mcha',
    'medd',
    'menp',
    'mnob',
    'mobd',
    'moft',
    'mosq',
    'neop',
    'nnon',
    'npop',
    'nusq',
    'ocac',
    'ocdi',
    'orch',
    'orga',
    'orgf',
    'orgm',
    'orgt',
    'ortf',
    'patf',
    'phob',
    'phpr',
    'phsf',
    'phsu',
    'plnt',
    'podg',
    'popg',
    'prog',
    'pros',
    'qlco',
    'qnco',
    'rcpt',
    'rept',
    'resa',
    'resd',
    'rnlw',
    'sbst',
    'shro',
    'socb',
    'sosy',
    'spco',
    'tisu',
    'tmco',
    'topp',
    'virs',
    'vita',
    'vtbt'
]