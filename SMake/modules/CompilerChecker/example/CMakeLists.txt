message("<smake::CompilerChecker> /modules/CompilerChecker/example/CMakeLists.txt in")

# set(CompilerChecker_INNER_INCLUDE_DIR ${CompilerChecker_INNER_INCLUDE_DIR} ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/)
# message("<CompilerChecker-CompilerChecker_INNER_INCLUDE_DIR> ${CompilerChecker_INNER_INCLUDE_DIR}")
# include_directories(${CompilerChecker_INNER_INCLUDE_DIR})

set(CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG )
set(CompilerChecker_INNER_EXSAMPLE_LINK_FLAG )

if(${CMAKE_GENERATOR} STREQUAL "Unix Makefiles")
    set(CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG ${CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG}
            -Wl,-rpath=./)
    set(CompilerChecker_INNER_EXSAMPLE_LINK_FLAG ${CompilerChecker_INNER_EXSAMPLE_LINK_FLAG}
            -lrt)
elseif(${CMAKE_GENERATOR} STREQUAL "MinGW Makefiles")
elseif(${CMAKE_GENERATOR} MATCHES "Visual Studio")
endif()

set(CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG ${CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG}
        -DPUMP_CORE_USING_DLL)

# set(CMAKE_CXX_STANDARD 98)
# add_executable(WinCmdClient ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/example/WinCmdClient.cpp)
# target_include_directories(WinCmdClient PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(WinCmdClient CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_EXSAMPLE_LINK_FLAG})
# target_compile_options(WinCmdClient PRIVATE ${CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG})
# set_target_properties(WinCmdClient PROPERTIES FOLDER "CompilerChecker/example")

# set(CMAKE_CXX_STANDARD 98)
# add_executable(WinCmdServer ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/example/WinCmdServer.cpp)
# target_include_directories(WinCmdServer PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(WinCmdServer CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_EXSAMPLE_LINK_FLAG})
# target_compile_options(WinCmdServer PRIVATE ${CompilerChecker_INNER_EXSAMPLE_COMPILE_FLAG})
# set_target_properties(WinCmdServer PROPERTIES FOLDER "CompilerChecker/example")

message("<smake::CompilerChecker> /modules/CompilerChecker/example/CMakeLists.txt out")