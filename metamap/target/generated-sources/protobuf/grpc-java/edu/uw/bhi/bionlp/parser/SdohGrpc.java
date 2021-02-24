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
 * Social Determinants of Health
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: uwbionlp.proto")
public final class SdohGrpc {

  private SdohGrpc() {}

  public static final String SERVICE_NAME = "uwbionlp.parser.Sdoh";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput,
      edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput> METHOD_PREDICT =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput, edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "uwbionlp.parser.Sdoh", "Predict"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.parser.Uwbionlp.PredictionOutput.getDefaultInstance()))
          .setSchemaDescriptor(new SdohMethodDescriptorSupplier("Predict"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static SdohStub newStub(io.grpc.Channel channel) {
    return new SdohStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static SdohBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new SdohBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static SdohFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new SdohFutureStub(channel);
  }

  /**
   * <pre>
   **
   * Social Determinants of Health
   * </pre>
   */
  public static abstract class SdohImplBase implements io.grpc.BindableService {

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
   * Social Determinants of Health
   * </pre>
   */
  public static final class SdohStub extends io.grpc.stub.AbstractStub<SdohStub> {
    private SdohStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SdohStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SdohStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SdohStub(channel, callOptions);
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
   * Social Determinants of Health
   * </pre>
   */
  public static final class SdohBlockingStub extends io.grpc.stub.AbstractStub<SdohBlockingStub> {
    private SdohBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SdohBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SdohBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SdohBlockingStub(channel, callOptions);
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
   * Social Determinants of Health
   * </pre>
   */
  public static final class SdohFutureStub extends io.grpc.stub.AbstractStub<SdohFutureStub> {
    private SdohFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SdohFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SdohFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SdohFutureStub(channel, callOptions);
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
    private final SdohImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(SdohImplBase serviceImpl, int methodId) {
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

  private static abstract class SdohBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    SdohBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.parser.Uwbionlp.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Sdoh");
    }
  }

  private static final class SdohFileDescriptorSupplier
      extends SdohBaseDescriptorSupplier {
    SdohFileDescriptorSupplier() {}
  }

  private static final class SdohMethodDescriptorSupplier
      extends SdohBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    SdohMethodDescriptorSupplier(String methodName) {
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
      synchronized (SdohGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new SdohFileDescriptorSupplier())
              .addMethod(METHOD_PREDICT)
              .build();
        }
      }
    }
    return result;
  }
}
