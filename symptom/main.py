import grpc
from concurrent import futures
from proto.python.uwbionlp_pb2_grpc import SymptomServicer as BaseSymptomServicer, add_SymptomServicer_to_server
from process import DocumentProcessor

class SymptomServicer(BaseSymptomServicer):

    def __init__(self):
        self.processor = DocumentProcessor()

    def Predict(self, request, context):

        # Process document.
        prediction = self.processor.predict(request, request.device)
        prediction.id = request.id

        return prediction

server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
add_SymptomServicer_to_server(SymptomServicer(), server)
server.add_insecure_port('[::]:8080')
server.start()
server.wait_for_termination()


# docker build -t uwbionlp-symptom -f symptom/Dockerfile symptom
# docker run -d --name uwbionlp-symptom -p 8080:8080 uwbionlp-symptom