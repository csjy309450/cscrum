#include <conio.h>
#include <map>
#include "pump_core/pump_core_logger.h"
#include "pump_core/pump_core_cmder.h"
#include "pump_core/pump_core_thread.h"
#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_file.h"
#include "pump_core/pump_core_environment.h"
#include "__GlobalMgr.h"
#include "__SecondaryBuilderChecker.h"
#include "__CodeTemplate.inl"

CSecondaryBuilderCheckBase::CSecondaryBuilderCheckBase(CSecondaryBuilderInfo & builderInfo)
    : m_builderInfo(builderInfo)
    , m_dwTotal(0)
    , m_dwPassed(0)
{

}

CSecondaryBuilderCheckBase::~CSecondaryBuilderCheckBase()
{

}

pump_int32_t CSecondaryBuilderCheckBase::Check()
{
    if (__MakeCheckTempDir() == PUMP_FALSE)
    {
        return -1;
    }
    if (this->__PreCheck() == PUMP_FALSE)
    {
        return -1;
    }
    pump_int32_t ret = this->__CheckCore();
    if (this->__PostCheck() == PUMP_FALSE)
    {
        return -1;
    }
    return (ret == m_dwTotal ? 0 : -1);
}

pump_bool_t CSecondaryBuilderCheckBase::__MakeCheckTempDir()
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
    strWorkDir += m_builderInfo.m_strBuilderName + "\\";
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

CCMakeDetect::CCMakeCheck::CCMakeCheck(CSecondaryBuilderInfo & builderInfo)
    : CSecondaryBuilderCheckBase(builderInfo)
{
}

CCMakeDetect::CCMakeCheck::~CCMakeCheck()
{

}

pump_int32_t CCMakeDetect::CCMakeCheck::__CheckCore()
{
    m_dwTotal++;
    std::string strCmdIn, strCmdOut;
    {
        // write HelloWorld.cpp
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
        // write CMakeLists.txt
        hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "CMakeLists.txt").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)CMAKE_SIMPLETEST, strlen(CMAKE_SIMPLETEST), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe;
        strCmdIn += "\" \"" + m_strCheckTempDir + "\\\" -B \"" + m_strCheckTempDir + "\\\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("-- Generating done") == std::string::npos
            || strCmdOut.find("-- Configuring done") == std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] gen failed, err msg: %s", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] gen succ", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str());
        }
        ret = PUMP_CORE_DirIsExist((m_strCheckTempDir+"HelloWorld.sln").c_str());
        if (ret==PUMP_OK)
        {
            PUMP_CORE_ERR("[%sHelloWorld.sln] is exist", m_strCheckTempDir.c_str());
        }
        else
        {
            PUMP_CORE_INFO("[%sHelloWorld.sln] isn't exist", m_strCheckTempDir.c_str());
            return PUMP_FALSE;
        }
    }
    m_dwPassed++;
    return PUMP_TRUE;
}

pump_bool_t CCMakeDetect::CCMakeCheck::__PreCheck()
{
    //bool bFind = false;
    //CompilerInfoContainer::iterator it = GetGlobalMgr().m_mapCompilerInfo.begin();
    //for (; it != GetGlobalMgr().m_mapCompilerInfo.end(); ++it)
    //{
    //    if ((*it).second.m_emType == CCompilerInfo::COMPILER_CL)
    //    {
    //        if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin") != std::string::npos)
    //        {
    //            m_dwGenType = 1;
    //            bFind = true;
    //            break;
    //        }
    //        else if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
    //        {
    //            m_dwGenType = 2;
    //            bFind = true;
    //            break;
    //        }
    //    }
    //}
    //if (bFind)
    //{
    //    (*it).second.SetCompilerEvnVar();
    //}
    //else
    //{
    //    return PUMP_FALSE;
    //}
    return PUMP_TRUE;
}

pump_bool_t CCMakeDetect::CCMakeCheck::__PostCheck()
{
    return PUMP_TRUE;
}

CSecondaryBuilderDetectBase::CSecondaryBuilderDetectBase()
{

}

CSecondaryBuilderDetectBase::CSecondaryBuilderDetectBase(const CSecondaryBuilderDetectBase& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CSecondaryBuilderDetectBase & CSecondaryBuilderDetectBase::operator=(const CSecondaryBuilderDetectBase& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CSecondaryBuilderDetectBase::~CSecondaryBuilderDetectBase()
{

}

CCMakeDetect::CCMakeDetect(const CSecondaryBuilderInfo & refBuiderInfo)
{
    m_objBuilderInfo = (refBuiderInfo);
}

CCMakeDetect::CCMakeDetect(const CCMakeDetect& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CCMakeDetect & CCMakeDetect::operator=(const CCMakeDetect& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CCMakeDetect::~CCMakeDetect()
{

}

pump_int32_t CCMakeDetect::Detect()
{
    std::string strNMakePath;
    pump_bool_t ret = PUMP_CORE_DirIsExist(m_objBuilderInfo.m_strBuilderDirPath.c_str());
    if (!ret)
    {
        PUMP_CORE_ERR("[%s] isn't exist", m_objBuilderInfo.m_strBuilderDirPath.c_str());
    }
    else
    {
        PUMP_CORE_INFO("[%s] is exist", m_objBuilderInfo.m_strBuilderDirPath.c_str());
        // 1. check compiler exe
        strNMakePath = m_objBuilderInfo.m_strBuilderDirPath;
        strNMakePath += m_objBuilderInfo.m_strBuilderExe;
        ret = PUMP_CORE_FileIsExist(strNMakePath.c_str());
        if (!ret)
        {
            PUMP_CORE_ERR("[%s] isn't exist", strNMakePath.c_str());
            return -1;
        }
        else
        {
            PUMP_CORE_INFO("[%s] is exist", strNMakePath.c_str());
        }

        //// 2. check compiler exe arch
        //pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strNMakePath.c_str());
        //if (iArch != 32)
        //{
        //    PUMP_CORE_ERR << "[" << strNMakePath.c_str() << "] isn't 32 bit exe";
        //    return -1;
        //}
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strNMakePath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objBuilderInfo.m_strBuilderVersion = szFileVersion;
        CCMakeCheck * pRunCheck = new (std::nothrow) CCMakeCheck(m_objBuilderInfo);
        if (!pRunCheck)
        {
            return -1;
        }
        // 4. compiler run time check
        if (pRunCheck->Check() == -1)
        {
            PUMP_CORE_ERR("[%s] run check failed", strNMakePath.c_str());
            delete pRunCheck;
            return -1;
        }
        delete pRunCheck;
        GetGlobalMgr().m_mapSecondaryBuiderInfo.insert(SecondaryBuilderInfoItem(m_objBuilderInfo.GetID(), m_objBuilderInfo));
    }
    return 0;
}