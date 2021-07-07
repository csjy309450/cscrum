#include <conio.h>
#include <map>
#include "pump_core/pump_core_logger.h"
#include "pump_core/pump_core_cmder.h"
#include "pump_core/pump_core_thread.h"
#include "pump_core/os_wrapper/pump_core_os_api.h"
#include "pump_core/pump_core_file.h"
#include "pump_core/pump_core_environment.h"
#include "__GlobalMgr.h"
#include "__PrimaryBuilderChecker.h"
#include "__CodeTemplate.inl"

CPrimaryBuilderCheckBase::CPrimaryBuilderCheckBase(CPrimaryBuilderInfo & builderInfo)
    : m_builderInfo(builderInfo)
    , m_dwTotal(0)
    , m_dwPassed(0)
{

}

CPrimaryBuilderCheckBase::~CPrimaryBuilderCheckBase()
{

}

pump_int32_t CPrimaryBuilderCheckBase::Check()
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

pump_bool_t CPrimaryBuilderCheckBase::__MakeCheckTempDir()
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

CNMakeDetect_14_x86::CNMakeCheck_14::CNMakeCheck_14(CPrimaryBuilderInfo & builderInfo)
    : CPrimaryBuilderCheckBase(builderInfo)
{
}

CNMakeDetect_14_x86::CNMakeCheck_14::~CNMakeCheck_14()
{

}

pump_int32_t CNMakeDetect_14_x86::CNMakeCheck_14::__CheckCore()
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
        char szNamefile[512] = { 0 };
        _snprintf(szNamefile, 511, NMake_SIMPLETEST, m_strCheckTempDir.c_str()
            , m_strCheckTempDir.c_str()
            , m_strCheckTempDir.c_str());
        pump_handle_t hMakefile = PUMP_CORE_FileOpen((m_strCheckTempDir + "Makefile").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hMakefile == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hMakefile, (const pump_pvoid_t)szNamefile, strlen(szNamefile), NULL);
        PUMP_CORE_FileClose(hMakefile);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe;
        strCmdIn += "\" /f \"" + m_strCheckTempDir+"Makefile\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] make failed, err msg: %s", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] make succ", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str());
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

pump_bool_t CNMakeDetect_14_x86::CNMakeCheck_14::__PreCheck()
{
    bool bFind = false;
    CompilerInfoContainer::iterator it = GetGlobalMgr().m_mapCompilerInfo.begin();
    for (; it != GetGlobalMgr().m_mapCompilerInfo.end(); ++it)
    {
        if ((*it).second.m_emType == CCompilerInfo::COMPILER_CL)
        {
            if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
            else if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
        }
    }
    if (bFind)
    {
        (*it).second.SetCompilerEvnVar();
    }
    else
    {
        return PUMP_FALSE;
    }
    return PUMP_TRUE;
}

pump_bool_t CNMakeDetect_14_x86::CNMakeCheck_14::__PostCheck()
{
    return PUMP_TRUE;
}

CMSBuildDetect_14_x86::CMSBuildCheck_14::CMSBuildCheck_14(CPrimaryBuilderInfo & builderInfo)
    : CPrimaryBuilderCheckBase(builderInfo)
{
}

CMSBuildDetect_14_x86::CMSBuildCheck_14::~CMSBuildCheck_14()
{

}

pump_int32_t CMSBuildDetect_14_x86::CMSBuildCheck_14::__CheckCore()
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
        // write HelloWorld.vcxproj
        hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.vcxproj").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)MSBUILD_SIMPLETEST_VCXPROJ, strlen(MSBUILD_SIMPLETEST_VCXPROJ), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        // write HelloWorld.sln
        hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.sln").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)MSBUILD_SIMPLETEST_SLN, strlen(MSBUILD_SIMPLETEST_SLN), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe;
        strCmdIn += "\" \"" + m_strCheckTempDir + "HelloWorld.sln\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CMSBuildDetect_14_x86::CMSBuildCheck_14::__CheckCore() [%s] build failed, err msg: %s", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CMSBuildDetect_14_x86::CMSBuildCheck_14::__CheckCore() [%s] build succ", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "Debug/HelloWorld.exe";
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

pump_bool_t CMSBuildDetect_14_x86::CMSBuildCheck_14::__PreCheck()
{
    bool bFind = false;
    CompilerInfoContainer::iterator it = GetGlobalMgr().m_mapCompilerInfo.begin();
    for (; it != GetGlobalMgr().m_mapCompilerInfo.end(); ++it)
    {
        if ((*it).second.m_emType == CCompilerInfo::COMPILER_CL)
        {
            if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
            else if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
        }
    }
    if (bFind)
    {
        (*it).second.SetCompilerEvnVar();
    }
    else
    {
        return PUMP_FALSE;
    }
    return PUMP_TRUE;
}

pump_bool_t CMSBuildDetect_14_x86::CMSBuildCheck_14::__PostCheck()
{
    return PUMP_TRUE;
}

CBuilderDetectBase::CBuilderDetectBase()
{

}

CBuilderDetectBase::CBuilderDetectBase(const CBuilderDetectBase& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CBuilderDetectBase & CBuilderDetectBase::operator=(const CBuilderDetectBase& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CBuilderDetectBase::~CBuilderDetectBase()
{

}

CNMakeDetect_14_x86::CNMakeDetect_14_x86()
{
    m_objBuilderInfo.m_emType = CPrimaryBuilderInfo::PBUILDER_NMAKE;
    m_objBuilderInfo.m_objArchinfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objBuilderInfo.m_objArchinfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objBuilderInfo.m_strBuilderDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/";
    m_objBuilderInfo.m_strBuilderExe = "nmake.exe";
    m_objBuilderInfo.m_strBuilderName = "nmake-14-x86";
}

CNMakeDetect_14_x86::CNMakeDetect_14_x86(const CNMakeDetect_14_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CNMakeDetect_14_x86 & CNMakeDetect_14_x86::operator=(const CNMakeDetect_14_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CNMakeDetect_14_x86::~CNMakeDetect_14_x86()
{

}

pump_int32_t CNMakeDetect_14_x86::Detect()
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

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strNMakePath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strNMakePath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strNMakePath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objBuilderInfo.m_strBuilderVersion = szFileVersion;
        CNMakeCheck_14 * pRunCheck = new (std::nothrow) CNMakeCheck_14(m_objBuilderInfo);
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
        GetGlobalMgr().m_mapPrimaryBuilderInfo.insert(PrimaryBuilderInfoItem(m_objBuilderInfo.GetID(), m_objBuilderInfo));
    }
    return 0;
}

CMSBuildDetect_14_x86::CMSBuildDetect_14_x86()
{
    m_objBuilderInfo.m_emType = CPrimaryBuilderInfo::PBUILDER_MSBUILD;
    m_objBuilderInfo.m_objArchinfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objBuilderInfo.m_objArchinfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objBuilderInfo.m_strBuilderDirPath = "C:/Program Files (x86)/MSBuild/14.0/Bin/";
    m_objBuilderInfo.m_strBuilderExe = "MSBuild.exe";
    m_objBuilderInfo.m_strBuilderName = "msbuild-14-x86";
}

CMSBuildDetect_14_x86::CMSBuildDetect_14_x86(const CMSBuildDetect_14_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CMSBuildDetect_14_x86 & CMSBuildDetect_14_x86::operator=(const CMSBuildDetect_14_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CMSBuildDetect_14_x86::~CMSBuildDetect_14_x86()
{

}

pump_int32_t CMSBuildDetect_14_x86::Detect()
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

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strNMakePath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strNMakePath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strNMakePath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objBuilderInfo.m_strBuilderVersion = szFileVersion;
        CMSBuildCheck_14 * pRunCheck = new (std::nothrow) CMSBuildCheck_14(m_objBuilderInfo);
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
        GetGlobalMgr().m_mapPrimaryBuilderInfo.insert(PrimaryBuilderInfoItem(m_objBuilderInfo.GetID(), m_objBuilderInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CNMakeDetect_12_x86::CNMakeCheck_12::CNMakeCheck_12(CPrimaryBuilderInfo & builderInfo)
    : CPrimaryBuilderCheckBase(builderInfo)
{
}

CNMakeDetect_12_x86::CNMakeCheck_12::~CNMakeCheck_12()
{

}

pump_int32_t CNMakeDetect_12_x86::CNMakeCheck_12::__CheckCore()
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
        char szNamefile[512] = { 0 };
        _snprintf(szNamefile, 511, NMake_SIMPLETEST, m_strCheckTempDir.c_str()
            , m_strCheckTempDir.c_str()
            , m_strCheckTempDir.c_str());
        pump_handle_t hMakefile = PUMP_CORE_FileOpen((m_strCheckTempDir + "Makefile").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hMakefile == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hMakefile, (const pump_pvoid_t)szNamefile, strlen(szNamefile), NULL);
        PUMP_CORE_FileClose(hMakefile);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe;
        strCmdIn += "\" /f \"" + m_strCheckTempDir + "Makefile\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CClRunCheck::__CheckBaseCompile() [%s] make failed, err msg: %s", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CClRunCheck::__CheckBaseCompile() [%s] make succ", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str());
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

pump_bool_t CNMakeDetect_12_x86::CNMakeCheck_12::__PreCheck()
{
    bool bFind = false;
    CompilerInfoContainer::iterator it = GetGlobalMgr().m_mapCompilerInfo.begin();
    for (; it != GetGlobalMgr().m_mapCompilerInfo.end(); ++it)
    {
        if ((*it).second.m_emType == CCompilerInfo::COMPILER_CL)
        {
            if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
            else if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
        }
    }
    if (bFind)
    {
        (*it).second.SetCompilerEvnVar();
    }
    else
    {
        return PUMP_FALSE;
    }
    return PUMP_TRUE;
}

pump_bool_t CNMakeDetect_12_x86::CNMakeCheck_12::__PostCheck()
{
    return PUMP_TRUE;
}


CNMakeDetect_12_x86::CNMakeDetect_12_x86()
{
    m_objBuilderInfo.m_emType = CPrimaryBuilderInfo::PBUILDER_NMAKE;
    m_objBuilderInfo.m_objArchinfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objBuilderInfo.m_objArchinfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objBuilderInfo.m_strBuilderDirPath = "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/";
    m_objBuilderInfo.m_strBuilderExe = "nmake.exe";
    m_objBuilderInfo.m_strBuilderName = "nmake-12-x86";
}

CNMakeDetect_12_x86::CNMakeDetect_12_x86(const CNMakeDetect_12_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CNMakeDetect_12_x86 & CNMakeDetect_12_x86::operator=(const CNMakeDetect_12_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CNMakeDetect_12_x86::~CNMakeDetect_12_x86()
{

}

pump_int32_t CNMakeDetect_12_x86::Detect()
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

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strNMakePath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 64 bit exe", strNMakePath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strNMakePath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objBuilderInfo.m_strBuilderVersion = szFileVersion;
        CNMakeCheck_12 * pRunCheck = new (std::nothrow) CNMakeCheck_12(m_objBuilderInfo);
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
        GetGlobalMgr().m_mapPrimaryBuilderInfo.insert(PrimaryBuilderInfoItem(m_objBuilderInfo.GetID(), m_objBuilderInfo));
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////////

CMSBuildDetect_12_x86::CMSBuildCheck_12::CMSBuildCheck_12(CPrimaryBuilderInfo & builderInfo)
    : CPrimaryBuilderCheckBase(builderInfo)
{
}

CMSBuildDetect_12_x86::CMSBuildCheck_12::~CMSBuildCheck_12()
{

}

pump_int32_t CMSBuildDetect_12_x86::CMSBuildCheck_12::__CheckCore()
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
        // write HelloWorld.vcxproj
        hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.vcxproj").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)MSBUILD_SIMPLETEST_VCXPROJ, strlen(MSBUILD_SIMPLETEST_VCXPROJ), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        // write HelloWorld.sln
        hCpp = PUMP_CORE_FileOpen((m_strCheckTempDir + "HelloWorld.sln").c_str(), PUMP_CREATE | PUMP_WRITE, PUMP_ATTR_WRITE);
        if (hCpp == PUMP_INVALID_FILE)
        {
            return  PUMP_FALSE;
        }
        ret = PUMP_CORE_FileWrite(hCpp, (const pump_pvoid_t)MSBUILD_SIMPLETEST_SLN, strlen(MSBUILD_SIMPLETEST_SLN), NULL);
        PUMP_CORE_FileClose(hCpp);
        hCpp = PUMP_INVALID_FILE;
        if (ret == PUMP_ERROR)
        {
            return  PUMP_FALSE;
        }
        strCmdIn = "\"";
        strCmdIn += m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe;
        strCmdIn += "\" \"" + m_strCheckTempDir + "HelloWorld.sln\"";
        strCmdOut.clear();
        GetGlobalMgr().m_cmdClient.ExeCmd(strCmdIn.c_str(), strCmdOut);
        if (strCmdOut.find("HelloWorld.cpp") == std::string::npos
            || strCmdOut.find("fatal error") != std::string::npos)
        {
            PUMP_CORE_ERR("CMSBuildDetect_12_x86::CMSBuildCheck_12::__CheckCore() [%s] build failed, err msg: %s",  (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str(), strCmdOut.c_str());
            return PUMP_FALSE;
        }
        else
        {
            PUMP_CORE_INFO("CMSBuildDetect_12_x86::CMSBuildCheck_12::__CheckCore() [%s] build succ", (m_builderInfo.m_strBuilderDirPath + m_builderInfo.m_strBuilderExe).c_str());
        }
        // run HelloWorld.exe
        strCmdIn = m_strCheckTempDir + "Debug/HelloWorld.exe";
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

pump_bool_t CMSBuildDetect_12_x86::CMSBuildCheck_12::__PreCheck()
{
    bool bFind = false;
    CompilerInfoContainer::iterator it = GetGlobalMgr().m_mapCompilerInfo.begin();
    for (; it != GetGlobalMgr().m_mapCompilerInfo.end(); ++it)
    {
        if ((*it).second.m_emType == CCompilerInfo::COMPILER_CL)
        {
            if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
            else if ((*it).second.m_strCompilerDirPath.find("C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin") != std::string::npos)
            {
                bFind = true;
                break;
            }
        }
    }
    if (bFind)
    {
        (*it).second.SetCompilerEvnVar();
    }
    else
    {
        return PUMP_FALSE;
    }
    return PUMP_TRUE;
}

pump_bool_t CMSBuildDetect_12_x86::CMSBuildCheck_12::__PostCheck()
{
    return PUMP_TRUE;
}

CMSBuildDetect_12_x86::CMSBuildDetect_12_x86()
{
    m_objBuilderInfo.m_emType = CPrimaryBuilderInfo::PBUILDER_MSBUILD;
    m_objBuilderInfo.m_objArchinfo.m_emBitLong = CCpuArchInfo::CPU_BITLONG_32;
    m_objBuilderInfo.m_objArchinfo.m_emArchType = CCpuArchInfo::CPU_ARCH_X86;
    m_objBuilderInfo.m_strBuilderDirPath = "C:/Program Files (x86)/MSBuild/12.0/Bin/";
    m_objBuilderInfo.m_strBuilderExe = "MSBuild.exe";
    m_objBuilderInfo.m_strBuilderName = "msbuild-12-x86";
}

CMSBuildDetect_12_x86::CMSBuildDetect_12_x86(const CMSBuildDetect_12_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
}

CMSBuildDetect_12_x86 & CMSBuildDetect_12_x86::operator=(const CMSBuildDetect_12_x86& other)
{
    m_objBuilderInfo = other.m_objBuilderInfo;
    return *this;
}

CMSBuildDetect_12_x86::~CMSBuildDetect_12_x86()
{

}

pump_int32_t CMSBuildDetect_12_x86::Detect()
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

        // 2. check compiler exe arch
        pump_int32_t iArch = PUMP_CORE_GetBinaryFileArch(strNMakePath.c_str());
        if (iArch != 32)
        {
            PUMP_CORE_ERR("[%s] isn't 32 bit exe", strNMakePath.c_str());
            return -1;
        }
        // 3. check compiler version
        char szFileVersion[128] = { 0 };
        if (PUMP_OK != PUMP_CORE_FileProperties(strNMakePath.c_str(), "FileVersion", szFileVersion, sizeof(szFileVersion) - 1))
        {
            return -1;
        }
        m_objBuilderInfo.m_strBuilderVersion = szFileVersion;
        CMSBuildCheck_12 * pRunCheck = new (std::nothrow) CMSBuildCheck_12(m_objBuilderInfo);
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
        GetGlobalMgr().m_mapPrimaryBuilderInfo.insert(PrimaryBuilderInfoItem(m_objBuilderInfo.GetID(), m_objBuilderInfo));
    }
    return 0;
}