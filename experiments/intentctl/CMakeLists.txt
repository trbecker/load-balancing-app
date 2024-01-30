project(intentctl C CXX)
cmake_minimum_required(VERSION 3.10)

add_executable(intentctl intentctl.cpp intent/intent.grpc.pb.cc intent/intent.pb.cc)
target_link_libraries(intentctl
        grpc++ grpc protobuf pthread)

install(TARGETS intentctl
        DESTINATION ${CMAKE_INSTALL_NAME_DIR}/bin)