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
 * MetaMap
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.7.0)",
    comments = "Source: CovidParser.proto")
public final class MetaMapGrpc {

  private MetaMapGrpc() {}

  public static final String SERVICE_NAME = "covid.parser.MetaMap";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput,
      edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput> METHOD_EXTRACT_NAMED_ENTITIES =
      io.grpc.MethodDescriptor.<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput, edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "covid.parser.MetaMap", "ExtractNamedEntities"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput.getDefaultInstance()))
          .setSchemaDescriptor(new MetaMapMethodDescriptorSupplier("ExtractNamedEntities"))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static MetaMapStub newStub(io.grpc.Channel channel) {
    return new MetaMapStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static MetaMapBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new MetaMapBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static MetaMapFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new MetaMapFutureStub(channel);
  }

  /**
   * <pre>
   **
   * MetaMap
   * </pre>
   */
  public static abstract class MetaMapImplBase implements io.grpc.BindableService {

    /**
     */
    public void extractNamedEntities(edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_EXTRACT_NAMED_ENTITIES, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_EXTRACT_NAMED_ENTITIES,
            asyncUnaryCall(
              new MethodHandlers<
                edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput,
                edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput>(
                  this, METHODID_EXTRACT_NAMED_ENTITIES)))
          .build();
    }
  }

  /**
   * <pre>
   **
   * MetaMap
   * </pre>
   */
  public static final class MetaMapStub extends io.grpc.stub.AbstractStub<MetaMapStub> {
    private MetaMapStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MetaMapStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MetaMapStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MetaMapStub(channel, callOptions);
    }

    /**
     */
    public void extractNamedEntities(edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput request,
        io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_EXTRACT_NAMED_ENTITIES, getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   **
   * MetaMap
   * </pre>
   */
  public static final class MetaMapBlockingStub extends io.grpc.stub.AbstractStub<MetaMapBlockingStub> {
    private MetaMapBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MetaMapBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MetaMapBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MetaMapBlockingStub(channel, callOptions);
    }

    /**
     */
    public edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput extractNamedEntities(edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput request) {
      return blockingUnaryCall(
          getChannel(), METHOD_EXTRACT_NAMED_ENTITIES, getCallOptions(), request);
    }
  }

  /**
   * <pre>
   **
   * MetaMap
   * </pre>
   */
  public static final class MetaMapFutureStub extends io.grpc.stub.AbstractStub<MetaMapFutureStub> {
    private MetaMapFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MetaMapFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MetaMapFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MetaMapFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput> extractNamedEntities(
        edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_EXTRACT_NAMED_ENTITIES, getCallOptions()), request);
    }
  }

  private static final int METHODID_EXTRACT_NAMED_ENTITIES = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final MetaMapImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(MetaMapImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_EXTRACT_NAMED_ENTITIES:
          serviceImpl.extractNamedEntities((edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapInput) request,
              (io.grpc.stub.StreamObserver<edu.uw.bhi.bionlp.covid.parser.CovidParser.MetaMapOutput>) responseObserver);
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

  private static abstract class MetaMapBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    MetaMapBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return edu.uw.bhi.bionlp.covid.parser.CovidParser.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("MetaMap");
    }
  }

  private static final class MetaMapFileDescriptorSupplier
      extends MetaMapBaseDescriptorSupplier {
    MetaMapFileDescriptorSupplier() {}
  }

  private static final class MetaMapMethodDescriptorSupplier
      extends MetaMapBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    MetaMapMethodDescriptorSupplier(String methodName) {
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
      synchronized (MetaMapGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new MetaMapFileDescriptorSupplier())
              .addMethod(METHOD_EXTRACT_NAMED_ENTITIES)
              .build();
        }
      }
    }
    return result;
  }
}
