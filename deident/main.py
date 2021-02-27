import os
import sys
import grpc
from concurrent import futures

from proto.python.uwbionlp_pb2_grpc import DeidentificationServicer as BaseDeidentificationServicer, add_DeidentificationServicer_to_server
from process import DocumentProcessor

# This one is rather odd - the TF dataset was pickled with
# a custom class, 'dataset', and that can't be found when unpickling unless
# /nn modules are visible to the interpreter (/nn/dataset.py in this case), 
# so we do so here.
sys.path.append(os.path.join(os.getcwd(), 'nn'))

class DeidentificationServicer(BaseDeidentificationServicer):

    def __init__(self):
        self.processor = DocumentProcessor()

    def Deidentify(self, request, context):

        # Process document.
        prediction = self.processor.predict(request.text)
        prediction.id = request.id

        return prediction

server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
add_DeidentificationServicer_to_server(DeidentificationServicer(), server)
server.add_insecure_port('[::]:8080')
server.start()
server.wait_for_termination()

# docker build -t uwbionlp-parser-deident -f deident/Dockerfile deident
# docker run -d --name uwbionlp-parser-deident -p 8080:8080 uwbionlp-parser-deident