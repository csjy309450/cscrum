#include <time.h>
#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_logger.h"
#include "pump_core/pump_core_file.h"
#include "__GlobalMgr.h"

CompilerCheckerGlobalMgr g_global_mgr;

CompilerCheckerGlobalMgr & GetGlobalMgr()
{
    return g_global_mgr;
}

int CompilerCheckerGlobalMgr::__InitLogger()
{
    PUMP_CORE_LOG_CONF struLogCong;
    memset(&struLogCong, 0, sizeof(struLogCong));
    struLogCong.bPrintConsole = PUMP_TRUE;
    struLogCong.bWriteFile = PUMP_TRUE;
    struLogCong.emLogLevel = PUMP_LOG_INFO;
    strcpy(struLogCong.szFilePath, "smake_log");
    struLogCong.emLogLevel = PUMP_LOG_INFO;
    pump_handle_t hLog = PUMP_CORE_LoggerCreate();
    if (hLog != PUMP_NULL)
    {
        PUMP_CORE_LoggerConfig(hLog, &struLogCong);
        PUMP_CORE_InjectLocalLogger(hLog);
    }
    return  0;
}

pump_int32_t CompilerCheckerGlobalMgr::Init()
{
    __InitLogger();
    GetGlobalMgr().m_thxCmdServer.Start();
    PUMP_CORE_Sleep(1000);
    GetGlobalMgr().m_cmdClient.Open();
    PUMP_CORE_Sleep(1000);
    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::Cleanup()
{
    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::__Init()
{
    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::__Cleanup()
{
    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::CheckCompiler()
{
    // msvc14 detect
    /*PUMP_CORE_INFO(">>>>> CCl14_x86_x86_Detect check <<<<<<");
    CCl14_x86_x86_Detect cl14_x86_x86;
    PUMP_CORE_INFO(">>>>> CCl14_x86_x86_Detect %d <<<<<<",cl14_x86_x86.Detect());

    PUMP_CORE_INFO(">>>>> CCl14_x86_amd64_Detect check <<<<<<");
    CCl14_x86_amd64_Detect cl14_x86_amd64;
    PUMP_CORE_INFO( ">>>>> CCl14_x86_amd64_Detect %d  <<<<<<", cl14_x86_amd64.Detect());

    PUMP_CORE_INFO(">>>>> CCl14_x86_arm_Detect check <<<<<<");
    CCl14_x86_arm_Detect cl14_x86_arm;
    PUMP_CORE_INFO( ">>>>> CCl14_x86_arm_Detect %d <<<<<<", cl14_x86_arm.Detect());

    PUMP_CORE_INFO(">>>>> CCl14_amd64_amd64_Detect check <<<<<<");
    CCl14_amd64_amd64_Detect cl14_amd64_amd64;
    PUMP_CORE_INFO(">>>>> CCl14_amd64_amd64_Detect %d  <<<<<<", cl14_amd64_amd64.Detect());

    PUMP_CORE_INFO(">>>>> CCl14_amd64_x86_Detect check <<<<<<");
    CCl14_amd64_x86_Detect cl14_amd64_x86;
    PUMP_CORE_INFO(">>>>> CCl14_amd64_x86_Detect %d  <<<<<<", cl14_amd64_x86.Detect());

    PUMP_CORE_INFO(">>>>> CCl14_amd64_arm_Detect check <<<<<<");
    CCl14_amd64_arm_Detect cl14_amd64_arm;
    PUMP_CORE_INFO(">>>>> CCl14_amd64_arm_Detect %d <<<<<<", cl14_amd64_arm.Detect());*/

    //msvc12 detect
    PUMP_CORE_INFO(">>>>> CCl12_x86_x86_Detect check <<<<<<");
    CCl12_x86_x86_Detect cl12_x86_x86;
    PUMP_CORE_INFO(">>>>> CCl12_x86_x86_Detect %d <<<<<<", cl12_x86_x86.Detect());

    PUMP_CORE_INFO(">>>>> CCl12_x86_amd64_Detect check <<<<<<");
    CCl12_x86_amd64_Detect cl12_x86_amd64;
    PUMP_CORE_INFO(">>>>> CCl12_x86_amd64_Detect %d <<<<<<", cl12_x86_amd64.Detect());

    PUMP_CORE_INFO(">>>>> CCl12_x86_arm_Detect check <<<<<<");
    CCl12_x86_arm_Detect cl12_x86_arm;
    PUMP_CORE_INFO(">>>>> CCl12_x86_arm_Detect %d <<<<<<", cl12_x86_arm.Detect());

    PUMP_CORE_INFO(">>>>> CCl12_amd64_amd64_Detect check <<<<<<");
    CCl12_amd64_amd64_Detect cl12_amd64_amd64;
    PUMP_CORE_INFO(">>>>> CCl12_amd64_amd64_Detect %d <<<<<<", cl12_amd64_amd64.Detect());

    PUMP_CORE_INFO(">>>>> CCl12_amd64_x86_Detect check <<<<<<");
    CCl12_amd64_x86_Detect cl12_amd64_x86;
    PUMP_CORE_INFO(">>>>> CCl12_amd64_x86_Detect %d <<<<<<", cl12_amd64_x86.Detect());

    PUMP_CORE_INFO(">>>>> CCl12_amd64_arm_Detect check <<<<<<");
    CCl12_amd64_arm_Detect cl12_amd64_arm;
    PUMP_CORE_INFO(">>>>> CCl12_amd64_arm_Detect %d <<<<<<", cl12_amd64_arm.Detect());

    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::CheckPrimaryBuilder()
{
    PUMP_CORE_INFO(">>>>> CNMakeDetect_14_x86 check <<<<<<");
    CNMakeDetect_14_x86 nmake14_x86;
    PUMP_CORE_INFO(">>>>> CNMakeDetect_14_x86 %d <<<<<<", nmake14_x86.Detect());

    PUMP_CORE_INFO(">>>>> CMSBuildDetect_14_x86 check <<<<<<");
    CMSBuildDetect_14_x86 msbuild14_x86;
    PUMP_CORE_INFO(">>>>> CMSBuildDetect_14_x86 %d <<<<<<",msbuild14_x86.Detect());

    PUMP_CORE_INFO(">>>>> CNMakeDetect_12_x86 check <<<<<<");
    CNMakeDetect_12_x86 nmake12_x86;
    PUMP_CORE_INFO(">>>>> CNMakeDetect_12_x86 %d  <<<<<<", nmake12_x86.Detect());

    PUMP_CORE_INFO(">>>>> CMSBuildDetect_12_x86 check <<<<<<");
    CMSBuildDetect_12_x86 msbuild12_x86;
    PUMP_CORE_INFO(">>>>> CMSBuildDetect_12_x86 %d  <<<<<<", msbuild12_x86.Detect());

    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::CheckSecondaryBuilder()
{
    PUMP_CORE_INFO(">>>>> CCMakeDetect check <<<<<<");
    CSecondaryBuilderInfo cmakeInfo;
    cmakeInfo.m_emType = CSecondaryBuilderInfo::SBUILDER_CMAKE;
    cmakeInfo.m_objArchinfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    cmakeInfo.m_objArchinfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    cmakeInfo.m_strBuilderDirPath = "E:/tools/CMake/CMake3_16_2/bin/";
    cmakeInfo.m_strBuilderExe = "cmake.exe";
    cmakeInfo.m_strBuilderName = "cmake-3_16";
    CCMakeDetect cmake_3_16_x86(cmakeInfo);
    PUMP_CORE_INFO(">>>>> CCMakeDetect %d <<<<<<", cmake_3_16_x86.Detect());
    return PUMP_OK;
}

pump_int32_t CompilerCheckerGlobalMgr::WriteFile()
{
    PUMP_CORE_INFO(">>>>> WriteFile in<<<<<<");
    std::string strOut;
    strOut += "{";
    {
        { //添加跟新时间戳
            time_t t;  //秒时间
            tm* local; //本地时间
            char szbuf[128] = { 0 };
            t = ::time(NULL); //获取目前秒时间
            local = ::localtime(&t); //转为本地时间
            ::strftime(szbuf, 128, "%Y-%m-%d %H:%M:%S", local);
            strOut += "\"DateTime\":\"";
            strOut += szbuf;
            strOut += "\"";
        }
        strOut += ",";
        {
            strOut += "\"CompilerInfo\":";
            strOut += "[";
            for (CompilerInfoContainer::const_iterator it = m_mapCompilerInfo.cbegin();
                it != m_mapCompilerInfo.cend();)
            {
                strOut += (*it).second.ToString();
                it++;
                if (it != m_mapCompilerInfo.cend())
                {
                    strOut += ",";
                }
            }
            strOut += "]";
        }
        strOut += ",";
        {
            strOut += "\"PrimaryBuilderInfo\":";
            strOut += "[";
            for (PrimaryBuilderInfoContainer::const_iterator it = m_mapPrimaryBuilderInfo.cbegin();
                it != m_mapPrimaryBuilderInfo.cend();)
            {
                strOut += (*it).second.ToString();
                it++;
                if (it != m_mapPrimaryBuilderInfo.cend())
                {
                    strOut += ",";
                }
            }
            strOut += "]";
        }
        strOut += ",";
        {
            strOut += "\"SecondaryBuilderInfo\":";
            strOut += "[";
            for (SecondaryBuilderInfoContainer::const_iterator it = m_mapSecondaryBuiderInfo.cbegin();
                it != m_mapSecondaryBuiderInfo.cend();)
            {
                strOut += (*it).second.ToString();
                it++;
                if (it != m_mapSecondaryBuiderInfo.cend())
                {
                    strOut += ",";
                }
            }
            strOut += "]";
        }
    }
    strOut += "}";
    pump_uint32_t dwSize;
    pump_handle_t hFile = PUMP_CORE_FileOpen("CompilerInfo.json", PUMP_WRITE | PUMP_CREATE, PUMP_ATTR_WRITE | FILE_FLAG_OVERLAPPED);
    if (hFile == PUMP_INVALID_FILE)
    {
        PUMP_CORE_ERR("create CompilerInfo.json failed");
        return PUMP_ERROR;
    }
    PUMP_CORE_FileWrite(hFile, (void*)strOut.c_str(), strOut.size(), &dwSize);
    PUMP_CORE_INFO(">>>>> WriteFile out<<<<<<");
    return PUMP_OK;
}