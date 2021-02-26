from concurrent import futures

import grpc
import json

from proto.python.uwbionlp_pb2_grpc import SdohServicer as BaseSdohServicer, add_SdohServicer_to_server

from process import DocumentProcessor

class SdohServicer(BaseSdohServicer):

    def __init__(self):
        self.processor = DocumentProcessor()

    def Predict(self, request, context):

        # Process document.
        prediction = self.processor.predict(request.text, request.device)
        prediction.id = request.id

        return prediction

server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
add_SdohServicer_to_server(SdohServicer(), server)
server.add_insecure_port('[::]:8080')
server.start()
server.wait_for_termination()


# docker build -t uwbionlp-sdoh -f sdoh/Dockerfile sdoh
# docker run -d --name uwbionlp-sdoh -p 8080:8080 uwbionlp-sdoh