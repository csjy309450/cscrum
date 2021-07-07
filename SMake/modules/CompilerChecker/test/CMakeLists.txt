# set(CompilerChecker_INNER_INCLUDE_DIR ${CompilerChecker_INNER_INCLUDE_DIR} ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/)
# message("<CompilerChecker-CompilerChecker_INNER_INCLUDE_DIR> ${CompilerChecker_INNER_INCLUDE_DIR}")
# include_directories(${CompilerChecker_INNER_INCLUDE_DIR})

set(CompilerChecker_INNER_TEST_COMPILE_FLAG )
set(CompilerChecker_INNER_TEST_LINK_FLAG )

if(${CMAKE_GENERATOR} STREQUAL "Unix Makefiles")
    set(CompilerChecker_INNER_TEST_COMPILE_FLAG ${CompilerChecker_INNER_TEST_COMPILE_FLAG}
            -Wl,-rpath=./)
    set(CompilerChecker_INNER_TEST_LINK_FLAG ${CompilerChecker_INNER_TEST_LINK_FLAG}
            -lrt)
elseif(${CMAKE_GENERATOR} STREQUAL "MinGW Makefiles")
elseif(${CMAKE_GENERATOR} MATCHES "Visual Studio")
endif()

set(CompilerChecker_INNER_TEST_COMPILE_FLAG ${CompilerChecker_INNER_TEST_COMPILE_FLAG}
        -DPUMP_CORE_USING_DLL)
set(CMAKE_CXX_STANDARD 98)

# add_executable(CompilerChecker_ut0 ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_ut0.cpp)
# target_include_directories(CompilerChecker_ut0 PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_ut0 CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_ut0 PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_ut0 PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_ut1 
#     ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_ut1.cpp
#     ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/async_pipe_server_thread.h
#     ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/async_pipe_server_thread.cpp
#     ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/async_pipe_server_recv_thread.h
#     ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/async_pipe_server_recv_thread.cpp
#     )
# target_include_directories(CompilerChecker_ut1 PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_ut1 CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_ut1 PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_ut1 PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_tcp_server ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_tcp_server.cpp)
# target_include_directories(CompilerChecker_test_fixture_tcp_server PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_tcp_server CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_tcp_server PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_tcp_server PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_tcp_client ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_tcp_client.cpp)
# target_include_directories(CompilerChecker_test_fixture_tcp_client PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_tcp_client CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_tcp_client PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_tcp_client PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_cmder_client ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_cmder_client.cpp)
# target_include_directories(CompilerChecker_test_fixture_cmder_client PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_cmder_client CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_cmder_client PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_cmder_client PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_cmder_server ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_cmder_server.cpp)
# target_include_directories(CompilerChecker_test_fixture_cmder_server PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_cmder_server CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_cmder_server PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_cmder_server PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_file ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_file.cpp)
# target_include_directories(CompilerChecker_test_fixture_file PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_file CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_file PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_file PROPERTIES FOLDER "CompilerChecker/test")

# add_executable(CompilerChecker_test_fixture_reg ${CompilerChecker_INNER_PROJECT_ROOT_DIR}/test/CompilerChecker_test_fixture_reg.cpp)
# target_include_directories(CompilerChecker_test_fixture_reg PRIVATE ${CompilerChecker_INNER_TEST_DEP_INC_DIRS})
# target_link_libraries(CompilerChecker_test_fixture_reg CompilerChecker_dll ${CompilerChecker_INNER_TEST_DEP_LIBS} ${CompilerChecker_INNER_TEST_LINK_FLAG})
# target_compile_options(CompilerChecker_test_fixture_reg PRIVATE ${CompilerChecker_INNER_TEST_COMPILE_FLAG})
# set_target_properties(CompilerChecker_test_fixture_reg PROPERTIES FOLDER "CompilerChecker/test")