#! -*-encoding=utf-8-*-

g_dict_mode_dir = {
    "ehome_2.0": {
        "mode_dir": "D:\\3_test_program\\HCStructModel\\EHomeSDK_XmlModel\\mode\\win32\\xml\\",
        "outline_path": "D:\\3_test_program\\HCStructModel\\EHomeSDK_XmlModel\\outline\\EHomeSDK.outline"
    },
    "hcnet_5.0_old": {
        "mode_dir": "D:\\3_test_program\\HCStructModel\\HCNetSDK_XmlModel\\mode\\win32\\xml\\",
        "outline_path": "D:\\3_test_program\\HCStructModel\\HCNetSDK_XmlModel\\mode\\outline\\HCNetSDK5.0.outline"
    },
    "test": {
        "mode_dir": "F:\\YZ-data\\4_projects\\ReverseModeling\\c_src\\res\\xml\\",
        "outline_path": "F:\\YZ-data\\4_projects\\ReverseModeling\\c_src\\res\\outline\\test.outline"
    },
}

# HCNetSDK_XmlModel
g_mode_dir = g_dict_mode_dir["test"]["mode_dir"]
outline_path = g_dict_mode_dir["test"]["outline_path"]

# XmlModel4
# g_mode_dir = "..\\XmlModel4\\mode\\xml\\"
# outline_path = "..\\XmlModel4\\mode\\outline\\test.outline"

import metadata.tools as tools
tools.set_dev_evn()