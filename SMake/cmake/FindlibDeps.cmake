message("<smake::libDeps> /cmake/FindlibDeps.cmake in")

if(NOT libDeps_FOUND)
    add_subdirectory(${smake_ROOT_DIR}/modules/libDeps/)
endif()

set(libDeps_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/modules/libDeps/include)
message("<smake::libDeps> libDeps_INCLUDE_DIRS=${libDeps_INCLUDE_DIRS}")

set(libDeps_LIBRARIES "" CACHE STRING INTERNAL FORCE)
message("<smake::libDeps> libDeps_LIBRARIES=${libDeps_LIBRARIES}")

set(libDeps_FOUND TRUE)
message("<smake::libDeps> libDeps_FOUND=${libDeps_FOUND}")

message("<smake::libDeps> /cmake/FindlibDeps.cmake out")