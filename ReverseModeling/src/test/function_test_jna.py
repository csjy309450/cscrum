# -*-encoding=utf-8-*-

try:
    from test_config import *
except ImportError:
    from test.test_config import *
try:
    from metadata import def_parser2 as dp, index_parser as ip
except ImportError:
    import sys
    # test_src_path = "D:\\3_test_program\\HCStructModel\\src"
    sys.path.append(test_src_path)
    from metadata import def_parser2 as dp, index_parser as ip
from g_config import *
from mapping_rule.mapping_rule_base import*
import mapping_rule.jna_mapping_rule as jna


def mapping_test_compound():
    f = open("jna_com.java", 'w')
    if f is None:
        raise "f is None"
    hIndx = ip.index_execute(g_mode_dir + "index.xml")
    evn = jna.JnaMappingEngine.JnaGlobalEvn("test", "test_dll")
    print("// total count: " + str(len(hIndx.stru_xml.arr_compound)))
    for it in hIndx.stru_xml.arr_compound:
        elm = dp.find_com_by_id(it.sz_XFile_refid, hIndx)
        if evn.find(elm, 'com') is False:
            obj_rule = CompoundMappingRule(elm)
            com_type, com_out = obj_rule.mapping(jna.JnaCompound(), {"var_type": "fn_arg", "g_evn": evn})
            evn.arr_obj_com.append(elm)
            f.write(com_out[0] + com_out[1])
        pass
    pass


def mapping_test_a_compound():
    # l_com_id = ["structtag_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___f_i_x_e_d___h_e_a_d_e_r",
    #              "struct_n_e_t___d_v_r___c_l_i_e_n_t_i_n_f_o",
    #              "structtag_n_e_t___d_v_r___w_i_f_i___c_f_g___e_x",
    #              "struct_____p_l_a_y_r_e_c_t",
    #              "struct_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___v40",
    #              "structtag_n_e_t___d_v_r___v_q_d___e_v_e_n_t___r_u_l_e"]

    l_com_id = [#"structtag_n_e_t___v_c_a___o_n_e___r_u_l_e", # 本复合类型涉及若干其他符合类型，作为典型案例
        'structtag_n_e_t___d_v_r___s_e_a_r_c_h___e_v_e_n_t___p_a_r_a_m___v50',  # 本复合类型内部有若干匿名内联复合类型，作为典型案例
        # 'structtag_n_e_t___e_h_o_m_e___i_n_p_u_t___w_e_e_k_l_y___p_l_a_n',
        # 'structtag_n_e_t___v_c_a___l_i_n_e'
                ]

    hIndx = ip.index_execute(g_mode_dir + "index.xml")
    evn = jna.JnaMappingEngine.JnaGlobalEvn("test", "test_dll")
    print("\n//****************\n")
    for id in l_com_id:
        elm = dp.find_com_by_id(id, hIndx)
        if evn.find(elm, 'com') is False:
            obj_rule = CompoundMappingRule(elm)
            com_type, com_out = obj_rule.mapping(jna.JnaCompound(), {"var_type": "fn_arg", "g_evn": evn})
            evn.arr_obj_com.append(elm)
            print(com_out[0]+com_out[1]+"\n//****************\n")
    pass


def mapping_test_fn():
    l_func_id = []
    # l_func_id = ["_h_c_net_s_d_kv5_80__nc__win32_8h_1a1eb93ca68398b731fd7e95b857ce2ebd",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a4bc059df73198994fbd36cf37dc28273",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1aff91ae8817a06bfc5f2a603c97b4e641",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a89c498630103a3682d5017a61f8304f6",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1ab783b913809c130799ea502beca390c4",]
    l_func_id = ["test_8h_1ab4adfd7611d30d063e17e6e16ff371d0",]
    hIndx = ip.index_execute(g_mode_dir + "index.xml")
    # print("// [INFO] function count:"+str(len(hIndx.stru_xml.arr_function)))
    for i in range(0, len(hIndx.stru_xml.arr_function)):
        l_func_id.append(hIndx.stru_xml.arr_function[i].sz_Fn_refid)
    fn_list = []
    for id in l_func_id:
        elm = dp.find_fn_by_id(id, "test_8h", hIndx)
        fn_list.append(elm)
    print("// [INFO] finish parser API functions")
    jnaEng = jna.JnaMappingEngine("test_code", "test_code_dll")
    funList = jna.MappingList()
    funList.arr_function = fn_list
    print(jnaEng.run(funList))


def mapping_test_a_fn():
    l_func_id = []
    # l_func_id = ["_h_c_net_s_d_kv5_80__nc__win32_8h_1a1eb93ca68398b731fd7e95b857ce2ebd",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a4bc059df73198994fbd36cf37dc28273",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1aff91ae8817a06bfc5f2a603c97b4e641",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a89c498630103a3682d5017a61f8304f6",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1ab783b913809c130799ea502beca390c4",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a6f77ec4992127086bd9578c84ad99fdd",
    #                  "_h_c_net_s_d_kv5_80__nc__win32_8h_1a9194d4d12e92bd1b5cebc87a5a907e2a",]
    l_func_id = ["_e_home_s_d_k__nc_8h_1a55d6ea1528dd146155c9b0810c53418b",]
    # l_func_id = ["_h_c_net_s_d_kv5_80__nc__win32_8h_1a9194d4d12e92bd1b5cebc87a5a907e2a",]
    hIndx = ip.index_execute(g_mode_dir + "index.xml")
    fn_list = []
    for id in l_func_id:
        elm = dp.find_fn_by_id(id, "work_8h", hIndx)
        fn_list.append(elm)
    jnaEng = jna.JnaMappingEngine("test_code", "test_code_dll")
    funList = jna.MappingList()
    funList.arr_function = fn_list
    print(jnaEng.run(funList))


def mapping_test_a_cb():
    l_func_id = []
    l_com_id = ["_e_home_s_d_k__nc_8h_1af312959d3faefe4286ad63e73b7613e3", ]

    hIndx = ip.index_execute(g_mode_dir + "index.xml")
    evn = jna.JnaMappingEngine.JnaGlobalEvn("test", "test_dll")
    print("\n//****************\n")
    for id in l_com_id:
        elm = dp.find_an_by_id(id, "work_8h", hIndx)
        obj_rule = AnotherNameMappingRule(elm)
        com_type, com_out = obj_rule.mapping(jna.JnaAnotherName(), {"var_type": "fn_arg", "g_evn": evn})
        print(com_out[0] + com_out[1] + "\n//****************\n")


if __name__ == "__main__":
    # mapping_test_compound()
    mapping_test_fn()
    # mapping_test_fn()
    # mapping_test_a_fn()
    # mapping_test_a_cb()
    pass