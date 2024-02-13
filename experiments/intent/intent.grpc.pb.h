// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: intent.proto
#ifndef GRPC_intent_2eproto__INCLUDED
#define GRPC_intent_2eproto__INCLUDED

#include "intent.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/method_handler_impl.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

namespace grpc {
class CompletionQueue;
class Channel;
class ServerCompletionQueue;
class ServerContext;
}  // namespace grpc

namespace intent {

class Intent final {
 public:
  static constexpr char const* service_full_name() {
    return "intent.Intent";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    virtual ::grpc::Status setIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::intent::IntentResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>> AsyncsetIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>>(AsyncsetIntentRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>> PrepareAsyncsetIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>>(PrepareAsyncsetIntentRaw(context, request, cq));
    }
    class experimental_async_interface {
     public:
      virtual ~experimental_async_interface() {}
      virtual void setIntent(::grpc::ClientContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response, std::function<void(::grpc::Status)>) = 0;
    };
    virtual class experimental_async_interface* experimental_async() { return nullptr; }
  private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>* AsyncsetIntentRaw(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::intent::IntentResponse>* PrepareAsyncsetIntentRaw(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel);
    ::grpc::Status setIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::intent::IntentResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>> AsyncsetIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>>(AsyncsetIntentRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>> PrepareAsyncsetIntent(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>>(PrepareAsyncsetIntentRaw(context, request, cq));
    }
    class experimental_async final :
      public StubInterface::experimental_async_interface {
     public:
      void setIntent(::grpc::ClientContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response, std::function<void(::grpc::Status)>) override;
     private:
      friend class Stub;
      explicit experimental_async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class experimental_async_interface* experimental_async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class experimental_async async_stub_{this};
    ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>* AsyncsetIntentRaw(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::intent::IntentResponse>* PrepareAsyncsetIntentRaw(::grpc::ClientContext* context, const ::intent::IntentRequest& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_setIntent_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    virtual ::grpc::Status setIntent(::grpc::ServerContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_setIntent : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_setIntent() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_setIntent() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status setIntent(::grpc::ServerContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestsetIntent(::grpc::ServerContext* context, ::intent::IntentRequest* request, ::grpc::ServerAsyncResponseWriter< ::intent::IntentResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_setIntent<Service > AsyncService;
  template <class BaseClass>
  class WithGenericMethod_setIntent : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_setIntent() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_setIntent() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status setIntent(::grpc::ServerContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_setIntent : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithRawMethod_setIntent() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_setIntent() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status setIntent(::grpc::ServerContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestsetIntent(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_setIntent : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithStreamedUnaryMethod_setIntent() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::StreamedUnaryHandler< ::intent::IntentRequest, ::intent::IntentResponse>(std::bind(&WithStreamedUnaryMethod_setIntent<BaseClass>::StreamedsetIntent, this, std::placeholders::_1, std::placeholders::_2)));
    }
    ~WithStreamedUnaryMethod_setIntent() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status setIntent(::grpc::ServerContext* context, const ::intent::IntentRequest* request, ::intent::IntentResponse* response) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedsetIntent(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::intent::IntentRequest,::intent::IntentResponse>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_setIntent<Service > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_setIntent<Service > StreamedService;
};

}  // namespace intent


#endif  // GRPC_intent_2eproto__INCLUDED