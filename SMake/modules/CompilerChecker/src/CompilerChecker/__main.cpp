#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_logger.h"
#include "__ClChecker.h"
#include "__GlobalMgr.h"

int main(int argc, char** argv)
{
    PUMP_CORE_INFO("[INFO] CompilerChecker start!");
    GetGlobalMgr().Init();
    GetGlobalMgr().CheckCompiler();
    //GetGlobalMgr().CheckPrimaryBuilder();
    //GetGlobalMgr().CheckSecondaryBuilder();
    GetGlobalMgr().WriteFile();
    GetGlobalMgr().Cleanup();
    PUMP_CORE_INFO("[INFO] CompilerChecker finished!");
    return getchar();
}