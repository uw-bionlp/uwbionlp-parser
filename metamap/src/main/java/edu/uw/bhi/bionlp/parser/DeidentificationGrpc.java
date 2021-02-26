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
 * De-identification
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: uwbionlp.proto")
public final class DeidentificationGrpc {

  private DeidentificationGrpc() {}

  public static final String SERVICE_NAME = "uwbionlp.parser.Deidentification";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput,
      edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput> METHOD_DEIDENTIFY =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput, edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "uwbionlp.parser.Deidentification", "Deidentify"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput.getDefaultInstance()))
          .setSchemaDescriptor(new DeidentificationMethodDescriptorSupplier("Deidentify"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static DeidentificationStub newStub(io.grpc.Channel channel) {
    return new DeidentificationStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static DeidentificationBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new DeidentificationBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static DeidentificationFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new DeidentificationFutureStub(channel);
  }

  /**
   * <pre>
   **
   * De-identification
   * </pre>
   */
  public static abstract class DeidentificationImplBase implements io.grpc.BindableService {

    /**
     */
    public void deidentify(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_DEIDENTIFY, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_DEIDENTIFY,
            asyncUnaryCall(
              new MethodHandlers<
                edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput,
                edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput>(
                  this, METHODID_DEIDENTIFY)))
          .build();
    }
  }

  /**
   * <pre>
   **
   * De-identification
   * </pre>
   */
  public static final class DeidentificationStub extends io.grpc.stub.AbstractStub<DeidentificationStub> {
    private DeidentificationStub(io.grpc.Channel channel) {
      super(channel);
    }

    private DeidentificationStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected DeidentificationStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new DeidentificationStub(channel, callOptions);
    }

    /**
     */
    public void deidentify(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_DEIDENTIFY, getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   **
   * De-identification
   * </pre>
   */
  public static final class DeidentificationBlockingStub extends io.grpc.stub.AbstractStub<DeidentificationBlockingStub> {
    private DeidentificationBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private DeidentificationBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected DeidentificationBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new DeidentificationBlockingStub(channel, callOptions);
    }

    /**
     */
    public edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput deidentify(edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request) {
      return blockingUnaryCall(
          getChannel(), METHOD_DEIDENTIFY, getCallOptions(), request);
    }
  }

  /**
   * <pre>
   **
   * De-identification
   * </pre>
   */
  public static final class DeidentificationFutureStub extends io.grpc.stub.AbstractStub<DeidentificationFutureStub> {
    private DeidentificationFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private DeidentificationFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected DeidentificationFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new DeidentificationFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput> deidentify(
        edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_DEIDENTIFY, getCallOptions()), request);
    }
  }

  private static final int METHODID_DEIDENTIFY = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final DeidentificationImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(DeidentificationImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_DEIDENTIFY:
          serviceImpl.deidentify((edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput) request,
              (io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.parser.Uwbionlp.DeidentificationOutput>) responseObserver);
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

  private static abstract class DeidentificationBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    DeidentificationBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.parser.Uwbionlp.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Deidentification");
    }
  }

  private static final class DeidentificationFileDescriptorSupplier
      extends DeidentificationBaseDescriptorSupplier {
    DeidentificationFileDescriptorSupplier() {}
  }

  private static final class DeidentificationMethodDescriptorSupplier
      extends DeidentificationBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    DeidentificationMethodDescriptorSupplier(String methodName) {
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
      synchronized (DeidentificationGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new DeidentificationFileDescriptorSupplier())
              .addMethod(METHOD_DEIDENTIFY)
              .build();
        }
      }
    }
    return result;
  }
}
