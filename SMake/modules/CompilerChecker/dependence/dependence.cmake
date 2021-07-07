#########################################################
# @file:    dependence.cmake
# @author:  yangzheng
# @brief:   modular CompilerChecker dependence configure.
#########################################################
message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/dependence.cmake in")

# #</find Boost>
# find_package(Boost REQUIRED COMPONENTS
#         thread
#         system
#         program_options)
# #</find Boost>

# TODO unzip boost.zip
# if(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
#         # Scan all files in directory.
#         execute_process(COMMAND find ${in_dir} -type d
#                 RESULT_VARIABLE ret
#                 OUTPUT_VARIABLE dir_dirs)
# elseif(${CMAKE_SYSTEM_NAME}  MATCHES "Windows")
#         message("<smake::CompilerChecker> expand ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/include/win/boost.zip")
#         execute_process(COMMAND expand ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/include/win/boost.zip
#                 RESULT_VARIABLE ret)
# endif(${CMAKE_SYSTEM_NAME}  MATCHES "Linux")

# containing header dir to project
set(CompilerChecker_INNER_DEP_INC_DIRS
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/include/${smake_OS_PLATFORM}
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/include
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src
        ${smake_macro_INCLUDE_DIRS}
        # ${Boost_INCLUDE_DIRS}
        )
message("<smake::CompilerChecker> CompilerChecker_INNER_DEP_INC_DIRS=${CompilerChecker_INNER_DEP_INC_DIRS}")

if (${smake_OS_PLATFORM} MATCHES "win")
        set(CompilerChecker_INNER_DEP_LIBS
                version.lib
        )
elseif(${smake_OS_PLATFORM} MATCHES "linux")
endif (${smake_OS_PLATFORM} MATCHES "win")

# containing 3rdpart libs to project
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/dlibs/CMakeLists.txt)
include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/slibs/CMakeLists.txt)
set(CompilerChecker_INNER_DEP_LIBS
        ${CompilerChecker_INNER_DEP_LIBS}
        ${CompilerChecker_INNER_DEP_SLIBS}
        ${CompilerChecker_INNER_DEP_DLIBS}
        )
message("<smake::CompilerChecker> CompilerChecker_INNER_DEP_LIBS=${CompilerChecker_INNER_DEP_LIBS}")

# set test srdparty header
set(CompilerChecker_INNER_TEST_DEP_INC_DIRS
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/include/${smake_OS_PLATFORM}
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/include
        ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src
        ${CompilerChecker_INCLUDE_DIRS}
        )
message("<smake::CompilerChecker> CompilerChecker_INNER_TEST_DEP_INC_DIRS=${CompilerChecker_INNER_TEST_DEP_INC_DIRS}")

# set test srdparty libs
set(CompilerChecker_INNER_TEST_DEP_LIBS
        ${CompilerChecker_INNER_DEP_SLIBS}
        ${CompilerChecker_INNER_DEP_DLIBS}
        )
message("<smake::CompilerChecker> CompilerChecker_INNER_TEST_DEP_LIBS=${CompilerChecker_INNER_TEST_DEP_LIBS}")


message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/dependence.cmake out")