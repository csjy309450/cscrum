# -*-encoding=utf-8-*-

from g_config import *

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
import copy as cp

from metadata import index_parser as ip, clang_type as clt, outline_parser as op, tools
import re


def parser_var_by_str(_indx_handler, _sz_arg):
    """
    解析一个变量，暂时不考虑
    :param _sz_arg:
    :return: Variable对象
    """
    if _sz_arg == "...":
        '''
        处理变长参数
        '''
        return '...'
    var_words = _sz_arg.split()
    obj_var = None
    if len(var_words) == 1:
        p_flag = var_words[0].count("*")
        if p_flag == 0:
            '''
            匿名形参，且非指针
            '''
            obj_var = clt.Variable('')
            obj_var.stru_Var_TData = parser_type_by_str(_indx_handler, var_words[0])
            obj_var.b_is_complete = True
            return obj_var
        elif p_flag > 0:
            '''
            Type*name 这种形式
            '''
            sz_t_arg = var_words[0].replace('*', ' ')
            var_words = sz_t_arg.split()
            if len(var_words) == 1:
                obj_var = clt.Variable('')
            elif len(var_words) == 2:
                obj_var = clt.Variable(var_words[1])
            else:
                raise "_sz_arg formate error"
            obj_type = parser_type_by_str(_indx_handler, var_words[0])
            obj_var.stru_Var_TData = tools.makePointer(obj_type, p_flag)
            obj_var.stru_Var_TData.obj_TD_size = tools.TDSize()
            obj_var.stru_Var_TData.obj_TD_size.count_size(obj_type)
            obj_var.b_is_complete = True
            return obj_var
    else:
        '''
        包含多种修饰符，如const等,
        FIXME 目前假设，这种情况下，变量必须有名字
        '''
        p_flag = 0
        sz_var_name = var_words[-1]
        if sz_var_name[0] == '*':
            sz_t_name = sz_var_name.strip("*")
            p_flag = p_flag + sz_var_name.count("*")
            sz_var_name = sz_t_name
        else:
            pass
        dict_type = tools.parserType(' '.join(var_words[:-1]))
        p_flag, sz_type = dict_type['pflag'] + p_flag, dict_type['type']
        obj_type = parser_type_by_str(_indx_handler, sz_type)
        obj_var = clt.Variable(sz_var_name)
        obj_var.stru_Var_TData = tools.makePointer(obj_type, p_flag)
        if obj_var.stru_Var_TData is clt.DPointer:
            obj_var.stru_Var_TData.obj_TD_size = tools.TDSize()
            obj_var.stru_Var_TData.obj_TD_size.count_size(obj_type)
        obj_var.sz_ELM_Name = sz_var_name
        obj_var.b_is_complete = True
    return obj_var


def parser_type_by_str(_indx_handler, _sz_type_name):
    pflag = 0
    sz_type = ''
    dict_type = tools.parserType(_sz_type_name)
    pflag, sz_type = dict_type['pflag'], dict_type['type']

    '''
    @brief 原生数据类型判定
    没有<ref>节点，SDKv5.0，函数的返回值<type>未发现<ref>，
    所以首先判断是否内建对象，然后根据名称查找复合数据类型、typedef及宏
    '''
    szBuildinType = tools.isBuildinType(sz_type)
    if szBuildinType is not None:
        '''
        c/c++内建类型
        '''
        dtype = clt.BuildIn(sz_type, szBuildinType)
        dtype.obj_TD_size = tools.TDSize()
        dtype.obj_TD_size.count_size(dtype)
        dtype.b_is_complete = True
        obj_work = tools.makePointer(dtype, pflag)
        obj_work.obj_TD_size = tools.TDSize()
        obj_work.obj_TD_size.count_size(obj_work)
        return obj_work
    '''
    @brief 复合数据类型判定
    注：理论上不会进到此分支
    '''
    dtype = _indx_handler.stru_xml.find_by_name(sz_type, "compound")
    if dtype is not None:
        if dtype.b_is_complete is False:
            '''
            如果，类型不完整，需要搜索数据库，补全类型
            '''
            HCom = ComHandler(_indx_handler)
            HCom.parser_by_id(dtype.sz_XFile_refid,
                              g_mode_dir + dtype.sz_XFile_refid + ".xml")
            pass
        obj_work = tools.makePointer(dtype, pflag)
        obj_work.obj_TD_size = tools.TDSize()
        obj_work.obj_TD_size.count_size(obj_work)
        return obj_work
    '''
    @brief 判断是否为typedef类型成员
    '''
    # [fixed] 现象解析器对于形如 DWORD* pAlarmData 的成员解析错误
    # 原因: 对于typedef的指针，未作特殊处理
    dtype = _indx_handler.stru_xml.find_by_name(sz_type, "typedef")
    if dtype is not None:
        if dtype.b_is_complete is False:
            HTDef = TypedefHandler(_indx_handler)
            HTDef.parser_by_id(dtype.sz_AN_refid,
                               g_mode_dir + dtype.sz_XFile_refid + ".xml")
        obj_work = tools.makePointer(dtype, pflag)
        if type(obj_work) is clt.DPointer:
            obj_work.obj_TD_size = tools.TDSize()
            obj_work.obj_TD_size.count_size(obj_work)
        return obj_work
    '''
    @brief 判断是否为define类型成员
    '''
    dtype = _indx_handler.stru_xml.find_by_name(sz_type, "define")
    if dtype is not None:
        if dtype.b_is_complete is False:
            HDef = TypedefHandler(_indx_handler)
            HDef.parser_by_id(dtype.sz_Def_refid,
                              g_mode_dir + dtype.sz_XFile_refid + ".xml")
        obj_work = tools.makePointer(dtype, pflag)
        obj_work.obj_TD_size = tools.TDSize()
        obj_work.obj_TD_size.count_size(obj_work)
        return obj_work
    '''
    @brief 判断是否为enum类型成员
    '''
    dtype = _indx_handler.stru_xml.find_by_name(sz_type, "enum")
    if dtype is not None:
        r_dtype = clt.BuildIn('int', 'int')
        obj_work = tools.makePointer(r_dtype, 0)
        obj_work.obj_TD_size = tools.TDSize()
        obj_work.obj_TD_size.count_size(obj_work)
        return obj_work


class TypedefHandler:
    def __init__(self, _indx_handler):
        self.obj_tree = None
        self.node_root = None
        self.node_compounddef = None
        self.node_sectiondef_typedef = None
        self.arr_node_memberdef_typedef = None
        if type(_indx_handler) is not ip.IndexHandler:
            raise "param _indx_handler must IndexHandler"
        self.obj_indx_handler = _indx_handler

    def parser_by_id(self, _refid, _xml):
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.node_compounddef = self.node_root.findall('compounddef')
        if len(self.node_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        arr_sec_def = self.node_compounddef[0].findall('sectiondef')
        for sec_node in arr_sec_def:
            if sec_node.attrib.get('kind') == 'typedef':
                self.node_sectiondef_typedef = sec_node
                break

        if self.node_sectiondef_typedef is None:
            print("file define have no <sectiondef> with 'typedef' kind")
            return

        self.arr_node_memberdef_typedef = self.node_sectiondef_typedef.findall("memberdef")
        for node_memberdef in self.arr_node_memberdef_typedef:
            '''
            遍历def 文件中的typedef部分，找到id匹配的typedef语法对象
            '''
            if node_memberdef.attrib.get("id") == _refid:
                return self.__parser_memberdef(node_memberdef)
        pass

    def parser_all(self, _xml):
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.node_compounddef = self.node_root.findall('compounddef')
        if len(self.node_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        arr_sec_def = self.node_compounddef[0].findall('sectiondef')
        for sec_node in arr_sec_def:
            if sec_node.attrib.get('kind') == 'typedef':
                self.node_sectiondef_typedef = sec_node
                break

        if self.node_sectiondef_typedef is None:
            print("file define have no <sectiondef> with 'typedef' kind")
            return

        self.arr_node_memberdef_typedef = self.node_sectiondef_typedef.findall("memberdef")
        for node_memberdef in self.arr_node_memberdef_typedef:
            self.__parser_memberdef(node_memberdef)
        pass

    def __parser_memberdef(self, _node):
        if type(_node) is not et.Element or _node.attrib.get("kind") != "typedef":
            raise "_node must a et.Element"
        sz_typedef_id = _node.attrib.get("id")
        obj_elm_typedef = self.obj_indx_handler.stru_xml.find(sz_typedef_id, 'typedef')
        if obj_elm_typedef is None or type(obj_elm_typedef) is not clt.AnotherName:
            raise "_node must in func of obj_indx_handler"
        if obj_elm_typedef.sz_ELM_Name != _node.find("name").text:
            raise "refid and node is't match"
        obj_elm_typedef.stru_AN_DT = self.__parser_type(_node.find("type"))
        if type(obj_elm_typedef.stru_AN_DT) is clt.FPointer:
            '''
            当typedef为函数指针时，做特殊处理
            '''
            self.__parser_FPointer(obj_elm_typedef.stru_AN_DT, _node)
            # obj_elm_typedef.stru_AN_DT.sz_ELM_Name = obj_elm_typedef.sz_ELM_Name
        obj_elm_typedef.sz_ELM_Define = _node.find("definition").text  # + _node.find("argsstring").text
        obj_elm_typedef.b_is_complete = True
        return obj_elm_typedef

    def __parser_type(self, _node):
        arr_node_ref = _node.findall("ref")
        if len(arr_node_ref) != 0:
            '''
            索引类型
            '''
            sz_text = "".join(_node.itertext())
            obj_type = None
            for node_ref in arr_node_ref:
                obj_type = self.obj_indx_handler.stru_xml.find(node_ref.attrib.get('refid'), 'compound')
                if obj_type is not None:
                    if obj_type.b_is_complete is False:
                        '''
                        说明为索引该复合类型
                        '''
                        HCom = ComHandler(self.obj_indx_handler)
                        HCom.parser_by_id(obj_type.sz_XFile_refid,
                                          g_mode_dir + obj_type.sz_XFile_refid + ".xml")
                        pass
                    break
                obj_type = self.obj_indx_handler.stru_xml.find(node_ref.attrib.get('refid'), 'typedef')
                if obj_type is not None:
                    if obj_type.b_is_complete is False:
                        '''
                        说明未索引别名对象
                        '''
                        HTDef = TypedefHandler(self.obj_indx_handler)
                        HTDef.parser_by_id(obj_type.sz_XFile_refid,
                                           g_mode_dir + obj_type.sz_XFile_refid + ".xml")
                        pass
                    break
                raise "type ref must compound or typedef"
            n_pointer_flag = sz_text.count("*")
            sz_pointer_name = obj_type.sz_ELM_Name
            obj_work = obj_type
            for i in range(n_pointer_flag):
                obj_pointer = clt.DPointer(sz_pointer_name + '*', None)
                obj_pointer.stru_DP_Type = obj_work
                obj_work = obj_pointer
                sz_pointer_name = sz_pointer_name + '*'
            obj_work.obj_TD_size = tools.TDSize()
            obj_work.obj_TD_size.count_size(obj_work)
            obj_work.b_is_complete = True
            return obj_work
        else:
            sz_type = _node.text
            if sz_type == "":
                raise "sz_type mustn't \"\""
            '''
            @brief 判断是否回调函数指针类型别名
            '''
            szPFuncType = tools.isPFunType(sz_type)
            if szPFuncType is not None:
                obj_work = clt.FPointer("")
                obj_work.obj_TD_size = tools.TDSize()
                obj_work.obj_TD_size.count_size(obj_work)
                obj_work.b_is_complete = True
                return obj_work
            '''
            @brief 判断是否是内建对象别名
            '''
            szBuildinType = tools.isBuildinType(sz_type)
            if szBuildinType is not None:
                '''
                c/c++内建类型
                '''
                obj_work = clt.BuildIn(sz_type, szBuildinType)
                obj_work.obj_TD_size = tools.TDSize()
                obj_work.obj_TD_size.count_size(obj_work)
                obj_work.b_is_complete = True
                return obj_work
            '''
            @brief 判断是否枚举类型别名
            '''
            szEnumType = tools.isEnumType(sz_type)
            if szEnumType is not None:
                obj_enum = self.obj_indx_handler.stru_xml.find_by_name(szEnumType.strip(), "enum")
                if obj_enum is not None:
                    return obj_enum
            else:
                '''
                未知类型
                '''
                return clt.TData(sz_type)

    def __parser_FPointer(self, _elm, _node):
        if type(_elm) is not clt.FPointer:
            raise "type(_elm) is not clt.FPointer"
        _elm.sz_ELM_Name = _node.find("name").text
        _elm.stru_FP_fn = clt.Function("Fn_" + _elm.sz_ELM_Name)
        '''
        1.解析返回值
        FIXME: 目前已知的回调函数中，未出现返回值节点中包含<ref>节点的，暂时不处理
        '''
        sz_ret = _node.find("type").text
        if re.fullmatch("(.*)\(CALLBACK(( )*)\*(( )*)", sz_ret) is not None:
            indx_end = sz_ret.find('(')
            sz_ret_type = sz_ret[0:indx_end]
            _elm.stru_FP_fn.obj_Fn_DT_Ret = parser_type_by_str(self.obj_indx_handler, sz_ret_type.strip())
        '''
        2.解析参数列表
        '''
        sz_args = _node.find("argsstring").text
        if re.fullmatch("\)\(.*\)", sz_args) is not None:
            index_begin = sz_args.find('(', 0)
            index_end = sz_args.find(')', -1)
            sz_args = sz_args[index_begin + 1:index_end].strip()
            arr_args = sz_args.split(',')
            _elm.stru_FP_fn.b_is_complete = True
            for sz_arg in arr_args:
                _elm.stru_FP_fn.arr_Fn_args.append(parser_var_by_str(self.obj_indx_handler, sz_arg.strip()))
                pass


class ComHandler:
    def __init__(self, _indx_handler):
        # self.sz_xml = ''
        self.obj_tree = None
        self.node_root = None
        self.arr_compounddef = None
        self.arr_sectiondef_com = None
        if type(_indx_handler) is not ip.IndexHandler:
            raise "param _indx_handler must IndexHandler"
        self.obj_indx_handler = _indx_handler
        self.obj_td_com = None
        self.obj_com_outline = None
        self.__i_n_anonymity = 0

    def parser_by_id(self, _refid, _xml):
        print("// [INFO] ComHandler.parser_by_id():" + _refid)
        # 0.打开复合类型的定义文件structxxx.xml
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        # 1.获取复合数据类型定义对象 Compound, 在Indexhandler中检索
        # 注：index.xml是解析后读入内存的结构化数据
        self.obj_td_com = self.obj_indx_handler.stru_xml.find(_refid, "compound")
        if self.obj_td_com is None:
            raise "refid is not correct"

        # 2.获取复合数据类型成员轮廓对象 ComStructure
        # 注：每次获取都需要在outline文件中查找一遍
        # self.obj_com_outline = op.get_outline_by_name(outline_path, self.obj_td_com.sz_ELM_Name)
        # if self.obj_com_outline is None:
        #     raise 'compound outline mustn\'t None'

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.arr_compounddef = self.node_root.findall('compounddef')
        if len(self.arr_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        if self.arr_compounddef[0].attrib.get('kind') not in ("struct", "class", "union") \
                or self.arr_compounddef[0].attrib.get('id') != _refid:
            raise "refid not match"

        self.arr_sectiondef_com = self.arr_compounddef[0].findall('sectiondef')
        if len(self.arr_sectiondef_com) == 0:
            print("com define have no <sectiondef>")
            return
        # 3.从xml数据库解析成员变量
        self.__parser_members()

        # 4.结合ComStructure对象矫正Compound对象
        self.__com_correction()

        # 5.计算Compound对象的长度
        self.__com_size()

        self.obj_td_com.b_is_complete = True
        return self.obj_td_com

    def __parser_members(self):
        for node_sectiondef in self.arr_sectiondef_com:
            arr_memberdef = node_sectiondef.findall("memberdef")
            for node_memberdef in arr_memberdef:
                self.__parser_memberdef(node_memberdef)
                # self.obj_td_com.arr_Com_members.append(obj_var)
                pass

    def __parser_memberdef(self, _node):
        if type(_node) is not et.Element or _node.attrib.get("kind") not in ("function", "variable"):
            raise "_node must a et.Element"
        obj_var = None
        if _node.attrib.get("kind") == "variable":
            # obj_var = clt.Variable(_node.find("name").text)
            if _node.find("name").text == "struNtpPara":
                pass
            obj_var = self.obj_td_com.find_member_by_name(_node.find("name").text)
            if obj_var is None:
                raise "obj_var mustn't None"
            obj_var.stru_Var_TData = self.__parser_type(_node.find("type"))
            obj_var.sz_TD_ArrSize = self.__parser_argsstring(_node.find("argsstring"), "variable")
            obj_var.sz_ELM_Define = _node.find("definition").text
            obj_var.b_is_complete = True
            pass
        elif _node.attrib.get("kind") == "function":
            pass
        return obj_var

    def __parser_type(self, _node):
        """
        解析一个成员变量类型
        :param _node:
        :return:
        """
        if (type(_node) is not et.Element) \
                and _node.tag != "type":
            raise "param _node must et.Element and _node.tag must \"type\""
        arr_node_ref = _node.findall('ref')
        if len(arr_node_ref) == 0:
            '''
            不含<ref>节点的<type>处理分支
            '''

            # 解析<type>中数据类型、指针等属性
            pflag = 0
            sz_type = ''
            dict_type = tools.parserType(_node.text)
            pflag, sz_type = dict_type['pflag'], dict_type['type']

            '''
            @brief 原生数据类型判定
            没有<ref>节点，SDKv5.0，函数的返回值<type>未发现<ref>，
            所以首先判断是否内建对象，然后根据名称查找复合数据类型、typedef及宏
            '''
            szBuildinType = tools.isBuildinType(sz_type)
            if szBuildinType is not None:
                '''
                c/c++内建类型
                '''
                dtype = clt.BuildIn(sz_type, szBuildinType)
                dtype.obj_TD_size = tools.TDSize()
                dtype.obj_TD_size.count_size(dtype)
                dtype.b_is_complete = True
                return tools.makePointer(dtype, pflag)
            '''
            @brief 复合数据类型判定
            注：理论上不会进到此分支,因为复合类型一般都带<ref>
            特殊：匿名的内联复合类型
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "compound")
            if sz_type.find('@') != -1:
                '''
                TODO 内联匿名
                '''
                if dtype is not None:
                    if dtype.b_is_complete is False:
                        '''
                        如果，类型不完整，需要搜索数据库，补全类型
                        '''
                        HCom = ComHandler(self.obj_indx_handler)
                        HCom.parser_by_id(dtype.sz_XFile_refid,
                                          g_mode_dir + dtype.sz_XFile_refid + ".xml")
                        dtype.b_is_inline = True
                        pass
                    return tools.makePointer(dtype, pflag)
            else:
                '''
                非内敛匿名
                '''
                if dtype is not None:
                    '''
                    理论进不到的分支，如果进到，说明可能缺少复合类型的定义
                    '''
                    if dtype.b_is_complete is False:
                        '''
                        如果，类型不完整，需要搜索数据库，补全类型
                        '''
                        HCom = ComHandler(self.obj_indx_handler)
                        HCom.parser_by_id(dtype.sz_XFile_refid,
                                          g_mode_dir + dtype.sz_XFile_refid + ".xml")
                        pass
                    return tools.makePointer(dtype, pflag)
            '''
            @brief 判断是否为typedef类型成员
            '''
            # [fixed] 现象解析器对于形如 DWORD* pAlarmData 的成员解析错误
            # 原因: 对于typedef的指针，未作特殊处理
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "typedef")
            if dtype is not None:
                if dtype.b_is_complete is False:
                    HTDef = TypedefHandler(self.obj_indx_handler)
                    HTDef.parser_by_id(dtype.sz_AN_refid,
                                       g_mode_dir + dtype.sz_XFile_refid + ".xml")
                return tools.makePointer(dtype, pflag)
            '''
            @brief 判断是否为define类型成员
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "define")
            if dtype is not None:
                if dtype.b_is_complete is False:
                    HDef = TypedefHandler(self.obj_indx_handler)
                    HDef.parser_by_id(dtype.sz_Def_refid,
                                      g_mode_dir + dtype.sz_XFile_refid + ".xml")
                return tools.makePointer(dtype, pflag)
        else:
            '''
            有<ref>节点，SDKv5.0中，铁定是复合类型
            '''
            if arr_node_ref[0].attrib.get("kindref") == "compound":
                dtype = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "compound")
                if dtype is not None:
                    if dtype.b_is_complete is False:
                        '''
                        类型不完整，递归查询
                        '''
                        HCom = ComHandler(self.obj_indx_handler)
                        HCom.parser_by_id(dtype.sz_XFile_refid,
                                          g_mode_dir + dtype.sz_XFile_refid + ".xml")
                    return dtype
                dtype = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "typedef")
                if dtype is not None:
                    if dtype.b_is_complete is False:
                        '''
                        类型不完整，递归查询
                        '''
                        HTD = TypedefHandler(self.obj_indx_handler)
                        HTD.parser_by_id(dtype.sz_AN_refid,
                                         g_mode_dir + dtype.sz_XFile_refid + ".xml")
                    return dtype
            elif arr_node_ref[0].attrib.get("kindref") == "member":
                '''
                v5.0 SDK理论上进不到这个分支
                '''
                pflag = 0
                sz_type_other = _node.text
                if sz_type_other is not None:
                    pflag = sz_type_other.count('*')
                obj_type = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "typedef")
                if obj_type is not None:
                    HTDef = TypedefHandler(self.obj_indx_handler)
                    HTDef.parser_by_id(obj_type.sz_AN_refid,
                                       g_mode_dir + obj_type.sz_XFile_refid + ".xml")
                    return tools.makePointer(obj_type, pflag)
                return None
        pass

    def __parser_argsstring(self, _node, _kind):
        if type(_node) is not et.Element or _kind not in ("variable", "function"):
            raise "_node must a et.Element"
        if _kind == "variable":
            sz_argsstring = _node.text
            if sz_argsstring is None:
                return []
            if re.fullmatch("\[.*\]", sz_argsstring) is None:
                raise "argsstring must mutch partern \[.*\]"
            arr_argsstr = re.findall("\[[a-zA-Z0-9_]*\]", sz_argsstring)
            arr_args_value = []
            for argsstr in arr_argsstr:
                if argsstr[1:-1].isdigit():
                    arr_args_value.append(argsstr[1:-1])
                    pass
                else:
                    obj_arss = self.obj_indx_handler.stru_xml.find_by_name(argsstr[1:-1], "define")
                    if obj_arss is not None:
                        '''
                        数组参数为宏类型
                        '''
                        if obj_arss.b_is_complete is not True:
                            '''
                            非完全索引类型，需要检索
                            '''
                            HDef = DefineHandler(self.obj_indx_handler)
                            HDef.paser_by_id(obj_arss.sz_Def_refid,
                                             g_mode_dir + obj_arss.sz_XFile_refid + ".xml")
                        if type(obj_arss.obj_real_value) is int:
                            arr_args_value.append(obj_arss)
                        else:
                            arr_args_value.append(argsstr[1:-1])
                        continue

                    obj_arss = self.obj_indx_handler.stru_xml.find_by_name(argsstr[1:-1], "var")
                    if obj_arss is not None:
                        '''
                        数组参数为常量
                        '''
                        arr_args_value.append(obj_arss)
                        continue
                    raise "variable argsstring must define or const var"
            return arr_args_value
        elif _kind == "function":
            pass

    def __com_correction(self):
        """
        虽然无需在使用outline矫正复合类型结构，但是源码很多地方都使用复合类型的tree_Com_members成员，所以
        :return:
        """
        self.obj_td_com.tree_Com_members = self.obj_td_com.arr_Com_members
        pass

    def __com_correction_deprecated(self):
        """
        [deprecated]
        结合ComStructure对象矫正Compound对象。
        因为doxygen产生的xml数据库，不能正确识别复合类型的匿名内联数据类型，所以需要利用
        成员结构对象 ComStructure 对 Compound 对象的成员变量关系进行矫正
        20191024:修改doxygen源码，修复内联匿名复合对象缺陷，无需再使用outline矫正复合类型结构，弃用此接口
        :return:
        """
        if self.obj_td_com is None or self.obj_com_outline is None \
                or type(self.obj_td_com) is not clt.Compound \
                or type(self.obj_com_outline) is not op.ComStructure:
            raise "self.obj_td_com and self.obj_com_outline mustn\'t None"
        if self.obj_com_outline.is_contain_inline_member() is False:
            '''
            无内联成员对象
            '''
            self.obj_td_com.tree_Com_members = self.obj_td_com.arr_Com_members
            pass
        else:
            '''
            有内联成员对象
            '''
            for member in self.obj_com_outline.arr_member:
                '''
                遍历outline对象，重新构造复合类型成员结构
                '''
                if member.is_inline() is False:
                    # 成员变量非内联类型
                    t_var = self.obj_td_com.find_member_by_name(member.sz_name.strip())
                    if t_var is None:
                        raise member.sz_name + " can't find"
                    self.obj_td_com.tree_Com_members.append(t_var)
                else:
                    # 成员变量为内联类型
                    t_var = self.obj_td_com.find_member_by_name(member.sz_name.strip())
                    if t_var.stru_Var_TData is None:
                        raise "var type mustn\'t None"
                    t_copy_com = cp.deepcopy(t_var)
                    t_copy_com.stru_Var_TData.b_is_inline = True
                    self.__realloc_member(member, t_copy_com.stru_Var_TData)
                    t_copy_com.stru_Var_TData.obj_TD_size = tools.TDSize()
                    t_copy_com.stru_Var_TData.obj_TD_size.count_size(t_copy_com.stru_Var_TData)
                    t_copy_com.stru_Var_TData.b_is_complete = True
                    self.obj_td_com.tree_Com_members.append(t_copy_com)
                    pass
                # 从非结构化成员列表中删除
                # FIXME<严重20190429>: 多个内联匿名对象若存在相同名称的成员时，成员间会冲突.doxygen缺陷
                # self.obj_td_com.remove_member_by_value(t_var)
                pass
            pass
        pass

    def __com_size(self):
        self.obj_td_com.obj_TD_size = tools.TDSize()
        self.obj_td_com.obj_TD_size.count_size(self.obj_td_com)
        pass

    def __realloc_member(self, _ol_member, _com_type):
        if _ol_member.is_inline() is False:
            pass
        else:
            for member in _ol_member.obj_type:
                if member.is_inline() is False:
                    t_var = self.obj_td_com.find_member_by_name(member.sz_name.strip())
                    if t_var.stru_Var_TData is None:
                        raise "var type mustn\'t None"
                    _com_type.tree_Com_members.append(t_var)
                else:
                    # t_var = self.obj_td_com.find_member_by_name(member.sz_name)
                    # if t_var.stru_Var_TData is None:
                    #     raise "var type mustn\'t None"
                    # t_com = cp.deepcopy(t_var.stru_Var_TData)
                    # self.__realloc_member(member, t_com)
                    # _com_type.tree_Com_members.append(t_com)

                    t_var = self.obj_td_com.find_member_by_name(member.sz_name)
                    if t_var.stru_Var_TData is None:
                        raise "var type mustn\'t None"
                    t_copy_com = cp.deepcopy(t_var)
                    t_copy_com.stru_Var_TData.b_is_inline = True
                    self.__realloc_member(member, t_copy_com.stru_Var_TData)
                    t_copy_com.stru_Var_TData.obj_TD_size = tools.TDSize()
                    t_copy_com.stru_Var_TData.obj_TD_size.count_size(t_copy_com.stru_Var_TData)
                    t_copy_com.stru_Var_TData.b_is_complete = True
                    _com_type.tree_Com_members.append(t_copy_com)
                # self.obj_td_com.remove_member_by_value(t_var)
                pass


class DefineHandler:
    def __init__(self, _indx_handler):
        self.obj_tree = None
        self.node_root = None
        self.node_compounddef = None
        self.node_sectiondef_define = None
        self.arr_node_memberdef_define = None
        if type(_indx_handler) is not ip.IndexHandler:
            raise "param _indx_handler must IndexHandler"
        self.obj_indx_handler = _indx_handler

    def paser_by_id(self, _refid, _xml):
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.node_compounddef = self.node_root.findall('compounddef')
        if len(self.node_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        arr_sec_def = self.node_compounddef[0].findall('sectiondef')
        for sec_node in arr_sec_def:
            if sec_node.attrib.get('kind') == 'define':
                self.node_sectiondef_define = sec_node
                break

        if self.node_sectiondef_define is None:
            print("file define have no <sectiondef> with 'define' kind")
            return

        self.arr_node_memberdef_define = self.node_sectiondef_define.findall("memberdef")
        for node_memberdef in self.arr_node_memberdef_define:
            '''
            遍历def 文件中的define部分，找到id匹配的typedef语法对象
            '''
            if node_memberdef.attrib.get("id") == _refid:
                return self.__parser_memberdef(node_memberdef)
        pass

    def __parser_memberdef(self, _node):
        if type(_node) is not et.Element or _node.attrib.get("kind") != "define":
            raise "_node must a et.Element"
        sz_define_id = _node.attrib.get("id")
        obj_elm_define = self.obj_indx_handler.stru_xml.find(sz_define_id, 'define')
        if obj_elm_define.b_is_complete is True:
            return obj_elm_define
        if obj_elm_define is None or type(obj_elm_define) is not clt.Define:
            raise "_node must in func of obj_indx_handler"
        if obj_elm_define.sz_ELM_Name != _node.find("name").text:
            raise "refid and node is't match"
        self.__paser_initializer(obj_elm_define, _node.find("initializer").text)
        obj_elm_define.b_is_complete = True
        return obj_elm_define

    def __paser_initializer(self, _elm, _value):
        if type(_value) is not str or type(_elm) is not clt.Define:
            raise "type(_value) is not str or type(_elm) is not clt.Define"
        if _value.isdigit() is True:
            _elm.i_Def_Type = 2
            _elm.obj_real_value = int(_value)
            return
        if re.match('^[-+]?[0-9]*\.[0-9]+$', _value) is not None:
            _elm.i_Def_Type = 2
            _elm.obj_real_value = float(_value)
            return
        if re.fullmatch('[a-zA-Z0-9_]+', _value.strip()) is not None:
            obj_def = self.obj_indx_handler.stru_xml.find_by_name(_value.strip(), "define")
            if obj_def is not None:
                hdef = DefineHandler(self.obj_indx_handler)
                hdef.paser_by_id(g_mode_dir + obj_def.sz_Def_refid, g_mode_dir + obj_def.sz_XFile_refid)
            _elm.i_Def_Type = 3
            _elm.obj_real_value = obj_def.obj_real_value
            return
        if _elm.sz_ELM_Name == "MAX_ALARMOUT_V40":
            pass
        arr_martch = re.match('\(? *([a-zA-Z0-9_]+) *([\+\-\*]) *([a-zA-Z0-9_]+) *\)?', _value.strip())
        if arr_martch is not None:
            obj_def1 = self.obj_indx_handler.stru_xml.find_by_name(arr_martch.group(1).strip(), "define")
            if obj_def1 is not None:
                hdef = DefineHandler(self.obj_indx_handler)
                hdef.paser_by_id(obj_def1.sz_Def_refid, g_mode_dir + obj_def1.sz_XFile_refid+".xml")
            _elm.i_Def_Type = 3
            obj_def2 = self.obj_indx_handler.stru_xml.find_by_name(arr_martch.group(3).strip(), "define")
            if obj_def2 is not None:
                hdef = DefineHandler(self.obj_indx_handler)
                hdef.paser_by_id(obj_def2.sz_Def_refid, g_mode_dir + obj_def2.sz_XFile_refid+".xml")
            _elm.i_Def_Type = 3
            if arr_martch.group(2).strip() == "+":
                _elm.obj_real_value = int(obj_def1.obj_real_value) + int(obj_def2.obj_real_value)
            pass

class FuncHandler:
    def __init__(self, _indx_handler):
        # self.sz_xml = ''
        self.obj_tree = None
        self.node_root = None
        self.node_compounddef = None
        self.node_sectiondef_func = None
        self.arr_node_memberdef_func = None
        if type(_indx_handler) is not ip.IndexHandler:
            raise "param _indx_handler must IndexHandler"
        self.obj_indx_handler = _indx_handler

    def parser_by_id(self, _refid, _xml):
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.node_compounddef = self.node_root.findall('compounddef')
        if len(self.node_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        arr_sec_def = self.node_compounddef[0].findall('sectiondef')
        for sec_node in arr_sec_def:
            if sec_node.attrib.get('kind') == 'func':
                self.node_sectiondef_func = sec_node
                break

        if self.node_sectiondef_func == None:
            print("file define have no <sectiondef> with 'func' kind")
            return

        obj_fn = None
        self.arr_node_memberdef_func = self.node_sectiondef_func.findall("memberdef")
        for node_memberdef in self.arr_node_memberdef_func:
            if node_memberdef.attrib.get("id") == _refid:
                obj_fn = self.__parser_memberdef(node_memberdef)
                break
        if obj_fn is None:
            raise "no that refid"
        '''
        以下代码解析函数参数列表和返回值
        '''
        # 1.解析返回值类型
        if obj_fn.obj_Fn_DT_Ret is not None:
            '''
            v5.0 SDK 返回值都是BOOL、LONG、void*等基本数据类型
            FIXME: 目前来看，没有其他类型的返回值，均为typedef
            '''
            if type(obj_fn.obj_Fn_DT_Ret) is clt.BuildIn:
                pass
            elif type(obj_fn.obj_Fn_DT_Ret) is clt.AnotherName:
                HTDef = TypedefHandler(self.obj_indx_handler)
                HTDef.parser_by_id(obj_fn.obj_Fn_DT_Ret.sz_AN_refid,
                                   g_mode_dir + obj_fn.obj_Fn_DT_Ret.sz_XFile_refid + ".xml")
            elif type(obj_fn.obj_Fn_DT_Ret) is clt.DPointer:
                pass
            elif type(obj_fn.obj_Fn_DT_Ret) is clt.Compound:
                pass
        # 2.解析参数列表
        if len(obj_fn.arr_Fn_args) != 0:
            for arg in obj_fn.arr_Fn_args:
                if type(arg) is clt.Variable:
                    '''
                    成员变量
                    '''
                    if type(arg.stru_Var_TData) is clt.BuildIn:
                        pass
                    elif type(arg.stru_Var_TData) is clt.AnotherName:
                        HTDef = TypedefHandler(self.obj_indx_handler)
                        HTDef.parser_by_id(arg.stru_Var_TData.sz_AN_refid,
                                           g_mode_dir + arg.stru_Var_TData.sz_XFile_refid + ".xml")
                    elif type(arg.stru_Var_TData) is clt.DPointer:
                        pass
                    elif type(arg.stru_Var_TData) is clt.Compound:
                        HTDef = ComHandler(self.obj_indx_handler)
                        HTDef.parser_by_id(arg.stru_Var_TData.sz_XFile_refid,
                                           g_mode_dir + arg.stru_Var_TData.sz_XFile_refid + ".xml")
                    elif type(arg.stru_Var_TData) is clt.Enum:
                        pass
                    arg.b_is_complete = True
                    pass
                else:
                    '''
                    成员函数
                    '''
                    pass

        obj_fn.b_is_complete = True
        return obj_fn

    def parser_all(self, _xml):
        # self.sz_xml = _xml
        self.obj_tree = et.parse(_xml)
        self.node_root = self.obj_tree.getroot()

        if self.node_root.tag != 'doxygen':
            raise 'file define root node must <doxygen>'

        self.node_compounddef = self.node_root.findall('compounddef')
        if len(self.node_compounddef) != 1:
            raise 'file define must have only <compounddef>'

        arr_sec_def = self.node_compounddef[0].findall('sectiondef')
        for sec_node in arr_sec_def:
            if sec_node.attrib.get('kind') == 'func':
                self.node_sectiondef_func = sec_node
                break

        if self.node_sectiondef_func == None:
            print("file define have no <sectiondef> with 'func' kind")
            return

        self.arr_node_memberdef_func = self.node_sectiondef_func.findall("memberdef")
        for node_memberdef in self.arr_node_memberdef_func:
            self.__parser_memberdef(node_memberdef)
        pass

    def __parser_memberdef(self, _node):
        if type(_node) is not et.Element or _node.attrib.get("kind") != "function":
            raise "_node must a et.Element"
        sz_fn_id = _node.attrib.get("id")
        obj_elm_fn = self.obj_indx_handler.stru_xml.find(sz_fn_id, 'func')
        if obj_elm_fn.b_is_complete is True:
            return obj_elm_fn
        if obj_elm_fn is None or type(obj_elm_fn) is not clt.Function:
            raise "_node must in func of obj_indx_handler"

        obj_elm_fn.sz_ELM_Name = _node.find("name").text
        obj_elm_fn.obj_Fn_DT_Ret = self.__parser_type(_node.find("type"), "ret")
        obj_elm_fn.sz_ELM_Define = _node.find("definition").text + _node.find("argsstring").text
        arr_param_node = _node.findall("param")
        obj_elm_fn.arr_Fn_args = self.__parser_params(arr_param_node)
        return obj_elm_fn

    def __parser_type(self, _node, _kind):
        if _node is None:
            return clt.TData()
        if _kind not in ("ret", "param"):
            raise "_kind must in { ret, param }"
        if _kind == "ret":
            return self.parser_ret_type(_node)
        elif _kind == "param":
            return self.parser_param_type(_node)
        pass

    def __parser_params(self, _arr_node):
        if _arr_node is None or _arr_node == []:
            return []
        arr_obj_dt_param = []
        for param_node in _arr_node:
            arr_obj_dt_param.append(self.__parser_param(param_node))
        return arr_obj_dt_param

    def __parser_param(self, _node):
        if _node is None:
            return None
        node_p_type = _node.find("type")
        node_p_declname = _node.find("declname").text
        obj_dt_param = clt.Variable('')
        obj_dt_param.stru_Var_TData = self.__parser_type(node_p_type, "param")
        obj_dt_param.sz_ELM_Name = node_p_declname
        return obj_dt_param

    def parser_ret_type(self, _node):
        """
        解析函数的返回值
        :param _node:
        :return:
        """
        if (type(_node) is not et.Element) \
                and _node.tag != "type":
            raise "param _node must et.Element and _node.tag must \"type\""
        arr_node_ref = _node.findall('ref')
        if len(arr_node_ref) == 0:
            '''
            没有<ref>节点，SDKv5.0，函数的返回值<type>未发现<ref>，
            所以首先判断是否内建对象，然后根据名称查找复合数据类型、typedef及宏
            FIXME: 没有考虑 DWORD * 这种特殊类型的处理
            '''
            szBuildinType = tools.isBuildinType(_node.text)
            if szBuildinType is not None:
                '''
                c/c++内建类型
                '''
                return clt.BuildIn(_node.text, szBuildinType)
            dtype = self.obj_indx_handler.stru_xml.find_by_name(_node.text, "compound")
            if dtype is not None:
                return dtype
            dtype = self.obj_indx_handler.stru_xml.find_by_name(_node.text, "typedef")
            if dtype is not None:
                return dtype
            dtype = self.obj_indx_handler.stru_xml.find_by_name(_node.text, "define")
            if dtype is not None:
                return dtype
            pass
        else:
            '''
            有<ref>节点，SDKv5.0，理论上不会进到这个分支
            '''
            return None
        pass

    def parser_param_type(self, _node):
        """
        解析一个函数参数类型
        :param _node:
        :return:
        """
        if (type(_node) is not et.Element) \
                and _node.tag != "type":
            raise "param _node must et.Element and _node.tag must \"type\""
        arr_node_ref = _node.findall('ref')
        if len(arr_node_ref) == 0:
            '''
            没有<ref>节点，SDKv5.0，函数的返回值<type>未发现<ref>，
            所以首先判断是否内建对象，然后根据名称查找复合数据类型、typedef及宏
            '''

            pflag = 0
            sz_type = ''
            dict_type = tools.parserType(_node.text)
            pflag, sz_type = dict_type['pflag'], dict_type['type']
            '''
            @brief c/c++内建类型处理
            '''
            szBuildinType = tools.isBuildinType(sz_type)
            if szBuildinType is not None:
                dtype = clt.BuildIn(sz_type, szBuildinType)
                dtype.obj_TD_size = tools.TDSize()
                dtype.obj_TD_size.count_size(dtype)
                dtype.b_is_complete = True
                return tools.makePointer(dtype, pflag)
            '''
            @brief 复合类型处理
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "compound")
            if dtype is not None:
                if dtype.b_is_complete is False:
                    '''
                    若果，类型不完整，需要搜索数据库，补全类型
                    '''
                    pass
                return tools.makePointer(dtype, pflag)
            '''
            @brief typedef类型处理
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "typedef")
            if dtype is not None:
                if dtype.b_is_complete is False:
                    pass
                return tools.makePointer(dtype, pflag)
            '''
            @brief define类型处理
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "define")
            if dtype is not None:
                if dtype.b_is_complete is False:
                    pass
                return tools.makePointer(dtype, pflag)
            pass
            '''
            @brief define类型处理
            '''
            dtype = self.obj_indx_handler.stru_xml.find_by_name(sz_type, "enum")
            if dtype is not None:
                r_dtype = clt.BuildIn('int', 'int')
                return tools.makePointer(r_dtype, pflag)
            pass
        else:
            if arr_node_ref[0].attrib.get("kindref") == "compound":
                dtype = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "compound")
                if dtype is not None:
                    return dtype
                dtype = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "typedef")
                if dtype is not None:
                    return dtype
            elif arr_node_ref[0].attrib.get("kindref") == "member":
                '''
                理论上这个分支应该不走
                '''
                pflag = 0
                sz_type_other = _node.text
                if sz_type_other is not None:
                    pflag = sz_type_other.count('*')
                obj_type = self.obj_indx_handler.stru_xml.find_by_name(arr_node_ref[0].text, "typedef")
                if obj_type is not None:
                    HTDef = TypedefHandler(self.obj_indx_handler)
                    HTDef.parser_by_id(obj_type.sz_AN_refid,
                                       g_mode_dir + obj_type.sz_XFile_refid + ".xml")
                    return tools.makePointer(obj_type, pflag)
                return None
        pass


def find_com_by_id(_refid, _hIndx=None):
    if _hIndx is not None and type(_hIndx) is ip.IndexHandler:
        if _hIndx.isOK():
            TDefCom = ComHandler(_hIndx)
            com = TDefCom.parser_by_id(_refid, g_mode_dir + _refid + ".xml")
            return com
        else:
            return None
    else:
        hIndx = ip.index_execute(g_mode_dir + "index.xml")
        TDefCom = ComHandler(hIndx)
        com = TDefCom.parser_by_id(_refid, g_mode_dir + _refid + ".xml")
        return com
    pass


def find_fn_by_id(_refid, _def_file, _hIndx=None):
    if _hIndx is not None and type(_hIndx) is ip.IndexHandler:
        if _hIndx.isOK():
            TDefFn = FuncHandler(_hIndx)
            fn = TDefFn.parser_by_id(_refid, g_mode_dir + _def_file + ".xml")
            return fn
        else:
            return None
    else:
        hIndx = ip.index_execute(g_mode_dir + "index.xml")
        TDefFn = FuncHandler(hIndx)
        fn = TDefFn.parser_by_id(_refid, g_mode_dir + _refid + ".xml")
        return fn
    pass


def find_an_by_id(_refid, _def_file, _hIndx=None):
    if _hIndx is not None and type(_hIndx) is ip.IndexHandler:
        if _hIndx.isOK():
            TH = TypedefHandler(_hIndx)
            an = TH.parser_by_id(_refid, g_mode_dir + _def_file + ".xml")
            return an
        else:
            return None
    else:
        hIndx = ip.index_execute(g_mode_dir + "index.xml")
        TH = TypedefHandler(hIndx)
        an = TH.parser_by_id(_refid, g_mode_dir + _refid + ".xml")
        return an
    pass


if __name__ == "__main__":
    pass
