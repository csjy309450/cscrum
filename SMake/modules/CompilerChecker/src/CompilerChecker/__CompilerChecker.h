#ifndef COMPILER_CHECKER_H
#define COMPILER_CHECKER_H
#include <string>
#include <vector>
#include "pump_core/os_wrapper/pump_core_os_types.h"
#include "__CmdService.h"

class CCpuArchInfo;
class CCompilerInfo;
class CCompilerCheckBase;

class CCpuArchInfo
{
public:
    typedef enum tagCPU_ARCH_TYPE
    {
        CPU_ARCH_DEFAULT = 0,
        CPU_ARCH_X86 = 1,
        CPU_ARCH_ARM = 2,
        CPU_ARCH_ALPHA = 3,
        CPU_ARCH_MIPS = 4,
    } CPU_ARCH_TYPE;
    typedef enum tagCPU_BITLONG_TYPE
    {
        CPU_BITLONG_DEFAULT = 0,
        CPU_BITLONG_8 = 1,
        CPU_BITLONG_16 = 2,
        CPU_BITLONG_32 = 3,
        CPU_BITLONG_64 = 4,
    } CPU_BITLONG_TYPE;

public:
    CCpuArchInfo();
    pump_uint16_t GetCpuArchID();
    std::string GetCpuArchString() const;
public:
    CPU_ARCH_TYPE m_emArchType;
    CPU_BITLONG_TYPE m_emBitLong;
};

class CCompilerInfo
{
public:
    typedef enum tagCOMPILER_TYPE
    {
        COMPILER_DEFAULT = 0,
        COMPILER_CL,
        COMPILER_GCC,
        COMPILER_MINGW,
    } COMPILER_TYPE;
    typedef std::vector<std::string> EnvVarType;
public:
    CCompilerInfo();
    ~CCompilerInfo();
    CCompilerInfo(const CCompilerInfo & other);
    CCompilerInfo & operator=(const CCompilerInfo & other);
    const std::string & GetCompilerID() const;
    pump_bool_t SetCompilerEvnVar();
    std::string ToString() const;
public:
    COMPILER_TYPE m_emType;
    CCpuArchInfo m_objHostCpuArchInfo;
    CCpuArchInfo m_objTargetCpuArchInfo;
    std::string m_strCompilerName;
    std::string m_strCompilerDirPath; // ±àÒëÆ÷³ÌÐòËùÔÚÄ¿Â¼
    std::string m_strCompilerExe; // ±àÒëÆ÷³ÌÐò
    std::string m_strCompilerVersion;
    EnvVarType m_vecPathEnv;
    EnvVarType m_vecLibEnv;
    EnvVarType m_vecIncEnv;
};

class CCompilerCheckBase
{
public:
    explicit CCompilerCheckBase(CCompilerInfo & compilerInfo);
    virtual ~CCompilerCheckBase();

    pump_int32_t Check();
protected:
    virtual pump_int32_t __CheckCore() = 0;
    virtual pump_bool_t __PreCheck() = 0;
    virtual pump_bool_t __PostCheck() = 0;
    pump_bool_t __MakeCheckTempDir();

private:
    CCompilerCheckBase();
    CCompilerCheckBase(const CCompilerCheckBase & other);
    CCompilerCheckBase & operator=(const CCompilerCheckBase & other);
public:
    CCompilerInfo & m_compilerInfo;
    pump_uint32_t m_dwPassed;
    pump_uint32_t m_dwTotal;
    std::string m_strCheckTempDir;
};

class CCompilerDetectBase
{
public:
    CCompilerDetectBase();
    CCompilerDetectBase(const CCompilerDetectBase& other);
    CCompilerDetectBase & operator=(const CCompilerDetectBase& other);
    virtual ~CCompilerDetectBase();
    virtual pump_int32_t Detect() = 0;
public:
    CCompilerInfo m_objCompilerInfo;
};

#endif // COMPILER_CHECKER_H