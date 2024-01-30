cmake_minimum_required (VERSION 3.2)

project(simulator)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -pg -g3" )

file(GLOB SRCS
    ${CMAKE_CURRENT_SOURCE_DIR}/simulator.cpp
)

add_executable(${PROJECT_NAME} ${SRCS})
target_link_libraries(${PROJECT_NAME} 
    admission_clnt grpc++ grpc protobuf envman pistache pthread)
install(TARGETS ${PROJECT_NAME})