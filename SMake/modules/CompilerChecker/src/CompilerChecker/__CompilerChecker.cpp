#include <conio.h>
#include <map>
#include "pump_core/pump_core_logger.h"
#include "pump_core/pump_core_cmder.h"
#include "pump_core/pump_core_thread.h"
#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_file.h"
#include "pump_core/pump_core_environment.h"
#include "__ClChecker.h"
#include "__GlobalMgr.h"

CCpuArchInfo::CCpuArchInfo()
    : m_emArchType(CPU_ARCH_DEFAULT)
    , m_emBitLong(CPU_BITLONG_DEFAULT)
{

}

pump_uint16_t CCpuArchInfo::GetCpuArchID()
{
    pump_uint8_t byArch = (pump_uint8_t)m_emArchType;
    pump_uint8_t byBitLong = (pump_uint8_t)m_emBitLong;
    pump_uint16_t sID = byArch;
    sID <<= 8;
    sID += byBitLong;
    return sID;
}

std::string CCpuArchInfo::GetCpuArchString() const
{
    std::string strArch;
    switch (m_emArchType)
    {
    case CPU_ARCH_X86:
        strArch += "x86";
        break;
    case CPU_ARCH_ARM:
        strArch += "arm";
        break;
    case CPU_ARCH_ALPHA:
        strArch += "alpha";
        break;
    case CPU_ARCH_MIPS:
        strArch += "mips";
        break;
    default:
        break;
    }
    switch (m_emBitLong)
    {
    case CPU_BITLONG_8:
        strArch += "_8";
        break;
    case CPU_BITLONG_16:
        strArch += "_16";
        break;
    case CPU_BITLONG_32:
        strArch += "_32";
        break;
    case CPU_BITLONG_64:
        strArch += "_64";
        break;
    default:
        break;
    }
    return strArch;
}

CCompilerInfo::CCompilerInfo() 
    : m_emType(CCompilerInfo::COMPILER_DEFAULT)
{
}

CCompilerInfo::~CCompilerInfo(){}

CCompilerInfo::CCompilerInfo(const CCompilerInfo & other)
{
    m_emType = other.m_emType;
    m_objHostCpuArchInfo = other.m_objHostCpuArchInfo;
    m_objTargetCpuArchInfo = other.m_objTargetCpuArchInfo;
    m_strCompilerName = other.m_strCompilerName;
    m_strCompilerDirPath = other.m_strCompilerDirPath;
    m_strCompilerExe = other.m_strCompilerExe;
    m_strCompilerVersion = other.m_strCompilerVersion;
    m_vecPathEnv = other.m_vecPathEnv;
    m_vecLibEnv = other.m_vecLibEnv;
    m_vecIncEnv = other.m_vecIncEnv;
}

CCompilerInfo & CCompilerInfo::operator=(const CCompilerInfo & other)
{
    m_emType = other.m_emType;
    m_objHostCpuArchInfo = other.m_objHostCpuArchInfo;
    m_objTargetCpuArchInfo = other.m_objTargetCpuArchInfo;
    m_strCompilerName = other.m_strCompilerName;
    m_strCompilerDirPath = other.m_strCompilerDirPath;
    m_strCompilerExe = other.m_strCompilerExe;
    m_strCompilerVersion = other.m_strCompilerVersion;
    m_vecPathEnv = other.m_vecPathEnv;
    m_vecLibEnv = other.m_vecLibEnv;
    m_vecIncEnv = other.m_vecIncEnv;
    return *this;
}

const std::string & CCompilerInfo::GetCompilerID() const
{
    return m_strCompilerName;
}

pump_bool_t CCompilerInfo::SetCompilerEvnVar()
{
    ::Pump::Core::CEnvVarSet envVarSet;
    GetGlobalMgr().m_env.GetForEnvVarSet(envVarSet);
    // set %PATH% env var
    CCmdUpdateEnvVar updateEnvVar(GetGlobalMgr().m_cmdClient);
    std::string strOut;
    GetGlobalMgr().m_env.GetForEnvVarSet(envVarSet);
    ::Pump::Core::CEnvVarSet::IteratorType itPath = envVarSet.Find("Path");
    if (itPath == envVarSet.End())
    {
        itPath = envVarSet.Find("PATH");
        if (itPath == envVarSet.End())
        {
            PUMP_CORE_ERR("%%PATH%% not exist");
            return PUMP_FALSE;
        }
    }
    itPath->second.clear();
    for (CCompilerInfo::EnvVarType::const_iterator it = m_vecPathEnv.cbegin();
        it != m_vecPathEnv.cend(); ++it)
    {
        itPath->second.insert(*it);
    }
    updateEnvVar.UpdatePath(envVarSet, strOut);
    GetGlobalMgr().m_cmdClient.ExeCmd("echo %PATH%", strOut);
    PUMP_CORE_INFO("%s", strOut.c_str());

    // set %LIB% env var
    strOut.clear();
    itPath = envVarSet.Find("Lib");
    if (itPath == envVarSet.End())
    {
        itPath = envVarSet.Find("LIB");
        if (itPath == envVarSet.End())
        {
            envVarSet.Insert("LIB");
            itPath = envVarSet.Find("LIB");
            if (itPath == envVarSet.End())
            {
                envVarSet.Insert("LIB");
                PUMP_CORE_ERR("%%LIB%% not exist");
                return PUMP_FALSE;
            }
        }
    }
    itPath->second.clear();
    //// DONE 20200517 should add these env var into CCompilerInfo 
    for (CCompilerInfo::EnvVarType::const_iterator it = m_vecLibEnv.cbegin();
        it != m_vecLibEnv.cend(); ++it)
    {
        itPath->second.insert(*it);
    }
    updateEnvVar.UpdateLib(envVarSet, strOut);
    GetGlobalMgr().m_cmdClient.ExeCmd("echo %LIB%", strOut);
    PUMP_CORE_INFO("%s", strOut.c_str());

    // set %INCLUDE% env var
    strOut.clear();
    itPath = envVarSet.Find("INCLUDE");
    if (itPath == envVarSet.End())
    {
        itPath = envVarSet.Find("INCLUDE");
        if (itPath == envVarSet.End())
        {
            envVarSet.Insert("INCLUDE");
            itPath = envVarSet.Find("INCLUDE");
            if (itPath == envVarSet.End())
            {
                PUMP_CORE_ERR("%%INCLUDE%% not exist");
                return PUMP_FALSE;
            }
        }
    }
    itPath->second.clear();
    for (CCompilerInfo::EnvVarType::const_iterator it = m_vecIncEnv.cbegin();
        it != m_vecIncEnv.cend(); ++it)
    {
        itPath->second.insert(*it);
    }
    updateEnvVar.UpdateInc(envVarSet, strOut);
    GetGlobalMgr().m_cmdClient.ExeCmd("echo %INCLUDE%", strOut);
    PUMP_CORE_INFO("%s", strOut.c_str());
    return PUMP_TRUE;
}

std::string CCompilerInfo::ToString() const
{
    std::string strInfo;
    strInfo = "{";
    { // 编译器种类
        strInfo += "\"CompilerType\":";
        switch (m_emType)
        {
        case COMPILER_CL:
            strInfo += "\"cl\"";
            break;
        case COMPILER_GCC:
            strInfo += "\"gcc\"";
            break;
        case COMPILER_MINGW:
            strInfo += "\"mingw\"";
            break;
        default:
            strInfo += "\"unknown\"";
            break;
        }
        // 编译器名
        strInfo += ",";
        strInfo += "\"CompilerName\":\"" + m_strCompilerName + "\"";
    }
    strInfo += ",";
    { // 编译环境CPU架构
        strInfo += "\"HostCpuArchInfo\":";
        strInfo += "{";
        strInfo += "\"ArchType\":";
        switch (m_objHostCpuArchInfo.m_emArchType)
        {
        case CCpuArchInfo::CPU_ARCH_X86:
            strInfo += "\"x86\"";
            break;
        case CCpuArchInfo::CPU_ARCH_ARM:
            strInfo += "\"arm\"";
            break;
        case CCpuArchInfo::CPU_ARCH_ALPHA:
            strInfo += "\"alpha\"";
            break;
        case CCpuArchInfo::CPU_ARCH_MIPS:
            strInfo += "\"mips\"";
            break;
        default:
            strInfo += "\"unknown\"";
            break;
        }
        strInfo += ",";
        strInfo += "\"BitLong\":";
        switch (m_objHostCpuArchInfo.m_emBitLong)
        {
        case CCpuArchInfo::CPU_BITLONG_8:
            strInfo += "8";
            break;
        case CCpuArchInfo::CPU_BITLONG_16:
            strInfo += "16";
            break;
        case CCpuArchInfo::CPU_BITLONG_32:
            strInfo += "32";
            break;
        case CCpuArchInfo::CPU_BITLONG_64:
            strInfo += "64";
            break;
        default:
            strInfo += "-1";
            break;
        }
        strInfo += "}";
    }
    strInfo += ",";
     { // 目标环境CPU架构
         strInfo += "\"TargetCpuArchInfo\":";
         strInfo += "{";
         strInfo += "\"ArchType\":";
         switch (m_objTargetCpuArchInfo.m_emArchType)
         {
         case CCpuArchInfo::CPU_ARCH_X86:
             strInfo += "\"x86\"";
             break;
         case CCpuArchInfo::CPU_ARCH_ARM:
             strInfo += "\"arm\"";
             break;
         case CCpuArchInfo::CPU_ARCH_ALPHA:
             strInfo += "\"alpha\"";
             break;
         case CCpuArchInfo::CPU_ARCH_MIPS:
             strInfo += "\"mips\"";
             break;
         default:
             strInfo += "\"unknown\"";
             break;
         }
         strInfo += ",";
         strInfo += "\"BitLong\":";
         switch (m_objTargetCpuArchInfo.m_emBitLong)
         {
         case CCpuArchInfo::CPU_BITLONG_8:
             strInfo += "8";
             break;
         case CCpuArchInfo::CPU_BITLONG_16:
             strInfo += "16";
             break;
         case CCpuArchInfo::CPU_BITLONG_32:
             strInfo += "32";
             break;
         case CCpuArchInfo::CPU_BITLONG_64:
             strInfo += "64";
             break;
         default:
             strInfo += "-1";
             break;
         }
         strInfo += "}";
     }
     strInfo += ",";
     {
         strInfo += "\"CompilerDirPath\":\"" + m_strCompilerDirPath + "\"";
         strInfo += ",";
         strInfo += "\"CompilerExe\":\"" + m_strCompilerExe + "\"";
         strInfo += ",";
         strInfo += "\"CompilerVersion\":\"" + m_strCompilerVersion + "\"";
     }
     strInfo += ",";
     {
         strInfo += "\"Evn\":";
         strInfo += "{";
         {
             strInfo += "\"PathEvn\":";
             strInfo += "[";
             for (EnvVarType::const_iterator it = m_vecPathEnv.cbegin();;)
             {
                 strInfo += "\"" + *it + "\"";
                 it++;
                 if (it == m_vecPathEnv.cend())
                 {
                     break;
                 }
                 strInfo += ",";
             }
             strInfo += "]";
         }
         strInfo += ",";
         {
             strInfo += "\"LibEvn\":";
             strInfo += "[";
             for (EnvVarType::const_iterator it = m_vecLibEnv.cbegin();;)
             {
                 strInfo += "\"" + *it + "\"";
                 it++;
                 if (it == m_vecLibEnv.cend())
                 {
                     break;
                 }
                 strInfo += ",";
             }
             strInfo += "]";
         }
         strInfo += ",";
         {
             strInfo += "\"IncludeEnv\":";
             strInfo += "[";
             for (EnvVarType::const_iterator it = m_vecIncEnv.cbegin(); it != m_vecIncEnv.cend();)
             {
                 strInfo += "\"" + *it + "\"";
                 it++;
                 if (it == m_vecIncEnv.cend())
                 {
                     break;
                 }
                 strInfo += ",";
             }
             strInfo += "]";
         }
         strInfo += "}";
     }
     strInfo += "}";
     return strInfo;
}

CCompilerCheckBase::CCompilerCheckBase(CCompilerInfo & compilerInfo)
    : m_compilerInfo(compilerInfo)
    , m_dwPassed(0)
    , m_dwTotal(0) {}

CCompilerCheckBase::~CCompilerCheckBase() {}

pump_int32_t CCompilerCheckBase::Check()
{
    if (__MakeCheckTempDir() == PUMP_FALSE)
    {
        return -1;
    }
    if (this->__PreCheck()==PUMP_FALSE)
    {
        return -1;
    }
    pump_int32_t ret = this->__CheckCore();
    if (this->__PostCheck() == PUMP_FALSE)
    {
        return -1;
    }
    return (ret == m_dwTotal?0:-1);
}

pump_bool_t CCompilerCheckBase::__MakeCheckTempDir()
{
    std::string strWorkDir;
    char szWorkDir[256] = { 0 };
    PUMP_CORE_GetWorkDir(szWorkDir, sizeof(szWorkDir));
    strWorkDir = szWorkDir;
    std::string::size_type pos = strWorkDir.find_last_of("\\");
    if (pos == std::string::npos)
    {
        return PUMP_FALSE;
    }
    strWorkDir = strWorkDir.substr(0, pos + 1);
    strWorkDir += "CheckTempDir\\";
    pump_handle_t hTempDir = PUMP_CORE_DirOpen(strWorkDir.c_str());
    if (hTempDir == PUMP_INVALID_HANDLE)
    {
        if (PUMP_CORE_DirCreate(strWorkDir.c_str()) != PUMP_OK)
        {
            return PUMP_FALSE;
        }
    }
    PUMP_CORE_DirClose(hTempDir);
    strWorkDir += m_compilerInfo.m_strCompilerName/* m_compilerInfo.m_objHostCpuArchInfo.GetCpuArchString() + "__" + m_compilerInfo.m_objTargetCpuArchInfo.GetCpuArchString()*/ + "\\";
    m_strCheckTempDir = strWorkDir;
    hTempDir = PUMP_CORE_DirOpen(m_strCheckTempDir.c_str());
    if (hTempDir == PUMP_INVALID_HANDLE)
    {
        if (PUMP_CORE_DirCreate(m_strCheckTempDir.c_str()) != PUMP_OK)
        {
            return PUMP_FALSE;
        }
    }
    return PUMP_TRUE;
}

CCompilerDetectBase::CCompilerDetectBase()
    : m_objCompilerInfo()
{
}

CCompilerDetectBase::CCompilerDetectBase(const CCompilerDetectBase& other)
    : m_objCompilerInfo(other.m_objCompilerInfo)
{

}

CCompilerDetectBase & CCompilerDetectBase::operator=(const CCompilerDetectBase& other)
{
    m_objCompilerInfo = (other.m_objCompilerInfo);
    return *this;
}

CCompilerDetectBase::~CCompilerDetectBase()
{
}