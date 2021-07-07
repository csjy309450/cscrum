message("<smake::CompilerChecker> /modules/CompilerChecker/src/CMakeLists.txt in")

include(${CompilerChecker_INNER_PROJECT_ROOT_DIR}/src/CompilerChecker/CMakeLists.txt)

if(${CompilerChecker_BUILD_FLAG} MATCHES "static")
    set(CMAKE_CXX_STANDARD 98)
    set(CompilerChecker_INNER_SLIB_NAME CompilerChecker)
    if(${smake_COMPILER} MATCHES "vc")
        set(CompilerChecker_INNER_SLIB_NAME lib${CompilerChecker_INNER_SLIB_NAME})
        set(CompilerChecker_INNER_SLIB_NAME ${CompilerChecker_INNER_SLIB_NAME}-${smake_COMPILER}-${smake_CPUARCH_FLAGE}-sll)
    elseif(${smake_COMPILER} MATCHES "gcc")
        set(CompilerChecker_INNER_SLIB_NAME ${CompilerChecker_INNER_SLIB_NAME}-${smake_COMPILER})
    endif()
    if(${smake_BUILD_TYPE} STREQUAL "Debug")
        set(CompilerChecker_INNER_SLIB_NAME ${CompilerChecker_INNER_SLIB_NAME}-d)
    else()
        set(CompilerChecker_INNER_SLIB_NAME ${CompilerChecker_INNER_SLIB_NAME}-r)
    endif()
    string(REPLACE "." "_" CompilerChecker_INNER_VERSION_STR ${CompilerChecker_INNER_VERSION})
    set(CompilerChecker_INNER_SLIB_NAME ${CompilerChecker_INNER_SLIB_NAME}-${CompilerChecker_INNER_VERSION_STR})
    message("<smake::CompilerChecker> CompilerChecker_INNER_SLIB_NAME=${CompilerChecker_INNER_SLIB_NAME}")
    add_library(CompilerChecker_sll
        STATIC
        ${CompilerChecker_INNER_HEADERS}
        ${CompilerChecker_INNER_SRCS}
        )
    target_include_directories(CompilerChecker_sll PRIVATE ${CompilerChecker_INNER_INCLUDE_DIR})
    target_compile_definitions(CompilerChecker_sll PRIVATE COMPILERCHECKER_BUILD_SLL=1)
    target_compile_options(CompilerChecker_sll PRIVATE ${CompilerChecker_INNER_COMPILE_FLAG})
    set_target_properties(CompilerChecker_sll PROPERTIES OUTPUT_NAME ${CompilerChecker_INNER_SLIB_NAME})
    set_target_properties(CompilerChecker_sll PROPERTIES FOLDER "CompilerChecker/target")
    if(${smake_OS_PLATFORM} MATCHES "win")
        set(CompilerChecker_LIBRARIES "${CompilerChecker_INNER_SLIB_NAME}.lib" CACHE STRING INTERNAL FORCE)
    elseif(${smake_OS_PLATFORM} MATCHES "linux")
        set(CompilerChecker_LIBRARIES "${CompilerChecker_INNER_SLIB_NAME}.a" CACHE STRING INTERNAL FORCE)
    endif()
    message("<smake::CompilerChecker> CompilerChecker_LIBRARIES=${CompilerChecker_LIBRARIES}")
endif()

if(${CompilerChecker_BUILD_FLAG} MATCHES "shared")
    set(CMAKE_CXX_STANDARD 98)
    set(CompilerChecker_DLIB_NAME CompilerChecker)
    if(${smake_COMPILER} MATCHES "vc")
        set(CompilerChecker_DLIB_NAME lib${CompilerChecker_DLIB_NAME})
        set(CompilerChecker_DLIB_NAME ${CompilerChecker_DLIB_NAME}-${smake_COMPILER}-${smake_CPUARCH_FLAGE}-dll)
    elseif(${smake_COMPILER} MATCHES "gcc")
        set(CompilerChecker_DLIB_NAME ${CompilerChecker_DLIB_NAME}-${smake_COMPILER})
    endif()
    if(${smake_BUILD_TYPE} STREQUAL "Debug")
        set(CompilerChecker_DLIB_NAME ${CompilerChecker_DLIB_NAME}-d)
    else()
        set(CompilerChecker_DLIB_NAME ${CompilerChecker_DLIB_NAME}-r)
    endif()
    string(REPLACE "." "_" CompilerChecker_INNER_VERSION_STR ${CompilerChecker_INNER_VERSION})
    set(CompilerChecker_DLIB_NAME ${CompilerChecker_DLIB_NAME}-${CompilerChecker_INNER_VERSION_STR})
    message("<smake::CompilerChecker> CompilerChecker_DLIB_NAME=${CompilerChecker_DLIB_NAME}")
    add_library(CompilerChecker_dll
        SHARED
        ${CompilerChecker_INNER_HEADERS}
        ${CompilerChecker_INNER_SRCS}
        )
    target_link_libraries(CompilerChecker_dll
        ${CompilerChecker_INNER_DEP_LIBS}
        ${CompilerChecker_INNER_LINK_FLAG}
        )
    target_include_directories(CompilerChecker_dll PRIVATE ${CompilerChecker_INNER_INCLUDE_DIR})
    target_compile_definitions(CompilerChecker_dll PRIVATE COMPILERCHECKER_BUILD_DLL=1)
    target_compile_options(CompilerChecker_dll PRIVATE ${CompilerChecker_INNER_COMPILE_FLAG})
    set_target_properties(CompilerChecker_dll PROPERTIES OUTPUT_NAME ${CompilerChecker_DLIB_NAME})
    set_target_properties(CompilerChecker_dll PROPERTIES FOLDER "CompilerChecker/target")
    if(${smake_OS_PLATFORM} MATCHES "win")
        set(CompilerChecker_LIBRARIES "${CompilerChecker_DLIB_NAME}.dll" CACHE STRING INTERNAL FORCE)
    elseif(${smake_OS_PLATFORM} MATCHES "linux")
        set(CompilerChecker_LIBRARIES "${CompilerChecker_DLIB_NAME}.so" CACHE STRING INTERNAL FORCE)
    endif()
    message("<smake::CompilerChecker> CompilerChecker_LIBRARIES=${CompilerChecker_LIBRARIES}")
endif()

if(${CompilerChecker_BUILD_FLAG} MATCHES "exe")
    set(CMAKE_CXX_STANDARD 98)
    set(CompilerChecker_EXE_NAME CompilerChecker)
    message("<smake::CompilerChecker> CompilerChecker_DLIB_NAME=${CompilerChecker_DLIB_NAME}")
    add_executable(CompilerChecker_exe
        ${CompilerChecker_INNER_HEADERS}
        ${CompilerChecker_INNER_SRCS}
        )
    target_link_libraries(CompilerChecker_exe
        ${CompilerChecker_INNER_DEP_LIBS}
        ${CompilerChecker_INNER_LINK_FLAG}
        )
    target_include_directories(CompilerChecker_exe PRIVATE ${CompilerChecker_INNER_INCLUDE_DIR})
    target_compile_definitions(CompilerChecker_exe PRIVATE COMPILERCHECKER_BUILD_EXE=1)
    target_compile_options(CompilerChecker_exe PRIVATE 
        ${CompilerChecker_INNER_COMPILE_FLAG}
        -DPUMP_CORE_USING_DLL
        )
    set_target_properties(CompilerChecker_exe PROPERTIES OUTPUT_NAME ${CompilerChecker_EXE_NAME})
    set_target_properties(CompilerChecker_exe PROPERTIES FOLDER "CompilerChecker/target")

    message("<smake::CompilerChecker> CompilerChecker_EXE=${CompilerChecker_EXE}")
endif()

message("<smake::CompilerChecker> /modules/CompilerChecker/src/CMakeLists.txt out")
