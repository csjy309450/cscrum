#ifndef CL_CHECKER_H
#define CL_CHECKER_H
#include <string>
#include "pump_core/pump_core_config.h"
#include "pump_core/os_wrapper/pump_core_os_types.h"
#include "__CmdService.h"
#include "__CompilerChecker.h"

class CCpuArchInfo;
class CCompilerInfo;
class CCompilerCheckBase;

#ifdef PUMP_OS_WINDOWS
class CClCheck
    : public CCompilerCheckBase
{
public:
    explicit CClCheck(CCompilerInfo & compilerInfo);
    virtual ~CClCheck();
    CClCheck(CClCheck & other);
    CClCheck & operator=(const CClCheck & other);
protected:
    virtual pump_int32_t __CheckCore();
    virtual pump_bool_t __HelpOutputCheck();
    virtual pump_bool_t __BaseCompileCheck();
};

class CClDetect
    : public CCompilerDetectBase
{
};

class CCl14_x86_x86_Detect
    : public CClDetect
{
private:
        class CCl14_x86_x86_Check
            : public CClCheck
        {
        public:
            explicit CCl14_x86_x86_Check(CCompilerInfo & compilerInfo);
        protected:
            virtual pump_bool_t __PreCheck();
            virtual pump_bool_t __PostCheck();
            virtual pump_bool_t __BaseCompileCheck();
        };
public:
    CCl14_x86_x86_Detect();
    virtual ~CCl14_x86_x86_Detect();
    virtual pump_int32_t Detect();
};

class CCl14_x86_amd64_Detect
    : public CClDetect
{
private:
    class CCl14_x86_amd64_Check
        : public CClCheck
    {
    public:
        explicit CCl14_x86_amd64_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl14_x86_amd64_Detect();
    virtual ~CCl14_x86_amd64_Detect();
    virtual pump_int32_t Detect();
};

class CCl14_x86_arm_Detect
    : public CClDetect
{
private:
    class CCl14_x86_arm_Check
        : public CClCheck
    {
    public:
        explicit CCl14_x86_arm_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl14_x86_arm_Detect();
    virtual ~CCl14_x86_arm_Detect();
    virtual pump_int32_t Detect();
};

class CCl14_amd64_amd64_Detect
    : public CClDetect
{
private:
    class CCl14_amd64_amd64_Check
        : public CClCheck
    {
    public:
        explicit CCl14_amd64_amd64_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl14_amd64_amd64_Detect();
    virtual ~CCl14_amd64_amd64_Detect();
    virtual pump_int32_t Detect();
};

class CCl14_amd64_arm_Detect
    : public CClDetect
{
private:
    class CCl14_amd64_arm_Check
        : public CClCheck
    {
    public:
        explicit CCl14_amd64_arm_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl14_amd64_arm_Detect();
    virtual ~CCl14_amd64_arm_Detect();
    virtual pump_int32_t Detect();
};

class CCl14_amd64_x86_Detect
    : public CClDetect
{
private:
    class CCl14_amd64_x86_Check
        : public CClCheck
    {
    public:
        explicit CCl14_amd64_x86_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl14_amd64_x86_Detect();
    virtual ~CCl14_amd64_x86_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_x86_x86_Detect
    : public CClDetect
{
private:
    class CCl12_x86_x86_Check
        : public CClCheck
    {
    public:
        explicit CCl12_x86_x86_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_x86_x86_Detect();
    virtual ~CCl12_x86_x86_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_x86_amd64_Detect
    : public CClDetect
{
private:
    class CCl12_x86_amd64_Check
        : public CClCheck
    {
    public:
        explicit CCl12_x86_amd64_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_x86_amd64_Detect();
    virtual ~CCl12_x86_amd64_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_x86_arm_Detect
    : public CClDetect
{
private:
    class CCl12_x86_arm_Check
        : public CClCheck
    {
    public:
        explicit CCl12_x86_arm_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_x86_arm_Detect();
    virtual ~CCl12_x86_arm_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_amd64_amd64_Detect
    : public CClDetect
{
private:
    class CCl12_amd64_amd64_Check
        : public CClCheck
    {
    public:
        explicit CCl12_amd64_amd64_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_amd64_amd64_Detect();
    virtual ~CCl12_amd64_amd64_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_amd64_arm_Detect
    : public CClDetect
{
private:
    class CCl12_amd64_arm_Check
        : public CClCheck
    {
    public:
        explicit CCl12_amd64_arm_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_amd64_arm_Detect();
    virtual ~CCl12_amd64_arm_Detect();
    virtual pump_int32_t Detect();
};

class CCl12_amd64_x86_Detect
    : public CClDetect
{
private:
    class CCl12_amd64_x86_Check
        : public CClCheck
    {
    public:
        explicit CCl12_amd64_x86_Check(CCompilerInfo & compilerInfo);
    protected:
        virtual pump_bool_t __PreCheck();
        virtual pump_bool_t __PostCheck();
        virtual pump_bool_t __BaseCompileCheck();
    };
public:
    CCl12_amd64_x86_Detect();
    virtual ~CCl12_amd64_x86_Detect();
    virtual pump_int32_t Detect();
};

#endif // PUMP_OS_WINDOWS
#endif // CL_CHECKER_H