#ifndef CMD_SERVICE_H
#define CMD_SERVICE_H
#include <string>
#include "pump_core/pump_core_cmder.h"
#include "pump_core/pump_core_thread.h"
#include "pump_core/pump_core_environment.h"

class CThxCmdServer
    : public ::Pump::Core::Thread::CThread
{
private:
    virtual pump_void_t * ThreadCallback(pump_void_t * pData);
private:
    ::Pump::Core::Cmder::CCmderServer m_cmdServer;
};

class CTestCmdClient
    : public ::Pump::Core::Cmder::CCmderClient
{
private:
    virtual pump_void_t ReadCallback(pump_uint32_t iCBType, const char * szBuff, pump_uint32_t dwSize, pump_pvoid_t pdata);
};

class CUserCmdClient
{
public:
    pump_int32_t Open();
    pump_int32_t ExeCmd(const char* cmd, std::string & strOut);
private:
    CTestCmdClient m_cmdClient;
};

class CCmdUpdateEnvVar
{
public:
    CCmdUpdateEnvVar(
        CUserCmdClient & cmdClient)
        : m_cmdClient(cmdClient)
    {}
    ~CCmdUpdateEnvVar() {}
    pump_int32_t UpdatePath(::Pump::Core::CEnvVarSet & envVarSet, std::string & strOut)
    {
        if (envVarSet.Size() == 0)
        {
            return PUMP_ERROR;
        }
        std::string strCmd;
        this->__SerializePath(envVarSet, strCmd);
        return m_cmdClient.ExeCmd(strCmd.c_str(), strOut);
    }
    pump_int32_t UpdateLib(::Pump::Core::CEnvVarSet & envVarSet, std::string & strOut)
    {
        if (envVarSet.Size() == 0)
        {
            return PUMP_ERROR;
        }
        std::string strCmd;
        this->__SerializeLib(envVarSet, strCmd);
        return m_cmdClient.ExeCmd(strCmd.c_str(), strOut);
    }
    pump_int32_t UpdateInc(::Pump::Core::CEnvVarSet & envVarSet, std::string & strOut)
    {
        if (envVarSet.Size() == 0)
        {
            return PUMP_ERROR;
        }
        std::string strCmd;
        this->__SerializeInc(envVarSet, strCmd);
        return m_cmdClient.ExeCmd(strCmd.c_str(), strOut);
    }
protected:
    virtual pump_void_t __SerializePath(::Pump::Core::CEnvVarSet & envVarSet, std::string & strCmd)
    {
        const char * szKey = "Path";
        ::Pump::Core::CEnvVarSet::IteratorType itPath = envVarSet.Find(szKey);
        if (itPath == envVarSet.End())
        {
            szKey = "PATH";
            itPath = envVarSet.Find(szKey);
            if (itPath == envVarSet.End())
            {
                return;
            }
        }
        strCmd = "set ";
        strCmd += szKey;
        strCmd += "=";
        strCmd += envVarSet.ToString(szKey);
    }
    virtual pump_void_t __SerializeLib(::Pump::Core::CEnvVarSet & envVarSet, std::string & strCmd)
    {
        const char * szKey = "Lib";
        ::Pump::Core::CEnvVarSet::IteratorType itPath = envVarSet.Find(szKey);
        if (itPath == envVarSet.End())
        {
            szKey = "LIB";
            itPath = envVarSet.Find(szKey);
            if (itPath == envVarSet.End())
            {
                return;
            }
        }
        strCmd = "set ";
        strCmd += szKey;
        strCmd += "=";
        strCmd += envVarSet.ToString(szKey);
    }
    virtual pump_void_t __SerializeInc(::Pump::Core::CEnvVarSet & envVarSet, std::string & strCmd)
    {
        const char * szKey = "INCLUDE";
        ::Pump::Core::CEnvVarSet::IteratorType itPath = envVarSet.Find(szKey);
        if (itPath == envVarSet.End())
        {
            szKey = "INCLUDE";
            itPath = envVarSet.Find(szKey);
            if (itPath == envVarSet.End())
            {
                return;
            }
        }
        strCmd = "set ";
        strCmd += szKey;
        strCmd += "=";
        strCmd += envVarSet.ToString(szKey);
    }
private:
    CCmdUpdateEnvVar();
private:
    CUserCmdClient & m_cmdClient;
};

#endif // CMD_SERVICE_H