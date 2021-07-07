message("<smake> /cmake/platforms/CMakeLists.txt in")

message("<smake> CMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}")
message("<smake> smake_CPUARCH_FLAGE=${smake_CPUARCH_FLAGE}")
if (CMAKE_SYSTEM_NAME MATCHES "Linux")
    set(smake_OS_PLATFORM "linux")
elseif(CMAKE_SYSTEM_NAME MATCHES "Windows")
    set(smake_OS_PLATFORM "win")
endif()
message("<smake> smake_OS_PLATFORM=${smake_OS_PLATFORM}")

message("<smake> /cmake/platforms/CMakeLists.txt out")