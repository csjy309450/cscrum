message("<smake::CompilerChecker> /cmake/FindCompilerChecker.cmake in")

if(NOT CompilerChecker_FOUND)
    add_subdirectory(${smake_ROOT_DIR}/modules/CompilerChecker/)
endif()

set(CompilerChecker_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/modules/CompilerChecker/include)
message("<smake::CompilerChecker> CompilerChecker_INCLUDE_DIRS=${CompilerChecker_INCLUDE_DIRS}")

set(CompilerChecker_LIBRARIES "" CACHE STRING INTERNAL FORCE)
message("<smake::CompilerChecker> CompilerChecker_LIBRARIES=${CompilerChecker_LIBRARIES}")

set(CompilerChecker_FOUND TRUE)
message("<smake::CompilerChecker> CompilerChecker_FOUND=${CompilerChecker_FOUND}")

message("<smake::CompilerChecker> /cmake/FindCompilerChecker.cmake out")