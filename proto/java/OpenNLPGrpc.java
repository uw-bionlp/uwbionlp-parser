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
 * OpenNLP
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: CovidParser.proto")
public final class OpenNLPGrpc {

  private OpenNLPGrpc() {}

  public static final String SERVICE_NAME = "covid.parser.OpenNLP";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput,
      edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput> METHOD_DETECT_SENTENCES =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput, edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "covid.parser.OpenNLP", "DetectSentences"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput.getDefaultInstance()))
          .setSchemaDescriptor(new OpenNLPMethodDescriptorSupplier("DetectSentences"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static OpenNLPStub newStub(io.grpc.Channel channel) {
    return new OpenNLPStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static OpenNLPBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new OpenNLPBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static OpenNLPFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new OpenNLPFutureStub(channel);
  }

  /**
   * <pre>
   **
   * OpenNLP
   * </pre>
   */
  public static abstract class OpenNLPImplBase implements io.grpc.BindableService {

    /**
     */
    public void detectSentences(edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_DETECT_SENTENCES, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_DETECT_SENTENCES,
            asyncUnaryCall(
              new MethodHandlers<
                edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput,
                edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput>(
                  this, METHODID_DETECT_SENTENCES)))
          .build();
    }
  }

  /**
   * <pre>
   **
   * OpenNLP
   * </pre>
   */
  public static final class OpenNLPStub extends io.grpc.stub.AbstractStub<OpenNLPStub> {
    private OpenNLPStub(io.grpc.Channel channel) {
      super(channel);
    }

    private OpenNLPStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected OpenNLPStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new OpenNLPStub(channel, callOptions);
    }

    /**
     */
    public void detectSentences(edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_DETECT_SENTENCES, getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   **
   * OpenNLP
   * </pre>
   */
  public static final class OpenNLPBlockingStub extends io.grpc.stub.AbstractStub<OpenNLPBlockingStub> {
    private OpenNLPBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private OpenNLPBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected OpenNLPBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new OpenNLPBlockingStub(channel, callOptions);
    }

    /**
     */
    public edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput detectSentences(edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput request) {
      return blockingUnaryCall(
          getChannel(), METHOD_DETECT_SENTENCES, getCallOptions(), request);
    }
  }

  /**
   * <pre>
   **
   * OpenNLP
   * </pre>
   */
  public static final class OpenNLPFutureStub extends io.grpc.stub.AbstractStub<OpenNLPFutureStub> {
    private OpenNLPFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private OpenNLPFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected OpenNLPFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new OpenNLPFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput> detectSentences(
        edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_DETECT_SENTENCES, getCallOptions()), request);
    }
  }

  private static final int METHODID_DETECT_SENTENCES = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final OpenNLPImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(OpenNLPImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_DETECT_SENTENCES:
          serviceImpl.detectSentences((edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput) request,
              (io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput>) responseObserver);
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

  private static abstract class OpenNLPBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    OpenNLPBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.covid.parser.CovidParser.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("OpenNLP");
    }
  }

  private static final class OpenNLPFileDescriptorSupplier
      extends OpenNLPBaseDescriptorSupplier {
    OpenNLPFileDescriptorSupplier() {}
  }

  private static final class OpenNLPMethodDescriptorSupplier
      extends OpenNLPBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    OpenNLPMethodDescriptorSupplier(String methodName) {
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
      synchronized (OpenNLPGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new OpenNLPFileDescriptorSupplier())
              .addMethod(METHOD_DETECT_SENTENCES)
              .build();
        }
      }
    }
    return result;
  }
}
