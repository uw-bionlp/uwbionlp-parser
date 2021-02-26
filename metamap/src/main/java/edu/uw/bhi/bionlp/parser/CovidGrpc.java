package edu.uw.bhi.bionlp.parser;

import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;

/**
 * <pre>
 **
 * COVID
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: uwbionlp.proto")
public final class CovidGrpc {

  private CovidGrpc() {}

  public static final String SERVICE_NAME = "uwbionlp.parser.Covid";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput,
      edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput> METHOD_PREDICT =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput, edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "uwbionlp.parser.Covid", "Predict"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput.getDefaultInstance()))
          .setSchemaDescriptor(new CovidMethodDescriptorSupplier("Predict"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static CovidStub newStub(io.grpc.Channel channel) {
    return new CovidStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static CovidBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new CovidBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static CovidFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new CovidFutureStub(channel);
  }

  /**
   * <pre>
   **
   * COVID
   * </pre>
   */
  public static abstract class CovidImplBase implements io.grpc.BindableService {

    /**
     */
    public void predict(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_PREDICT, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_PREDICT,
            asyncUnaryCall(
              new MethodHandlers<
                edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput,
                edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput>(
                  this, METHODID_PREDICT)))
          .build();
    }
  }

  /**
   * <pre>
   **
   * COVID
   * </pre>
   */
  public static final class CovidStub extends io.grpc.stub.AbstractStub<CovidStub> {
    private CovidStub(io.grpc.Channel channel) {
      super(channel);
    }

    private CovidStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected CovidStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new CovidStub(channel, callOptions);
    }

    /**
     */
    public void predict(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_PREDICT, getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   **
   * COVID
   * </pre>
   */
  public static final class CovidBlockingStub extends io.grpc.stub.AbstractStub<CovidBlockingStub> {
    private CovidBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private CovidBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected CovidBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new CovidBlockingStub(channel, callOptions);
    }

    /**
     */
    public edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput predict(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request) {
      return blockingUnaryCall(
          getChannel(), METHOD_PREDICT, getCallOptions(), request);
    }
  }

  /**
   * <pre>
   **
   * COVID
   * </pre>
   */
  public static final class CovidFutureStub extends io.grpc.stub.AbstractStub<CovidFutureStub> {
    private CovidFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private CovidFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected CovidFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new CovidFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput> predict(
        edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_PREDICT, getCallOptions()), request);
    }
  }

  private static final int METHODID_PREDICT = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final CovidImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(CovidImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_PREDICT:
          serviceImpl.predict((edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput) request,
              (io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class CovidBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    CovidBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.parser.Uwbionlp.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Covid");
    }
  }

  private static final class CovidFileDescriptorSupplier
      extends CovidBaseDescriptorSupplier {
    CovidFileDescriptorSupplier() {}
  }

  private static final class CovidMethodDescriptorSupplier
      extends CovidBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    CovidMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (CovidGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new CovidFileDescriptorSupplier())
              .addMethod(METHOD_PREDICT)
              .build();
        }
      }
    }
    return result;
  }
}
