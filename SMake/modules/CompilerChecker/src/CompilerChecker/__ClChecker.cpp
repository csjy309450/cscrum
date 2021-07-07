#include <conio.h>
#include <map>
#include "pump_core/pump_core_config.h"
#include "pump_core/pump_core_logger.h"
#include "pump_core/pump_core_cmder.h"
#include "pump_core/pump_core_thread.h"
#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_file.h"
#include "pump_core/pump_core_environment.h"
#include "__ClChecker.h"
#include "__GlobalMgr.h"
#include "__CodeTemplate.inl"

#ifdef PUMP_OS_WINDOWS
CClCheck::CClCheck(CCompilerInfo & compilerInfo)
    : CCompilerCheckBase(compilerInfo)
{}

CClCheck::~CClCheck() {}

pump_int32_t CClCheck::__CheckCore()
{
    __HelpOutputCheck();
    __BaseCompileCheck();
    return m_dwPassed;
}

pump_bool_t CClCheck::__HelpOutputCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" /help";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Microsoft (R) C/C++") == std::string::npos)
        {
            PUMP_CORE_ERR("[%s] isn't correct", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is correct", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
            m_dwPassed++;
            return PUMP_TRUE;
        }
    }
}

pump_bool_t CClCheck::__BaseCompileCheck()
{
    return PUMP_FALSE;
}

CCl14_x86_x86_Detect::CCl14_x86_x86_Check::CCl14_x86_x86_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_x86_x86_Detect::CCl14_x86_x86_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_x86_x86_Detect::CCl14_x86_x86_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_x86_x86_Detect::CCl14_x86_x86_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_x86_arm_Detect::CCl14_x86_arm_Check::CCl14_x86_arm_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_x86_arm_Detect::CCl14_x86_arm_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_x86_arm_Detect::CCl14_x86_arm_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_x86_arm_Detect::CCl14_x86_arm_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"_ARM_WINAPI_PARTITION_DESKTOP_SDK_AVAILABLE\" /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "HelloWorld.exe";
        if (PUMP_CORE_FileIsExist(strCmdIn.c_str()) == PUMP_FALSE)
        {
            PUMP_CORE_ERR("[%s] not exist", strCmdIn.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("[%s] exist", strCmdIn.c_str());
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_x86_amd64_Detect::CCl14_x86_amd64_Check::CCl14_x86_amd64_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_x86_amd64_Detect::CCl14_x86_amd64_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_x86_amd64_Detect::CCl14_x86_amd64_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_x86_amd64_Detect::CCl14_x86_amd64_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut);
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_amd64_amd64_Detect::CCl14_amd64_amd64_Check::CCl14_amd64_amd64_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_amd64_amd64_Detect::CCl14_amd64_amd64_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_amd64_amd64_Detect::CCl14_amd64_amd64_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_amd64_amd64_Detect::CCl14_amd64_amd64_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_amd64_x86_Detect::CCl14_amd64_x86_Check::CCl14_amd64_x86_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_amd64_x86_Detect::CCl14_amd64_x86_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_amd64_x86_Detect::CCl14_amd64_x86_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_amd64_x86_Detect::CCl14_amd64_x86_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_amd64_arm_Detect::CCl14_amd64_arm_Check::CCl14_amd64_arm_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl14_amd64_arm_Detect::CCl14_amd64_arm_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl14_amd64_arm_Detect::CCl14_amd64_arm_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl14_amd64_arm_Detect::CCl14_amd64_arm_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"_ARM_WINAPI_PARTITION_DESKTOP_SDK_AVAILABLE\" /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc140.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "HelloWorld.exe";
        if (PUMP_CORE_FileIsExist(strCmdIn.c_str()) == PUMP_FALSE)
        {
            PUMP_CORE_ERR("[%s] not exist", strCmdIn.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("[%s] exist", strCmdIn.c_str());
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

CCl14_x86_x86_Detect::CCl14_x86_x86_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_strCompilerName = "cl-14-x86_x86";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x86");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x86");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_x86_x86_Detect::~CCl14_x86_x86_Detect()
{}

pump_int32_t CCl14_x86_x86_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_x86_x86_Check * pRunCheck = new (std::nothrow) CCl14_x86_x86_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

CCl14_x86_amd64_Detect::CCl14_x86_amd64_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_strCompilerName = "cl-14-x86_amd64";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x64");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_x86_amd64_Detect::~CCl14_x86_amd64_Detect()
{}

pump_int32_t CCl14_x86_amd64_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_x86_amd64_Check * pRunCheck = new (std::nothrow) CCl14_x86_amd64_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

CCl14_x86_arm_Detect::CCl14_x86_arm_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_ARM;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_DEFAULT;
    m_objCompilerInfo.m_strCompilerName = "cl-14-x86_arm";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_arm/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/arm");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_x86_arm_Detect::~CCl14_x86_arm_Detect()
{}

pump_int32_t CCl14_x86_arm_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_x86_arm_Check * pRunCheck = new (std::nothrow) CCl14_x86_arm_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

CCl14_amd64_amd64_Detect::CCl14_amd64_amd64_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_strCompilerName = "cl-14-amd64_amd64";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x64");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_amd64_amd64_Detect::~CCl14_amd64_amd64_Detect()
{}

pump_int32_t CCl14_amd64_amd64_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_amd64_amd64_Check * pRunCheck = new (std::nothrow) CCl14_amd64_amd64_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

CCl14_amd64_arm_Detect::CCl14_amd64_arm_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_ARM;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_DEFAULT;
    m_objCompilerInfo.m_strCompilerName = "cl-14-amd64_arm";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64_arm/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/arm");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_amd64_arm_Detect::~CCl14_amd64_arm_Detect()
{}

pump_int32_t CCl14_amd64_arm_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_amd64_arm_Check * pRunCheck = new (std::nothrow) CCl14_amd64_arm_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

CCl14_amd64_x86_Detect::CCl14_amd64_x86_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_strCompilerName = "cl-14-amd64_x86";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64_x86/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x86");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x86");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/");
}

CCl14_amd64_x86_Detect::~CCl14_amd64_x86_Detect()
{}

pump_int32_t CCl14_amd64_x86_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl14_amd64_x86_Check * pRunCheck = new (std::nothrow) CCl14_amd64_x86_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////
CCl12_x86_x86_Detect::CCl12_x86_x86_Check::CCl12_x86_x86_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_x86_x86_Detect::CCl12_x86_x86_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_x86_x86_Detect::CCl12_x86_x86_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_x86_x86_Detect::CCl12_x86_x86_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_x86_x86_Detect::CCl12_x86_x86_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_strCompilerName = "cl-12-x86_x86";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Windows/System32/"); // solve error "VS Command Prompt ERROR: Cannot determine the location of the VS Common Tools folder"
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/bin/x86/"); // rc.exe Path
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/Common7/IDE/");
    //
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x86/");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.0/Lib/Win8/um/x86/");
    //
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Include/shared/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Include/um/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Include/winrt/");
    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Windows Kits/8.0/Include/um/");
}

CCl12_x86_x86_Detect::~CCl12_x86_x86_Detect()
{}

pump_int32_t CCl12_x86_x86_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_x86_x86_Check * pRunCheck = new (std::nothrow) CCl12_x86_x86_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CCl12_x86_amd64_Detect::CCl12_x86_amd64_Check::CCl12_x86_amd64_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_x86_amd64_Detect::CCl12_x86_amd64_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_x86_amd64_Detect::CCl12_x86_amd64_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_x86_amd64_Detect::CCl12_x86_amd64_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_x86_amd64_Detect::CCl12_x86_amd64_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_strCompilerName = "cl-12-x86_amd64";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/x86_amd64/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/");

    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x64");

    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
}

CCl12_x86_amd64_Detect::~CCl12_x86_amd64_Detect()
{}

pump_int32_t CCl12_x86_amd64_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_x86_amd64_Check * pRunCheck = new (std::nothrow) CCl12_x86_amd64_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CCl12_x86_arm_Detect::CCl12_x86_arm_Check::CCl12_x86_arm_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_x86_arm_Detect::CCl12_x86_arm_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_x86_arm_Detect::CCl12_x86_arm_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_x86_arm_Detect::CCl12_x86_arm_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"_ARM_WINAPI_PARTITION_DESKTOP_SDK_AVAILABLE\" /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "HelloWorld.exe";
        if (PUMP_CORE_FileIsExist(strCmdIn.c_str()) == PUMP_FALSE)
        {
            PUMP_CORE_ERR("[%s] not exist, console err msg: %s", strCmdIn.c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("[%s] exist", strCmdIn.c_str());
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_x86_arm_Detect::CCl12_x86_arm_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_ARM;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_DEFAULT;
    m_objCompilerInfo.m_strCompilerName = "cl-12-x86_arm";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/x86_arm/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/");

    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/arm");

    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
}

CCl12_x86_arm_Detect::~CCl12_x86_arm_Detect()
{}

pump_int32_t CCl12_x86_arm_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_x86_arm_Check * pRunCheck = new (std::nothrow) CCl12_x86_arm_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CCl12_amd64_amd64_Detect::CCl12_amd64_amd64_Check::CCl12_amd64_amd64_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_amd64_amd64_Detect::CCl12_amd64_amd64_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_amd64_amd64_Detect::CCl12_amd64_amd64_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_amd64_amd64_Detect::CCl12_amd64_amd64_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_amd64_amd64_Detect::CCl12_amd64_amd64_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_strCompilerName = "cl-12-amd64_amd64";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/amd64/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);

    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib/amd64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x64");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x64");

    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
}

CCl12_amd64_amd64_Detect::~CCl12_amd64_amd64_Detect()
{}

pump_int32_t CCl12_amd64_amd64_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_amd64_amd64_Check * pRunCheck = new (std::nothrow) CCl12_amd64_amd64_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CCl12_amd64_arm_Detect::CCl12_amd64_arm_Check::CCl12_amd64_arm_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_amd64_arm_Detect::CCl12_amd64_arm_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_amd64_arm_Detect::CCl12_amd64_arm_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_amd64_arm_Detect::CCl12_amd64_arm_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"_ARM_WINAPI_PARTITION_DESKTOP_SDK_AVAILABLE\" /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "HelloWorld.exe";
        if (PUMP_CORE_FileIsExist(strCmdIn.c_str()) == PUMP_FALSE)
        {
            PUMP_CORE_ERR("[%s] not exist", strCmdIn.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("[%s] exist", strCmdIn.c_str());
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_amd64_arm_Detect::CCl12_amd64_arm_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_ARM;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_DEFAULT;
    m_objCompilerInfo.m_strCompilerName = "cl-12-amd64_arm";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/amd64_arm/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/amd64");

    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/arm");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/arm");

    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
}

CCl12_amd64_arm_Detect::~CCl12_amd64_arm_Detect()
{}

pump_int32_t CCl12_amd64_arm_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_amd64_arm_Check * pRunCheck = new (std::nothrow) CCl12_amd64_arm_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CCl12_amd64_x86_Detect::CCl12_amd64_x86_Check::CCl12_amd64_x86_Check(CCompilerInfo & compilerInfo)
    : CClCheck(compilerInfo)
{

}

pump_bool_t CCl12_amd64_x86_Detect::CCl12_amd64_x86_Check::__PreCheck()
{
    return m_compilerInfo.SetCompilerEvnVar();
}

pump_bool_t CCl12_amd64_x86_Detect::CCl12_amd64_x86_Check::__PostCheck()
{
    return PUMP_TRUE;
}

pump_bool_t CCl12_amd64_x86_Detect::CCl12_amd64_x86_Check::__BaseCompileCheck()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        pump_handle_t hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.cpp").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        pump_int32_t ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CXX_COMPILER_SIMPLETEST, strlen(CXX_COMPILER_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe;
        strCmdIn += "\" " + m_strCheckTempDir + "HelloWorld.cpp";
        strCmdIn += " /GS /TP /W3 /Zi /Gm- /Od /Ob0 /fp:precise /D \"WIN32\" /D \"_WINDOWS\" /D \"_C RT_SECURE_NO_WARNINGS \" /D \"CMAKE_INTDIR=\\\"Debug\\\"\" /D \"_MBCS\" /errorReport:prompt /WX- /Zc:forScope /RTC1 /GR /Gd /Oy- /MDd /EHsc /nologo";
        strCmdIn += " /Fa\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fo\"" + m_strCheckTempDir + "\\\"";
        strCmdIn += " /Fd\"" + m_strCheckTempDir + "vc120.pdb\"";
        strCmdIn += " /link /OUT:";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe \"kernel32.Lib\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } failed, err msg: %s", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] compile { main.cpp } succ", (m_compilerInfo.m_strCompilerDirPath + m_compilerInfo.m_strCompilerExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = "\"";
        strCmdIn += m_strCheckTempDir + "HelloWorld.exe";
        strCmdIn += "\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("Hello world!") == std::string::npos)
        {
            PUMP_CORE_ERR("run main.exe failed, err msg: %s", strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("run main.exe succ");
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}


CCl12_amd64_x86_Detect::CCl12_amd64_x86_Detect()
{
    m_objCompilerInfo.m_emType = CCompilerInfo::COMPILER_CL;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objHostCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_64;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objCompilerInfo.m_objTargetCpuArchInfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objCompilerInfo.m_strCompilerName = "cl-12-amd64_x86";
    m_objCompilerInfo.m_strCompilerDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/amd64_x86/";
    m_objCompilerInfo.m_strCompilerExe = "cl.exe";
    m_objCompilerInfo.m_vecPathEnv.push_back(m_objCompilerInfo.m_strCompilerDirPath);
    m_objCompilerInfo.m_vecPathEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/amd64");

    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Lib");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.10240.0/ucrt/x86");
    m_objCompilerInfo.m_vecLibEnv.push_back("C:/Program Files (x86)/Windows Kits/8.1/Lib/winv6.3/um/x86");

    m_objCompilerInfo.m_vecIncEnv.push_back("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include/");
}

CCl12_amd64_x86_Detect::~CCl12_amd64_x86_Detect()
{}

pump_int32_t CCl12_amd64_x86_Detect::Detect()
{
    std::string strCompilerPath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objCompilerInfo.m_strCompilerDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objCompilerInfo.m_strCompilerDirPath.c_str());
        // 1. check compiler exe
        strCompilerPath = m_objCompilerInfo.m_strCompilerDirPath;
        strCompilerPath += m_objCompilerInfo.m_strCompilerExe;
        ret = PUMP_CORE_FileIsExist(strCompilerPath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strCompilerPath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strCompilerPath.c_str());
        }

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strCompilerPath.c_str());
        if (iArch != 64)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strCompilerPath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strCompilerPath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objCompilerInfo.m_strCompilerVersion = szFileVersion;
        CCl12_amd64_x86_Check * pRunCheck = new (std::nothrow) CCl12_amd64_x86_Check(m_objCompilerInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strCompilerPath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapCompilerInfo.insert(CompilerInfoItem(m_objCompilerInfo.GetCompilerID(), m_objCompilerInfo));
    }
    return 0;
}

#endif // PUMP_OS_WINDOWS

//int CheckMsvcCl12()
//{
//    const char* kMsvc14Dir = "C:/Program Files (x86)/Microsoft Visual Studio 14.0";
//    const char* kmsvc14_cl_default = "/VC/bin/cl.exe";
//    const char* kmsvc14_cl_x86_arm = "/VC/bin/x86_arm/cl.exe";
//    const char* kmsvc14_cl_x86_amd64 = "/VC/bin/x86_amd64/cl.exe";
//
//    std::string strBuff;
//    pump_bool_t ret = PUMP_CORE_DirIsExist(kMsvc14Dir);
//    if (!ret)
//    {
//        PUMP_CORE_ERR << "[" << kMsvc14Dir << "] isn't exist";
//    }
//    else
//    {
//        PUMP_CORE_INFO << "[" << kMsvc14Dir << "] is exist";
//
//        strBuff = kMsvc14Dir;
//        strBuff += kmsvc14_cl_default;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc14Dir << kmsvc14_cl_default << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc14Dir << kmsvc14_cl_default << "] is exist";
//        }
//
//        strBuff = kMsvc14Dir;
//        strBuff += kmsvc14_cl_x86_arm;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc14Dir << kmsvc14_cl_x86_arm << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc14Dir << kmsvc14_cl_x86_arm << "] is exist";
//        }
//
//        strBuff = kMsvc14Dir;
//        strBuff += kmsvc14_cl_x86_amd64;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc14Dir << kmsvc14_cl_x86_amd64 << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc14Dir << kmsvc14_cl_x86_amd64 << "] is exist";
//        }
//    }
//    return 0;
//}
//
//int CheckMsvcNMake12()
//{
//    const char* kMsvc12Dir = "C:/Program Files (x86)/Microsoft Visual Studio 12.0";
//    const char* kmsvc12_nmake_default = "/VC/bin/nmake.exe";
//    const char* kmsvc12_nmake_amd64 = "/VC/bin/amd64/nmake.exe";
//
//    std::string strBuff;
//    pump_bool_t ret = PUMP_CORE_DirIsExist(kMsvc12Dir);
//    if (!ret)
//    {
//        PUMP_CORE_ERR << "[" << kMsvc12Dir << "] isn't exist";
//    }
//    else
//    {
//        PUMP_CORE_INFO << "[" << kMsvc12Dir << "] is exist";
//
//        strBuff = kMsvc12Dir;
//        strBuff += kmsvc12_nmake_default;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc12Dir << kmsvc12_nmake_default << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc12Dir << kmsvc12_nmake_default << "] is exist";
//        }
//
//        strBuff = kMsvc12Dir;
//        strBuff += kmsvc12_nmake_amd64;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc12Dir << kmsvc12_nmake_amd64 << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc12Dir << kmsvc12_nmake_amd64 << "] is exist";
//        }
//    }
//    return 0;
//}
//
//int CheckMsvcNMake14()
//{
//    const char* kMsvc14Dir = "C:/Program Files (x86)/Microsoft Visual Studio 14.0";
//    const char* kmsvc14_nmake_default = "/VC/bin/nmake.exe";
//    const char* kmsvc14_nmake_amd64 = "/VC/bin/amd64/nmake.exe";
//
//    std::string strBuff;
//    pump_bool_t ret = PUMP_CORE_DirIsExist(kMsvc14Dir);
//    if (!ret)
//    {
//        PUMP_CORE_ERR << "[" << kMsvc14Dir << "] isn't exist";
//    }
//    else
//    {
//        PUMP_CORE_INFO << "[" << kMsvc14Dir << "] is exist";
//
//        strBuff = kMsvc14Dir;
//        strBuff += kmsvc14_nmake_default;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc14Dir << kmsvc14_nmake_default << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc14Dir << kmsvc14_nmake_default << "] is exist";
//        }
//
//        strBuff = kMsvc14Dir;
//        strBuff += kmsvc14_nmake_amd64;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvc14Dir << kmsvc14_nmake_amd64 << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvc14Dir << kmsvc14_nmake_amd64 << "] is exist";
//        }
//    }
//    return 0;
//}
//
//int CheckMsvcMSBuild12()
//{
//    const char* kMsvcBuild12Dir = "C:/Program Files (x86)/MSBuild/12.0";
//    const char* kmsvc12_msbuild_default = "/Bin/MSBuild.exe";
//
//    std::string strBuff;
//    pump_bool_t ret = PUMP_CORE_DirIsExist(kMsvcBuild12Dir);
//    if (!ret)
//    {
//        PUMP_CORE_ERR << "[" << kMsvcBuild12Dir << "] isn't exist";
//    }
//    else
//    {
//        PUMP_CORE_INFO << "[" << kMsvcBuild12Dir << "] is exist";
//
//        strBuff = kMsvcBuild12Dir;
//        strBuff += kmsvc12_msbuild_default;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvcBuild12Dir << kmsvc12_msbuild_default << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvcBuild12Dir << kmsvc12_msbuild_default << "] is exist";
//        }
//    }
//    return 0;
//}
//
//int CheckMsvcMSBuild14()
//{
//    const char* kMsvcBuild14Dir = "C:/Program Files (x86)/MSBuild/14.0";
//    const char* kmsvc14_msbuild_default = "/Bin/MSBuild.exe";
//
//    std::string strBuff;
//    pump_bool_t ret = PUMP_CORE_DirIsExist(kMsvcBuild14Dir);
//    if (!ret)
//    {
//        PUMP_CORE_ERR << "[" << kMsvcBuild14Dir << "] isn't exist";
//    }
//    else
//    {
//        PUMP_CORE_INFO << "[" << kMsvcBuild14Dir << "] is exist";
//
//        strBuff = kMsvcBuild14Dir;
//        strBuff += kmsvc14_msbuild_default;
//        ret = PUMP_CORE_FileIsExist(strBuff.c_str());
//        if (!ret)
//        {
//            PUMP_CORE_ERR << "[" << kMsvcBuild14Dir << kmsvc14_msbuild_default << "] isn't exist";
//        }
//        else
//        {
//            PUMP_CORE_INFO << "[" << kMsvcBuild14Dir << kmsvc14_msbuild_default << "] is exist";
//        }
//    }
//    return 0;
//}
//