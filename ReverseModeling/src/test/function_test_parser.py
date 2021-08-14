#! -*-encoding=utf-8-*-

try:
    from test_config import *
except ImportError:
    from test.test_config import *
try:
    from metadata.def_parser2 import *
except ImportError:
    import sys

    # test_src_path = "D:\\3_test_program\\HCStructModel\\src"
    sys.path.append(test_src_path)
    from metadata.def_parser2 import *
from g_config import *


def test_find_fn_by_id():
    HIndx = ip.index_execute(g_mode_dir + "index.xml")
    HFn = FuncHandler(HIndx)
    fn = HFn.parser_by_id("work_8h_1a76be0cd270de1f86009bbd016d8cb4da",
                          g_mode_dir + "work_8h.xml")
    if fn is not None:
        print("test_find_fn_by_id succ")
    else:
        print("test_find_fn_by_id fail")
    pass


def test_find_com_by_id():
    HIndx = ip.index_execute(g_mode_dir + "index.xml")
    TDefCom = ComHandler(HIndx)
    # com = TDefCom.parser_by_id("structtag_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___f_i_x_e_d___h_e_a_d_e_r",
    #                   g_mode_dir + "structtag_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___f_i_x_e_d___h_e_a_d_e_r.xml")
    # com = TDefCom.parser_by_id("struct_n_e_t___d_v_r___c_l_i_e_n_t_i_n_f_o",
    #                            g_mode_dir + "struct_n_e_t___d_v_r___c_l_i_e_n_t_i_n_f_o.xml")
    # com = TDefCom.parser_by_id("structtag_n_e_t___d_v_r___w_i_f_i___c_f_g___e_x",
    #                            g_mode_dir + "structtag_n_e_t___d_v_r___w_i_f_i___c_f_g___e_x.xml")
    # com = TDefCom.parser_by_id("struct_____p_l_a_y_r_e_c_t",
    #                   g_mode_dir + "struct_____p_l_a_y_r_e_c_t.xml")
    # com = TDefCom.parser_by_id("struct_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___v40",
    #                            g_mode_dir + "struct_n_e_t___d_v_r___a_l_a_r_m_i_n_f_o___v40.xml")
    # com = TDefCom.parser_by_id("structtag_n_e_t___d_v_r___p_i_c",
    #                            g_mode_dir + "structtag_n_e_t___d_v_r___p_i_c.xml")
    com = TDefCom.parser_by_id("structtag_n_e_t___d_v_r___v_q_d___e_v_e_n_t___r_u_l_e",
                               g_mode_dir \
                               + "structtag_n_e_t___d_v_r___v_q_d___e_v_e_n_t___r_u_l_e.xml")
    if com is not None:
        print("test_find_com_by_id succ")
    else:
        print("test_find_com_by_id fail")
    pass


def test_find_all_typedef():
    HIndx = ip.index_execute(g_mode_dir + "index.xml")
    TDefFn = TypedefHandler(HIndx)
    TDefFn.parser_all(g_mode_dir + "work_8h.xml")
    a = TDefFn.obj_indx_handler.stru_xml.find('_h_c_net_s_d_kv5_80__nc__win32_8h_1a56019ca88dd76ad0d954460ca2d70847',
                                              'typedef')
    pass


def test_find_a_typedef():
    HIndx = ip.index_execute(g_mode_dir + "index.xml")
    TDefFn = TypedefHandler(HIndx)
    TDefFn.parser_by_id('_h_c_net_s_d_kv5_80__nc__win32_8h_1a56019ca88dd76ad0d954460ca2d70847',
                        g_mode_dir + "work_8h.xml")
    a = TDefFn.obj_indx_handler.stru_xml.find('_h_c_net_s_d_kv5_80__nc__win32_8h_1a56019ca88dd76ad0d954460ca2d70847',
                                              'typedef')
    pass


def test_find_all_define():
    HIndx = ip.index_execute(g_mode_dir + "index.xml")
    DefH = DefineHandler(HIndx)
    DefH.paser_by_id("_h_c_net_s_d_kv5_80__nc__win32_8h_1a3c88a94d6eeb9664c579245b2a7615aa",
                     g_mode_dir + "work_8h.xml")
    a = DefH.obj_indx_handler.stru_xml.find('_h_c_net_s_d_kv5_80__nc__win32_8h_1a3c88a94d6eeb9664c579245b2a7615aa',
                                            'define')
    pass


if __name__ == "__main__":
    test_find_fn_by_id()
    # test_find_com_by_id()
    # test_find_all_define()
    # test_find_all_typedef()
    # test_find_a_typedef()
    pass
