project(xapp C CXX)
cmake_minimum_required(VERSION 3.10)

add_executable(xapp xapp.cpp intent/intent.grpc.pb.cc intent/intent.pb.cc)
target_link_libraries(xapp
        admission_srv sqlite3 grpc++ grpc protobuf pthread)

install(TARGETS xapp
        DESTINATION ${CMAKE_INSTALL_PREFIX}/bin)