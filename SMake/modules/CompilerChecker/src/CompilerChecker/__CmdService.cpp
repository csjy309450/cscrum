#include "__CmdService.h"
#include "__GlobalMgr.h"

pump_void_t * CThxCmdServer::ThreadCallback(pump_void_t * pData)
{
    m_cmdServer.Open();
    return NULL;
}

pump_void_t CTestCmdClient::ReadCallback(pump_uint32_t iCBType, const char * szBuff, pump_uint32_t dwSize, pump_pvoid_t pdata)
{
    switch (iCBType)
    {
    case PUMP_CMDER_CLIENT_CB_END:
        GetGlobalMgr().m_strOutput += szBuff;
        GetGlobalMgr().m_csWriteCmd.Unlock();
        PUMP_CORE_INFO("[YZ] CTestCmdClient::ReadCallback() PUMP_CMDER_CLIENT_CB_RECV:\n %s", szBuff);
        break;
    case PUMP_CMDER_CLIENT_CB_RECV:
        //PUMP_CORE_INFO << "[YZ] CTestCmdClient::ReadCallback() PUMP_CMDER_CLIENT_CB_RECV:\n" << szBuff;
        GetGlobalMgr().m_strOutput += szBuff;
        PUMP_CORE_INFO("%s<END>\n", szBuff);
        break;
    case PUMP_CMDER_CLIENT_CB_CLOSE:
        PUMP_CORE_INFO("[YZ] CTestCmdClient::ReadCallback() PUMP_CMDER_CLIENT_CB_CLOSE");
        break;
    case PUMP_CMDER_CLIENT_CB_OPEN:
        PUMP_CORE_INFO("[YZ] CTestCmdClient::ReadCallback() PUMP_CMDER_CLIENT_CB_OPEN");
        break;
    }
}

pump_int32_t CUserCmdClient::Open()
{
    return m_cmdClient.Open();
}

pump_int32_t CUserCmdClient::ExeCmd(const char* cmd, std::string & strOut)
{
    GetGlobalMgr().m_csWriteCmd.Lock();
    if (m_cmdClient.Write(cmd, strlen(cmd)) == PUMP_ERROR)
    {
        GetGlobalMgr().m_csWriteCmd.Unlock();
        return -1;
    }
    GetGlobalMgr().m_csWriteCmd.Lock();
    strOut = GetGlobalMgr().m_strOutput;
    GetGlobalMgr().m_strOutput.clear();
    GetGlobalMgr().m_csWriteCmd.Unlock();
    return 0;
}