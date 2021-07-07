#####################################################
# user supper-configure
#####################################################
set(smake_CPUARCH_FLAGE x64) # x86 x64
set(smake_COMPILER gcc) # gcc g++ cl clang
set(smake_BUILD_TYPE Debug)

#####################################################
# cmake script begine
#####################################################
cmake_minimum_required(VERSION 3.2)
project(smake)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/cmake)
set(smake_ROOT_DIR ${PROJECT_SOURCE_DIR})

message("<smake> CMakeLists.txt in")

message("<smake> CMAKE_BINARY_DIR=${CMAKE_BINARY_DIR}")

if(smake_BUILD_TYPE MATCHES "^((Debug)|(Release))$")
    set(CMAKE_BUILD_TYPE ${smake_BUILD_TYPE})
else()
    message(FATAL_ERROR "<smake> smake_BUILD_TYPE must be in {Debug, Release}")
endif()

# load file find function
include(${PROJECT_SOURCE_DIR}/cmake/find_files.cmake)

# check platform info and compiler info
include(${PROJECT_SOURCE_DIR}/cmake/compiler_conf.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/platforms/CMakeLists.txt)

# set libs/bin output dir
message("<smake> CMAKE_BINARY_DIR=${CMAKE_BINARY_DIR}")

# MSVC will add Debug/Release after output path automatically, so should have special handling under linux.
if(MSVC)
    set(smake_BINARY_DIR ${CMAKE_BINARY_DIR}/bin/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE})
else()
    set(smake_BINARY_DIR ${CMAKE_BINARY_DIR}/bin/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE})
endif()
message("<smake> smake_BINARY_DIR=${smake_BINARY_DIR}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${smake_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${smake_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${smake_BINARY_DIR})

# modules buiding configure
set(CompilerChecker_BUILD_FLAG "exe")
message("<smake> CompilerChecker_BUILD_FLAG=${CompilerChecker_BUILD_FLAG}")
if(${CompilerChecker_BUILD_FLAG} MATCHES "(shared)|(static)|(exe)|(code)")
    find_package(CompilerChecker)
endif()

set(libDeps_BUILD_FLAG "shared")
message("<smake> libDeps_BUILD_FLAG=${libDeps_BUILD_FLAG}")
if(${libDeps_BUILD_FLAG} MATCHES "(shared)|(static)|(exe)|(code)")
    find_package(libDeps)
endif()

# set(smake_core_BUILD_FLAG "shared,static")
# message("<smake> smake_core_BUILD_FLAG=${smake_core_BUILD_FLAG}")
# if(${smake_core_BUILD_FLAG} MATCHES "(shared)|(static)|(code)")
#     find_package(smake_core)
# endif()

# set(smake_function_BUILD_FLAG "static")
# message("<smake> smake_function_BUILD_FLAG=${smake_function_BUILD_FLAG}")
# if(${smake_function_BUILD_FLAG} MATCHES "(shared)|(static)|(code)")
#     find_package(smake_function)
# endif()

# set(smake_memory_BUILD_FLAG "static")
# message("<smake> smake_memory_BUILD_FLAG=${smake_memory_BUILD_FLAG}")
# if(${smake_memory_BUILD_FLAG} MATCHES "(shared)|(static)|(code)")
#     find_package(smake_memory)
# endif()


include(${PROJECT_SOURCE_DIR}/example/CMakeLists.txt)
set("<smake> CMakeLists.txt out")