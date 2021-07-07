message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/slibs/CMakeLists.txt in")

# aimed at containing static libs or windows import libs to project
if(${smake_OS_PLATFORM} STREQUAL "linux_x64")
    if(${smake_DEBUG_FLAG})
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    else()
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    endif()
elseif(${smake_OS_PLATFORM} STREQUAL "linux_x86")
    if(${smake_DEBUG_FLAG})
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    else()
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    endif()
elseif(${smake_OS_PLATFORM} STREQUAL "win_x64")
    if(${smake_DEBUG_FLAG})
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    else()
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    endif()
elseif(${smake_OS_PLATFORM} STREQUAL "win_x86")
    if(${smake_DEBUG_FLAG})
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    else()
        set(CompilerChecker_INNER_DEP_SLIBS
                )
    endif()
endif()

file(GLOB_RECURSE CompilerChecker_INNER_DEP_SLIBFILES
        "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/slibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*")
# different platform are libs extension differently.
if (${smake_OS_PLATFORM} MATCHES "win")
    file(GLOB_RECURSE CompilerChecker_INNER_DEP_SLIBS
            "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/slibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*.lib")
elseif(${smake_OS_PLATFORM} MATCHES "linux")
    file(GLOB_RECURSE CompilerChecker_INNER_DEP_SLIBS
            "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/slibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*.a")
endif (${smake_OS_PLATFORM} MATCHES "win")
message("<smake::CompilerChecker> CompilerChecker_INNER_DEP_SLIBS=${CompilerChecker_INNER_DEP_SLIBS}")

message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/slibs/CMakeLists.txt out")