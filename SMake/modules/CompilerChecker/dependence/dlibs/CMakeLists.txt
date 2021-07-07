message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/dlibs/CMakeLists.txt in")

# containing dlibs in project
#message("smake_OS_PLATFORM="${smake_OS_PLATFORM})
file(GLOB_RECURSE CompilerChecker_INNER_DEP_DLIBFILES
        "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/dlibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*")
# different platform are libs extension differently.
if (${smake_OS_PLATFORM} MATCHES "win")
    file(GLOB_RECURSE CompilerChecker_INNER_DEP_DLIBS
            "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/dlibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*.lib")
elseif(${smake_OS_PLATFORM} MATCHES "linux")
    file(GLOB_RECURSE CompilerChecker_INNER_DEP_DLIBS
            "${CompilerChecker_INNER_PROJECT_ROOT_DIR}/dependence/dlibs/${smake_OS_PLATFORM}_${smake_CPUARCH_FLAGE}/${smake_BUILD_TYPE}/*.so")
endif (${smake_OS_PLATFORM} MATCHES "win")
message("<smake::CompilerChecker> CompilerChecker_INNER_DEP_DLIBS=${CompilerChecker_INNER_DEP_DLIBS}")

# copy dlibs to output dir
if(MSVC)
    file(COPY ${CompilerChecker_INNER_DEP_DLIBFILES} DESTINATION ${smake_BINARY_DIR}/${smake_BUILD_TYPE})
else()
    file(COPY ${CompilerChecker_INNER_DEP_DLIBFILES} DESTINATION ${smake_BINARY_DIR})
endif()

message("<smake::CompilerChecker> /modules/CompilerChecker/dependence/dlibs/CMakeLists.txt out")
