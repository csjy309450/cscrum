#ifndef PRIMARYBUILDER_CHECKER_H
#define PRIMARYBUILDER_CHECKER_H
#include <string>
#include "pump_core/os_wrapper/pump_core_os_types.h"
#include "__CmdService.h"
#include "__CompilerChecker.h"

class CCpuArchInfo;
class CCompilerInfo;
class CCompilerCheckBase;

class CPrimaryBuilderInfo
{
public:
    typedef enum tagPRIMARYBUILDER_TYPE
    {
        PBUILDER_DEFAULT = 0,
        PBUILDER_NMAKE,
        PBUILDER_MSBUILD,
    } PRIMARYBUILDER_TYPE;
public:
    std::string GetID()
    {
        std::string strID = m_strBuilderExe + m_strBuilderVersion;
        switch (m_objArchinfo.m_emBitLong)
        {
        case CCpuArchInfo::CPU_BITLONG_32:
            strID += "x86";
            break;
        case CCpuArchInfo::CPU_BITLONG_64:
            strID += "amd64";
            break;
        default:
            break;
        }
        return  strID;
    }
    std::string ToString() const
    {
        std::string strInfo;
        strInfo += "{";
        {
            strInfo += "\"PrimaryBuilderType\":";
            switch (m_emType)
            {
            case PBUILDER_NMAKE:
                strInfo += "\"nmake\"";
                break;
            case PBUILDER_MSBUILD:
                strInfo += "\"msbuild\"";
                break;
            default:
                strInfo += "\"unknown\"";
                break;
            }
        }
        strInfo += ",";
        {// 一级构建工具运行环境CPU架构
            strInfo += "\"ArchInfo\":";
            strInfo += "{";
            strInfo += "\"ArchType\":";
            switch (m_objArchinfo.m_emArchType)
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
            switch (m_objArchinfo.m_emBitLong)
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
            strInfo += "\"BuilderDirPath\":\"" + m_strBuilderDirPath + "\"";
            strInfo += ",";
            strInfo += "\"BuilderExe\":\"" + m_strBuilderExe + "\"";
            strInfo += ",";
            strInfo += "\"BuilderName\":\"" + m_strBuilderName + "\"";
            strInfo += ",";
            strInfo += "\"BuilderVersion\":\"" + m_strBuilderVersion + "\"";
        }
        strInfo += "}";
        return strInfo;
    }
public:
    PRIMARYBUILDER_TYPE m_emType;
    CCpuArchInfo m_objArchinfo;
    std::string m_strBuilderDirPath;
    std::string m_strBuilderExe;
    std::string m_strBuilderName;
    std::string m_strBuilderVersion;
};

class CPrimaryBuilderCheckBase
{
public:
    explicit CPrimaryBuilderCheckBase(CPrimaryBuilderInfo & builderInfo);
    virtual ~CPrimaryBuilderCheckBase();

    pump_int32_t Check();
protected:
    virtual pump_int32_t __CheckCore() = 0;
    virtual pump_bool_t __PreCheck() = 0;
    virtual pump_bool_t __PostCheck() = 0;
    pump_bool_t __MakeCheckTempDir();

private:
    CPrimaryBuilderCheckBase();
    CPrimaryBuilderCheckBase(const CPrimaryBuilderCheckBase & other);
    CPrimaryBuilderCheckBase & operator=(const CPrimaryBuilderCheckBase & other);
public:
    CPrimaryBuilderInfo & m_builderInfo;
    pump_uint32_t m_dwPassed;
    pump_uint32_t m_dwTotal;
    std::string m_strCheckTempDir;
};

class CBuilderDetectBase
{
public:
    CBuilderDetectBase();
    CBuilderDetectBase(const CBuilderDetectBase& other);
    CBuilderDetectBase & operator=(const CBuilderDetectBase& other);
    virtual ~CBuilderDetectBase();
    virtual pump_int32_t Detect() = 0;
public:
    CPrimaryBuilderInfo m_objBuilderInfo;
};

class CNMakeDetect_14_x86
    : public CBuilderDetectBase
{
private:
    class CNMakeCheck_14
        : public CPrimaryBuilderCheckBase
    {
    public:
        explicit CNMakeCheck_14(CPrimaryBuilderInfo & builderInfo);
        virtual ~CNMakeCheck_14();
    protected:
        virtual pump_int32_t __CheckCore();
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
    };
public:
    CNMakeDetect_14_x86();
    CNMakeDetect_14_x86(const CNMakeDetect_14_x86& other);
    CNMakeDetect_14_x86 & operator=(const CNMakeDetect_14_x86& other);
    virtual ~CNMakeDetect_14_x86();
    virtual pump_int32_t Detect();
};

class CNMakeDetect_12_x86
    : public CBuilderDetectBase
{
private:
    class CNMakeCheck_12
        : public CPrimaryBuilderCheckBase
    {
    public:
        explicit CNMakeCheck_12(CPrimaryBuilderInfo & builderInfo);
        virtual ~CNMakeCheck_12();
    protected:
        virtual pump_int32_t __CheckCore();
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
    };
public:
    CNMakeDetect_12_x86();
    CNMakeDetect_12_x86(const CNMakeDetect_12_x86& other);
    CNMakeDetect_12_x86 & operator=(const CNMakeDetect_12_x86& other);
    virtual ~CNMakeDetect_12_x86();
    virtual pump_int32_t Detect();
};

class CMSBuildDetect_14_x86
    : public CBuilderDetectBase
{
private:
    class CMSBuildCheck_14
        : public CPrimaryBuilderCheckBase
    {
    public:
        explicit CMSBuildCheck_14(CPrimaryBuilderInfo & builderInfo);
        virtual ~CMSBuildCheck_14();
    protected:
        virtual pump_int32_t __CheckCore();
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
    };
public:
    CMSBuildDetect_14_x86();
    CMSBuildDetect_14_x86(const CMSBuildDetect_14_x86& other);
    CMSBuildDetect_14_x86 & operator=(const CMSBuildDetect_14_x86& other);
    virtual ~CMSBuildDetect_14_x86();
    virtual pump_int32_t Detect();
};

class CMSBuildDetect_12_x86
    : public CBuilderDetectBase
{
private:
    class CMSBuildCheck_12
        : public CPrimaryBuilderCheckBase
    {
    public:
        explicit CMSBuildCheck_12(CPrimaryBuilderInfo & builderInfo);
        virtual ~CMSBuildCheck_12();
    protected:
        virtual pump_int32_t __CheckCore();
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
    };
public:
    CMSBuildDetect_12_x86();
    CMSBuildDetect_12_x86(const CMSBuildDetect_12_x86& other);
    CMSBuildDetect_12_x86 & operator=(const CMSBuildDetect_12_x86& other);
    virtual ~CMSBuildDetect_12_x86();
    virtual pump_int32_t Detect();
};

#endif // PRIMARYBUILDER_CHECKER_H