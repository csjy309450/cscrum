message("<smake::CompilerChecker> /modules/CompilerChecker/src/CompilerChecker/CMakeLists.txt in")

# find header dir
find_sub_dir(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/CompilerChecker CompilerChecker_INNER_INCLUDE_DIR)
set(CompilerChecker_INNER_INCLUDE_DIR ${CompilerChecker_INNER_INCLUDE_DIR} ${CompilerChecker_INNER_DEP_INC_DIRS})
# include_directories(${CompilerChecker_INNER_INCLUDE_DIR})
# find header and src code
find_header_in_dir(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/include/CompilerChecker CompilerChecker_INNER_HEADERS_1)
find_header_in_dir(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/CompilerChecker CompilerChecker_INNER_HEADERS_2)
set(CompilerChecker_INNER_HEADERS ${CompilerChecker_INNER_HEADERS_1} ${CompilerChecker_INNER_HEADERS_2})
find_src_in_dir(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/CompilerChecker CompilerChecker_INNER_SRCS)
message("<smake::CompilerChecker> CompilerChecker_INNER_HEADERS=${CompilerChecker_INNER_HEADERS}")
message("<smake::CompilerChecker> CompilerChecker_INNER_SRCS=${CompilerChecker_INNER_SRCS}")

message("<smake::CompilerChecker> /modules/CompilerChecker/src/CompilerChecker/CMakeLists.txt out")