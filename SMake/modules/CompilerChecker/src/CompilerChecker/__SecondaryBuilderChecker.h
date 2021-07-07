#ifndef SECONDARYBUILDER_CHECKER_H
#define SECONDARYBUILDER_CHECKER_H
#include <string>
#include "pump_core/os_wrapper/pump_core_os_types.h"
#include "__CmdService.h"
#include "__CompilerChecker.h"

class CCpuArchInfo;
class CCompilerInfo;
class CCompilerCheckBase;

class CSecondaryBuilderInfo
{
public:
    typedef enum tagSECONDARYBUILDER_TYPE
    {
        SBUILDER_DEFAULT = 0,
        SBUILDER_CMAKE,
    } SECONDARYBUILDER_TYPE;
public:
    CSecondaryBuilderInfo() {}
    CSecondaryBuilderInfo(const CSecondaryBuilderInfo & other)
        : m_emType(other.m_emType)
        , m_objArchinfo(other.m_objArchinfo)
        , m_strBuilderDirPath(other.m_strBuilderDirPath)
        , m_strBuilderExe(other.m_strBuilderExe)
        , m_strBuilderName(other.m_strBuilderName)
        , m_strBuilderVersion(other.m_strBuilderVersion)
    {}
    CSecondaryBuilderInfo & operator=(const CSecondaryBuilderInfo & other)
    {
        m_emType = (other.m_emType);
        m_objArchinfo = (other.m_objArchinfo);
        m_strBuilderDirPath = (other.m_strBuilderDirPath);
        m_strBuilderExe = (other.m_strBuilderExe);
        m_strBuilderName = (other.m_strBuilderName);
        m_strBuilderVersion = (other.m_strBuilderVersion);
        return *this;
    }
    std::string GetID()
    {
        std::string strID;
        return  strID;
    }
    std::string ToString() const
    {
        std::string strInfo;
        strInfo += "{";
        {
            strInfo += "\"SecondaryBuilderType\":";
            switch (m_emType)
            {
            case SBUILDER_CMAKE:
                strInfo += "\"cmake\"";
                break;
            default:
                strInfo += "\"unknown\"";
                break;
            }
        }
        strInfo += ",";
        {// 二级构建工具运行环境CPU架构
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
    SECONDARYBUILDER_TYPE m_emType;
    CCpuArchInfo m_objArchinfo;
    std::string m_strBuilderDirPath;
    std::string m_strBuilderExe;
    std::string m_strBuilderName;
    std::string m_strBuilderVersion;
};

class CSecondaryBuilderCheckBase
{
public:
    explicit CSecondaryBuilderCheckBase(CSecondaryBuilderInfo & builderInfo);
    virtual ~CSecondaryBuilderCheckBase();

    pump_int32_t Check();
protected:
    virtual pump_int32_t __CheckCore() = 0;
    virtual pump_bool_t __PreCheck() = 0;
    virtual pump_bool_t __PostCheck() = 0;
    pump_bool_t __MakeCheckTempDir();

private:
    CSecondaryBuilderCheckBase();
    CSecondaryBuilderCheckBase(const CSecondaryBuilderCheckBase & other);
    CSecondaryBuilderCheckBase & operator=(const CSecondaryBuilderCheckBase & other);
public:
    CSecondaryBuilderInfo & m_builderInfo;
    pump_uint32_t m_dwPassed;
    pump_uint32_t m_dwTotal;
    std::string m_strCheckTempDir;
};

class CSecondaryBuilderDetectBase
{
public:
    CSecondaryBuilderDetectBase();
    CSecondaryBuilderDetectBase(const CSecondaryBuilderDetectBase& other);
    CSecondaryBuilderDetectBase & operator=(const CSecondaryBuilderDetectBase& other);
    virtual ~CSecondaryBuilderDetectBase();
    virtual pump_int32_t Detect() = 0;
public:
    CSecondaryBuilderInfo m_objBuilderInfo;
};

class CCMakeDetect
    : public CSecondaryBuilderDetectBase
{
private:
    class CCMakeCheck
        : public CSecondaryBuilderCheckBase
    {
    public:
        explicit CCMakeCheck(CSecondaryBuilderInfo & builderInfo);
        virtual ~CCMakeCheck();
    protected:
        virtual pump_int32_t __CheckCore();
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
    private:
        //pump_int32_t m_dwGenType; // 0-None, 1-msvc14, 2-msvc12
    };
public:
    explicit CCMakeDetect(const CSecondaryBuilderInfo & refBuiderInfo);
    CCMakeDetect(const CCMakeDetect& other);
    CCMakeDetect & operator=(const CCMakeDetect& other);
    virtual ~CCMakeDetect();
    virtual pump_int32_t Detect();
};

#endif // SECONDARYBUILDER_CHECKER_H