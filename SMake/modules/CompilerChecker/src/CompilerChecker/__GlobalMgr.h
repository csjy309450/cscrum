#ifndef GLOBAL_MGR_H
#define GLOBAL_MGR_H
#include <string>
#include <map>
#include "pump_core/pump_core_global_ctrl_base.h"
#include "pump_core/pump_core_mutex.h"
#include "pump_core/pump_core_environment.h"
#include "pump_core/pump_core_app.h"
#include "__CmdService.h"
#include "__ClChecker.h"
#include "__PrimaryBuilderChecker.h"
#include "__SecondaryBuilderChecker.h"

class CUserCmdClient;
class CThxCmdServer;
class CCompilerInfo;
class CPrimaryBuilderInfo;
class CSecondaryBuilderInfo;

typedef std::map<std::string, CCompilerInfo> CompilerInfoContainer;
typedef std::pair<std::string, CCompilerInfo> CompilerInfoItem;
typedef std::map<std::string, CPrimaryBuilderInfo> PrimaryBuilderInfoContainer;
typedef std::pair<std::string, CPrimaryBuilderInfo> PrimaryBuilderInfoItem;
typedef std::map<std::string, CSecondaryBuilderInfo> SecondaryBuilderInfoContainer;
typedef std::pair<std::string, CSecondaryBuilderInfo> SecondaryBuilderInfoItem;

class CompilerCheckerGlobalMgr
    : public ::Pump::Core::CGlobalCtrlBase
{
public:
    CompilerCheckerGlobalMgr() {}
    ~CompilerCheckerGlobalMgr() {}
    pump_int32_t Init();
    pump_int32_t Cleanup();
    pump_int32_t CheckCompiler();
    pump_int32_t CheckPrimaryBuilder();
    pump_int32_t CheckSecondaryBuilder();
    pump_int32_t WriteFile();
private:
    virtual pump_int32_t __Init();
    virtual pump_int32_t __Cleanup();
    /*
    * @brief initialize logger
    * @return 0-ok, -1-error
    */
    int __InitLogger();
public:
    ::Pump::Core::CApplication m_app;
    CUserCmdClient m_cmdClient;
    CThxCmdServer m_thxCmdServer;
    ::Pump::Core::Thread::CMutex m_csWriteCmd;
    std::string m_strOutput;
    CompilerInfoContainer m_mapCompilerInfo;
    PrimaryBuilderInfoContainer m_mapPrimaryBuilderInfo;
    SecondaryBuilderInfoContainer m_mapSecondaryBuiderInfo;
    ::Pump::Core::CEnvironment m_env;
};

CompilerCheckerGlobalMgr & GetGlobalMgr();

#endif // GLOBAL_MGR_H