message("<smake::CompilerChecker> /modules/CompilerChecker/CMakeLists.txt in")

message("<smake::CompilerChecker> CMAKE_CURRRENT_BINARY_DIR=${CMAKE_CURRRENT_BINARY_DIR}")
message("<smake::CompilerChecker> PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}")
message("<smake::CompilerChecker> CompilerChecker_INNER_SOURCE_DIR=${CompilerChecker_INNER_SOURCE_DIR}")
message("<smake::CompilerChecker> CMAKE_CURRENT_SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}")
message("<smake::CompilerChecker> CMAKE_MODULE_PATH=${CMAKE_MODULE_PATH}")
message("<smake::CompilerChecker> CMAKE_CURRENT_LIST_FILE=${CMAKE_CURRENT_LIST_FILE}")
message("<smake::CompilerChecker> CMAKE_CURRENT_LIST_DIR=${CMAKE_CURRENT_LIST_DIR}")

set(CompilerChecker_INNER_VERSION "0.9.0")

# config modular evn variale
if(NOT ${PROJECT_SOURCE_DIR} STREQUAL ${CMAKE_CURRENT_LIST_DIR})
    # build module non-independently.
    message("<smake::CompilerChecker> CompilerChecker_INNER_IS_SUB_MODULAR=true")
    set(CompilerChecker_INNER_IS_SUB_MODULAR true)
    set(CompilerChecker_INNER_PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})
    message("<smake::CompilerChecker> CompilerChecker_INNER_PROJECT_ROOT_DIR=${CompilerChecker_INNER_PROJECT_ROOT_DIR}")
    set(CompilerChecker_INNER_TOOLS_DIR ${PROJECT_SOURCE_DIR}/cmake)
    message("<smake::CompilerChecker> CompilerChecker_INNER_TOOLS_DIR=${CompilerChecker_INNER_TOOLS_DIR}")
else()
    # build module independently.
    message("<smake::CompilerChecker> CompilerChecker_INNER_IS_SUB_MODULAR=false")
    set(CompilerChecker_INNER_IS_SUB_MODULAR false)
    set(CompilerChecker_INNER_PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})
    message("<smake::CompilerChecker> CompilerChecker_INNER_PROJECT_ROOT_DIR=${CompilerChecker_INNER_PROJECT_ROOT_DIR}")
    set(CompilerChecker_INNER_TOOLS_DIR ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/cmake)
    message("<smake::CompilerChecker> CompilerChecker_INNER_TOOLS_DIR=${CompilerChecker_INNER_TOOLS_DIR}")
endif()

# load 3rdparty dependence, will create CompilerChecker_INNER_DEP_INC_DIRS CompilerChecker_INNER_DEP_LIBS
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/dependence.cmake)

# load compiler config
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/cmake/compiler_conf.cmake)

# load modular build script
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/CMakeLists.txt)

# load modular test script
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CMakeLists.txt)

# load modular example script
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/example/CMakeLists.txt)

message("<smake::CompilerChecker> /modules/CompilerChecker/CMakeLists.txt out")