// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: intent.proto

#ifndef PROTOBUF_INCLUDED_intent_2eproto
#define PROTOBUF_INCLUDED_intent_2eproto

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 3006001
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 3006001 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#define PROTOBUF_INTERNAL_EXPORT_protobuf_intent_2eproto 

namespace protobuf_intent_2eproto {
// Internal implementation detail -- do not use these members.
struct TableStruct {
  static const ::google::protobuf::internal::ParseTableField entries[];
  static const ::google::protobuf::internal::AuxillaryParseTableField aux[];
  static const ::google::protobuf::internal::ParseTable schema[2];
  static const ::google::protobuf::internal::FieldMetadata field_metadata[];
  static const ::google::protobuf::internal::SerializationTable serialization_table[];
  static const ::google::protobuf::uint32 offsets[];
};
void AddDescriptors();
}  // namespace protobuf_intent_2eproto
namespace intent {
class IntentRequest;
class IntentRequestDefaultTypeInternal;
extern IntentRequestDefaultTypeInternal _IntentRequest_default_instance_;
class IntentResponse;
class IntentResponseDefaultTypeInternal;
extern IntentResponseDefaultTypeInternal _IntentResponse_default_instance_;
}  // namespace intent
namespace google {
namespace protobuf {
template<> ::intent::IntentRequest* Arena::CreateMaybeMessage<::intent::IntentRequest>(Arena*);
template<> ::intent::IntentResponse* Arena::CreateMaybeMessage<::intent::IntentResponse>(Arena*);
}  // namespace protobuf
}  // namespace google
namespace intent {

// ===================================================================

class IntentRequest : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:intent.IntentRequest) */ {
 public:
  IntentRequest();
  virtual ~IntentRequest();

  IntentRequest(const IntentRequest& from);

  inline IntentRequest& operator=(const IntentRequest& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  IntentRequest(IntentRequest&& from) noexcept
    : IntentRequest() {
    *this = ::std::move(from);
  }

  inline IntentRequest& operator=(IntentRequest&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const IntentRequest& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const IntentRequest* internal_default_instance() {
    return reinterpret_cast<const IntentRequest*>(
               &_IntentRequest_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  void Swap(IntentRequest* other);
  friend void swap(IntentRequest& a, IntentRequest& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline IntentRequest* New() const final {
    return CreateMaybeMessage<IntentRequest>(NULL);
  }

  IntentRequest* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<IntentRequest>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const IntentRequest& from);
  void MergeFrom(const IntentRequest& from);
  void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input) final;
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const final;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(IntentRequest* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return NULL;
  }
  inline void* MaybeArenaPtr() const {
    return NULL;
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // int64 id = 1;
  void clear_id();
  static const int kIdFieldNumber = 1;
  ::google::protobuf::int64 id() const;
  void set_id(::google::protobuf::int64 value);

  // int64 limitUEAdmitted = 2;
  void clear_limitueadmitted();
  static const int kLimitUEAdmittedFieldNumber = 2;
  ::google::protobuf::int64 limitueadmitted() const;
  void set_limitueadmitted(::google::protobuf::int64 value);

  // int64 limitUEAdmissionPerSecond = 3;
  void clear_limitueadmissionpersecond();
  static const int kLimitUEAdmissionPerSecondFieldNumber = 3;
  ::google::protobuf::int64 limitueadmissionpersecond() const;
  void set_limitueadmissionpersecond(::google::protobuf::int64 value);

  // @@protoc_insertion_point(class_scope:intent.IntentRequest)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::int64 id_;
  ::google::protobuf::int64 limitueadmitted_;
  ::google::protobuf::int64 limitueadmissionpersecond_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_intent_2eproto::TableStruct;
};
// -------------------------------------------------------------------

class IntentResponse : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:intent.IntentResponse) */ {
 public:
  IntentResponse();
  virtual ~IntentResponse();

  IntentResponse(const IntentResponse& from);

  inline IntentResponse& operator=(const IntentResponse& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  IntentResponse(IntentResponse&& from) noexcept
    : IntentResponse() {
    *this = ::std::move(from);
  }

  inline IntentResponse& operator=(IntentResponse&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const IntentResponse& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const IntentResponse* internal_default_instance() {
    return reinterpret_cast<const IntentResponse*>(
               &_IntentResponse_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  void Swap(IntentResponse* other);
  friend void swap(IntentResponse& a, IntentResponse& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline IntentResponse* New() const final {
    return CreateMaybeMessage<IntentResponse>(NULL);
  }

  IntentResponse* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<IntentResponse>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const IntentResponse& from);
  void MergeFrom(const IntentResponse& from);
  void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input) final;
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const final;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(IntentResponse* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return NULL;
  }
  inline void* MaybeArenaPtr() const {
    return NULL;
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // int64 id = 1;
  void clear_id();
  static const int kIdFieldNumber = 1;
  ::google::protobuf::int64 id() const;
  void set_id(::google::protobuf::int64 value);

  // bool status = 2;
  void clear_status();
  static const int kStatusFieldNumber = 2;
  bool status() const;
  void set_status(bool value);

  // @@protoc_insertion_point(class_scope:intent.IntentResponse)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::int64 id_;
  bool status_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_intent_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// IntentRequest

// int64 id = 1;
inline void IntentRequest::clear_id() {
  id_ = GOOGLE_LONGLONG(0);
}
inline ::google::protobuf::int64 IntentRequest::id() const {
  // @@protoc_insertion_point(field_get:intent.IntentRequest.id)
  return id_;
}
inline void IntentRequest::set_id(::google::protobuf::int64 value) {
  
  id_ = value;
  // @@protoc_insertion_point(field_set:intent.IntentRequest.id)
}

// int64 limitUEAdmitted = 2;
inline void IntentRequest::clear_limitueadmitted() {
  limitueadmitted_ = GOOGLE_LONGLONG(0);
}
inline ::google::protobuf::int64 IntentRequest::limitueadmitted() const {
  // @@protoc_insertion_point(field_get:intent.IntentRequest.limitUEAdmitted)
  return limitueadmitted_;
}
inline void IntentRequest::set_limitueadmitted(::google::protobuf::int64 value) {
  
  limitueadmitted_ = value;
  // @@protoc_insertion_point(field_set:intent.IntentRequest.limitUEAdmitted)
}

// int64 limitUEAdmissionPerSecond = 3;
inline void IntentRequest::clear_limitueadmissionpersecond() {
  limitueadmissionpersecond_ = GOOGLE_LONGLONG(0);
}
inline ::google::protobuf::int64 IntentRequest::limitueadmissionpersecond() const {
  // @@protoc_insertion_point(field_get:intent.IntentRequest.limitUEAdmissionPerSecond)
  return limitueadmissionpersecond_;
}
inline void IntentRequest::set_limitueadmissionpersecond(::google::protobuf::int64 value) {
  
  limitueadmissionpersecond_ = value;
  // @@protoc_insertion_point(field_set:intent.IntentRequest.limitUEAdmissionPerSecond)
}

// -------------------------------------------------------------------

// IntentResponse

// int64 id = 1;
inline void IntentResponse::clear_id() {
  id_ = GOOGLE_LONGLONG(0);
}
inline ::google::protobuf::int64 IntentResponse::id() const {
  // @@protoc_insertion_point(field_get:intent.IntentResponse.id)
  return id_;
}
inline void IntentResponse::set_id(::google::protobuf::int64 value) {
  
  id_ = value;
  // @@protoc_insertion_point(field_set:intent.IntentResponse.id)
}

// bool status = 2;
inline void IntentResponse::clear_status() {
  status_ = false;
}
inline bool IntentResponse::status() const {
  // @@protoc_insertion_point(field_get:intent.IntentResponse.status)
  return status_;
}
inline void IntentResponse::set_status(bool value) {
  
  status_ = value;
  // @@protoc_insertion_point(field_set:intent.IntentResponse.status)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace intent

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_INCLUDED_intent_2eproto