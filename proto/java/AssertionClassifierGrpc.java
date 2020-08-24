package edu.uw.bhi.bionlp.covid.parser;

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
 * AssertionClassifier
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: CovidParser.proto")
public final class AssertionClassifierGrpc {

  private AssertionClassifierGrpc() {}

  public static final String SERVICE_NAME = "covid.parser.AssertionClassifier";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput,
      edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput> METHOD_PREDICT_ASSERTION =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput, edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "covid.parser.AssertionClassifier", "PredictAssertion"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput.getDefaultInstance()))
          .setSchemaDescriptor(new AssertionClassifierMethodDescriptorSupplier("PredictAssertion"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static AssertionClassifierStub newStub(io.grpc.Channel channel) {
    return new AssertionClassifierStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static AssertionClassifierBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new AssertionClassifierBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static AssertionClassifierFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new AssertionClassifierFutureStub(channel);
  }

  /**
   * <pre>
   **
   * AssertionClassifier
   * </pre>
   */
  public static abstract class AssertionClassifierImplBase implements io.grpc.BindableService {

    /**
     */
    public void predictAssertion(edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_PREDICT_ASSERTION, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_PREDICT_ASSERTION,
            asyncUnaryCall(
              new MethodHandlers<
                edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput,
                edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput>(
                  this, METHODID_PREDICT_ASSERTION)))
          .build();
    }
  }

  /**
   * <pre>
   **
   * AssertionClassifier
   * </pre>
   */
  public static final class AssertionClassifierStub extends io.grpc.stub.AbstractStub<AssertionClassifierStub> {
    private AssertionClassifierStub(io.grpc.Channel channel) {
      super(channel);
    }

    private AssertionClassifierStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AssertionClassifierStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new AssertionClassifierStub(channel, callOptions);
    }

    /**
     */
    public void predictAssertion(edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_PREDICT_ASSERTION, getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   **
   * AssertionClassifier
   * </pre>
   */
  public static final class AssertionClassifierBlockingStub extends io.grpc.stub.AbstractStub<AssertionClassifierBlockingStub> {
    private AssertionClassifierBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private AssertionClassifierBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AssertionClassifierBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new AssertionClassifierBlockingStub(channel, callOptions);
    }

    /**
     */
    public edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput predictAssertion(edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput request) {
      return blockingUnaryCall(
          getChannel(), METHOD_PREDICT_ASSERTION, getCallOptions(), request);
    }
  }

  /**
   * <pre>
   **
   * AssertionClassifier
   * </pre>
   */
  public static final class AssertionClassifierFutureStub extends io.grpc.stub.AbstractStub<AssertionClassifierFutureStub> {
    private AssertionClassifierFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private AssertionClassifierFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AssertionClassifierFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new AssertionClassifierFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput> predictAssertion(
        edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_PREDICT_ASSERTION, getCallOptions()), request);
    }
  }

  private static final int METHODID_PREDICT_ASSERTION = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AssertionClassifierImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(AssertionClassifierImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_PREDICT_ASSERTION:
          serviceImpl.predictAssertion((edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput) request,
              (io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput>) responseObserver);
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

  private static abstract class AssertionClassifierBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    AssertionClassifierBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.covid.parser.CovidParser.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("AssertionClassifier");
    }
  }

  private static final class AssertionClassifierFileDescriptorSupplier
      extends AssertionClassifierBaseDescriptorSupplier {
    AssertionClassifierFileDescriptorSupplier() {}
  }

  private static final class AssertionClassifierMethodDescriptorSupplier
      extends AssertionClassifierBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    AssertionClassifierMethodDescriptorSupplier(String methodName) {
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
      synchronized (AssertionClassifierGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new AssertionClassifierFileDescriptorSupplier())
              .addMethod(METHOD_PREDICT_ASSERTION)
              .build();
        }
      }
    }
    return result;
  }
}
