# -*-encoding=utf-8-*-

from mapping_rule.mapping_rule_base import *

g_sz_lang = 'jna'


# TODO: 将数据写到文件中，由于字符数量大且不定长度，使用临时文件
class JnaMappingEngine(MappingEngine):
    class JnaGlobalEvn(MappingEvn):
        def __init__(self, _file_name, _lib_name):
            super(self.__class__, self).__init__(g_sz_lang)
            self.sz_file_name = _file_name
            self.sz_lib_name = _lib_name
            self.sz_jna_public_class_code = ""
            self.sz_dep_packages = ""
            self.arr_sz_com = []
            self.arr_sz_def = []

    def __init__(self, _file_name, _lib_name):
        super(self.__class__, self).__init__(g_sz_lang)
        self.jna_evn = JnaMappingEngine.JnaGlobalEvn(_file_name, _lib_name)
        self.writer = CodeWriter(_file_name + ".java")
        self.__make_auto_code()

    def run(self, _l_mapping):
        if type(_l_mapping) is not MappingList:
            raise "type(_l_mapping) is not MappingList"
        sz_code = ""
        # 1.包引入code
        # sz_code = sz_code + self.jna_evn.sz_dep_packages
        self.writer.wirte_to_file(self.jna_evn.sz_dep_packages)
        # 2.public class code
        # sz_code = sz_code + self.jna_evn.sz_jna_public_class_code[0]
        self.writer.wirte_to_file(self.jna_evn.sz_jna_public_class_code[0])
        # 3.接口，数据结构等
        # sz_code = sz_code + self.__make_content(_l_mapping)
        self.writer.wirte_to_file(self.__make_content(_l_mapping))
        # 4.结束 "}" code
        # sz_code = sz_code + self.jna_evn.sz_jna_public_class_code[1]
        self.writer.wirte_to_file(self.jna_evn.sz_jna_public_class_code[1])
        return sz_code

    def __make_auto_code(self):
        self.jna_evn.sz_dep_packages = "import java.lang.String;\n" \
                                       "import java.util.Arrays;\n" \
                                       "import java.util.List;\n" \
                                       "import com.sun.jna.Native;\n" \
                                       "import com.sun.jna.Library;\n" \
                                       "import com.sun.jna.NativeLong;\n" \
                                       "import com.sun.jna.Pointer;\n" \
                                       "import com.sun.jna.Structure;\n" \
                                       "import com.sun.jna.Union;\n" \
                                       "import com.sun.jna.Callback;\n" \
                                       "import com.sun.jna.ptr.IntByReference;\n" \
                                       "import com.sun.jna.ptr.PointerByReference;\n" \
                                       "import com.sun.jna.ptr.NativeLongByReference;\n" \
                                       "import com.sun.jna.ptr.ByteByReference;\n" \
                                       "import com.sun.jna.ptr.PointerByReference;\n" \
                                       "\n"
        if self.jna_evn.sz_file_name != '' and self.jna_evn.sz_lib_name != '':
            self.jna_evn.sz_jna_public_class_code = ["public class " + self.jna_evn.sz_file_name \
                                                     + " {\npublic interface " + self.jna_evn.sz_lib_name \
                                                     + " extends Library{\n" \
                                                     + "public static final String m_libName = \"lib\\\\" \
                                                     + self.jna_evn.sz_lib_name + "\";\n" \
                                                     + "public static " + self.jna_evn.sz_lib_name + " m_libInstance = (" \
                                                     + self.jna_evn.sz_lib_name + ")Native.loadLibrary(m_libName, " \
                                                     + self.jna_evn.sz_lib_name + ".class);\n",
                                                     "}\n}\n"]

    def __make_content(self, _l_mapping):
        if type(_l_mapping) is not MappingList:
            raise "type(_l_mapping) must MappingList"
        # 遍历映射API列表，逐个将function模型->jna代码
        sz_fun_info = ""
        for fn in _l_mapping.arr_function:
            print(fn.sz_ELM_Name)
            if self.jna_evn.find(fn, "func") is False:
                '''
                在Jna全局上下文中未找到函数对象，若未找到说明之前未转换，执行转换工作
                '''
                obj_rule = FunctionMappingRule(fn)
                fn_type, fn_other_info = obj_rule.mapping(JnaFunction(), {'var_type': "fn_arg", 'g_evn': self.jna_evn})
                sz_fun_info = sz_fun_info + fn_type
                if fn_other_info != ['', '']:
                    self.jna_evn.arr_sz_com.append(fn_other_info[0] + fn_other_info[1])
                self.jna_evn.arr_obj_fn.append(fn)
        # 遍历映射复合类型列表，输出
        sz_com_info = ""
        for sz_com in self.jna_evn.arr_sz_com:
            sz_com_info = sz_com_info + sz_com
        return sz_com_info + sz_fun_info


class JnaEnumerator(MappingCore):
    def __init__(self):
        super(JnaEnumerator, self).__init__(g_sz_lang)
        pass

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class JnaFunction(MappingCore):
    class JnaFunctionEvn(MappingEvn):
        def __init__(self):
            self.sz_fn_name = ""
            self.sz_ret_type = ""
            self.arr_args_info = []

        def __str__(self):
            sz_args_info = ""
            i_indx = 0
            for sz_arg in self.arr_args_info:
                if i_indx != 0:
                    sz_args_info = sz_args_info + ", "
                sz_args_info = sz_args_info + sz_arg
                i_indx = i_indx + 1
            sz_fn_info = self.sz_ret_type + ' ' + self.sz_fn_name + "(" + sz_args_info + ")"
            return sz_fn_info

    def __init__(self):
        super(JnaFunction, self).__init__(g_sz_lang)
        self.obj_fn_evn = JnaFunction.JnaFunctionEvn()

    def mapping_core(self, _elm, _data=None):
        """
        函数对象映射
        :param _elm:
        :param _data: Jna全局上下文对象 JnaGlobalEvn 或 JnaCompoundEvn
        :return: 返回Jna函数原型, 以及函数附加信息，函数涉及的复合类型
        """
        if type(_elm) is not clt.Function:
            raise "type(_elm) must clt.Function"
        if "cb" in _data.keys() and _data['cb'] == 1:
            self.obj_fn_evn.sz_fn_name = 'invoke'
        else:
            self.obj_fn_evn.sz_fn_name = _elm.sz_ELM_Name

        # 1.转换返回值
        sz_ret_other_info = ['', '']  # 返回值的附带信息，如果返回值类型涉及某种复合数据类型，信息则为该复合类型的jna代码
        sz_ret_type = ""  # 返回值jna类型名
        if type(_elm.obj_Fn_DT_Ret) is clt.Compound:
            if _data is None \
                    or (issubclass(_data['g_evn'].__class__, MappingEvn) and _data['g_evn'].find(_elm.stru_Var_TData,
                                                                                                 'com') is False):
                '''
                若该复合类型未被转换过, 则进行Jna转换
                '''
                obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                sz_type, sz_t_ret_other_info = obj_rule.mapping(JnaCompound(), _data)
                sz_ret_other_info = sz_t_ret_other_info
                _data.arr_obj_com.append(_elm.stru_Var_TData)  # 记录复合类型已转换
            sz_ret_type = _elm.stru_Var_TData.sz_ELM_Name
        elif type(_elm.obj_Fn_DT_Ret) is clt.DPointer:
            obj_rule = DPointerMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(JnaDPointer(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif type(_elm.obj_Fn_DT_Ret) is clt.BuildIn:
            obj_rule = BuildinMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(JnaBuildin(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif type(_elm.obj_Fn_DT_Ret) is clt.AnotherName:
            obj_rule = AnotherNameMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(JnaAnotherName(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif _elm.obj_Fn_DT_Ret is None:
            sz_ret_type = "void"
        else:
            raise "_elm type must in { Compound DPointer BuildIn }"
        sz_ret_type = sz_ret_type.strip()
        '''
        向Jna上下文添加附加信息
        '''
        self.obj_fn_evn.sz_ret_type = sz_ret_type
        # if type(_data) is JnaCompound.JnaCompoundEvn:
        #     _data.arr_inline_compound.append(sz_ret_other_info)
        # elif type(_data) is JnaMappingEngine.JnaGlobalEvn:
        #     _data.arr_sz_com.append(sz_ret_other_info)
        # else:
        #     pass

        # 2.转换参数列表
        sz_var_type = _data['var_type']
        _data['var_type'] = 'fn_arg'
        sz_arg_other_info = ["", ""]
        for arg in _elm.arr_Fn_args:
            if type(arg) is not clt.Variable:
                raise "type(arg) must clt.Variable"
            obj_rule = VariableMappingRule(arg)
            sz_arg_type, sz_t_arg_other_info = obj_rule.mapping(JnaVariable(), _data)
            sz_arg_other_info[0] = sz_arg_other_info[0] + sz_t_arg_other_info[0]
            sz_arg_other_info[1] = sz_arg_other_info[1] + sz_t_arg_other_info[1]
            sz_arg_type = sz_arg_type.strip()
            self.obj_fn_evn.arr_args_info.append(sz_arg_type)
            # self.obj_fn_evn.arr_args_info[arg.sz_ELM_Name] = sz_arg_type
            # '''
            # 向Jna上下文添加附加信息
            # '''
            # if type(_data) is JnaCompound.JnaCompoundEvn:
            #     _data.arr_inline_compound.append(sz_arg_other_info)
            # elif type(_data) is JnaMappingEngine.JnaGlobalEvn:
            #     _data.arr_sz_com.append(sz_arg_other_info)
            # else:
            #     pass
        _data['var_type'] = sz_var_type
        sz_fn_info = "public " + str(self.obj_fn_evn) + ";\n"
        return sz_fn_info, [sz_ret_other_info[0] + sz_arg_other_info[0], sz_ret_other_info[1] + sz_arg_other_info[1]]


class JnaDefine(MappingCore):
    def __init__(self):
        super(JnaDefine, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class JnaAnotherName(MappingCore):
    def __init__(self):
        super(JnaAnotherName, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        sz_other_info = ['', '']
        if type(_elm.stru_AN_DT) is clt.Compound:
            if _data is not None:
                if _data['g_evn'].find(_elm.stru_AN_DT, 'com') is False:
                    obj_rule = CompoundMappingRule(_elm.stru_AN_DT)
                    sz_type, sz_other_info = obj_rule.mapping(JnaCompound(), _data)
                    _data['g_evn'].arr_obj_com.append(_elm.stru_AN_DT)
                else:
                    sz_type = _elm.stru_AN_DT.sz_ELM_Name + ' '
            else:
                if _elm.stru_AN_DT.is_inline() is True:
                    obj_rule = CompoundMappingRule(_elm.stru_AN_DT)
                    sz_type, sz_other_info = obj_rule.mapping(JnaCompound(), _data)
                else:
                    sz_type = _elm.stru_AN_DT.sz_ELM_Name + ' '
        elif type(_elm.stru_AN_DT) is clt.DPointer:
            obj_rule = DPointerMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(JnaDPointer(), _data)
        elif type(_elm.stru_AN_DT) is clt.BuildIn:
            obj_rule = BuildinMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(JnaBuildin())
        elif type(_elm.stru_AN_DT) is clt.AnotherName:
            obj_rule = AnotherNameMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(JnaAnotherName(), _data)
        elif type(_elm.stru_AN_DT) is clt.FPointer:
            obj_rule = FPointerMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(JnaFPointer(), _data)
        elif type(_elm.stru_AN_DT) is clt.Enum:
            obj_rule = EnumMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(JnaEnum())
        else:
            raise "_elm type must in { Compound DPointer BuildIn }"
        return sz_type, sz_other_info


class JnaVariable(MappingCore):
    tuple_var_type = ("fn_arg", "com_member")

    def __init__(self):
        super(JnaVariable, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        if _data is None or type(_data) is not dict \
                or _data["var_type"] is None or _data["var_type"] not in self.tuple_var_type:
            raise "type(_data) must dict"

        sz_other_info = ['', '']
        sz_type = ""
        if type(_elm.stru_Var_TData) is clt.Compound:
            if _data["var_type"] == 'fn_arg':
                if _data["g_evn"].find(_elm.stru_Var_TData, 'com') is False:
                    _data["g_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                    obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                    sz_type, sz_t_other = obj_rule.mapping(JnaCompound(), _data)
                    sz_other_info = sz_t_other
                else:
                    sz_type = _elm.stru_Var_TData.sz_ELM_Name
            elif _data["var_type"] == 'com_member':
                if _data["com_evn"].find(_elm.stru_Var_TData, 'com') is False \
                        and _data["g_evn"].find(_elm.stru_Var_TData, 'com') is False:
                    obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                    sz_type, sz_t_other = obj_rule.mapping(JnaCompound(), _data)
                    sz_other_info = sz_t_other
                    if _elm.stru_Var_TData.is_inline() is True:
                        _data["com_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                    else:
                        _data["g_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                else:
                    sz_type = _elm.stru_Var_TData.sz_ELM_Name
        elif type(_elm.stru_Var_TData) is clt.DPointer:
            obj_rule = DPointerMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other = obj_rule.mapping(JnaDPointer(), _data)
            sz_other_info = sz_t_other
        elif type(_elm.stru_Var_TData) is clt.BuildIn:
            obj_rule = BuildinMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other, = obj_rule.mapping(JnaBuildin())
            sz_other_info = sz_t_other
        elif type(_elm.stru_Var_TData) is clt.AnotherName:
            obj_rule = AnotherNameMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other = obj_rule.mapping(JnaAnotherName(), _data)
            sz_other_info = sz_t_other
        else:
            print(type(_elm.stru_Var_TData))
            raise "_elm type must in { Compound DPointer BuildIn }"
        sz_type = sz_type.strip()

        def make_var_create():

            def make_dim_info(_type):
                if _type not in list(JnaBuildin.dict_buildin_map.keys()):
                    sz_arr_size_info = "[] = (" + _type + "[])new " \
                                       + _type + "().toArray(" + _elm.get_dim_size(0) + ")"
                else:
                    sz_arr_size_info = "[] = new " + _type + "[" + _elm.get_dim_size(0) + "]"
                return sz_arr_size_info

            if len(_elm.sz_TD_ArrSize) != 0:
                '''
                数组处理
                '''
                if len(_elm.sz_TD_ArrSize) == 1:
                    '''
                    一维数组
                    '''
                    var_create_info = make_dim_info(sz_type)
                    return var_create_info
                else:
                    '''
                    多维数组
                    '''
                    var_other_info = ""
                    t_sz_type = sz_type
                    for i in range(1, len(_elm.sz_TD_ArrSize)):
                        var_other_info = var_other_info + \
                                         "public static class " + sz_type + "_arr_" \
                                         + str(i) + " extends Structure {\n" \
                                                    "public " + t_sz_type + " byKeyInfo " + make_dim_info(t_sz_type) \
                                         + ";\n" \
                                           "@Override\n" \
                                           "protected List<String> getFieldOrder() {\n" \
                                           "return Arrays.asList(\"byKeyInfo\");\n}\n}\n"
                        t_sz_type = sz_type + "_arr_" + str(i)
                    if 'com_evn' in _data.keys() and type(_data['com_evn']) is JnaCompound.JnaCompoundEvn:
                        _data['com_evn'].arr_inline_compound.append(var_other_info)
                    elif 'g_evn' in _data.keys() and type(_data['g_evn']) is JnaMappingEngine.JnaGlobalEvn:
                        _data['g_evn'].arr_inline_compound.append(var_other_info)
                    else:
                        pass
                    var_create_info = make_dim_info(sz_type + "_arr_1")
                    return var_create_info
            else:
                '''
                非数组处理
                '''
                var_create_info = ""
                if sz_type not in list(JnaBuildin.dict_buildin_map.keys()) \
                        and type(_elm) is clt.AnotherName and type(_elm.stru_AN_TData) is not clt.FPointer:
                    var_create_info = " = new " + sz_type + "()"
                else:
                    pass
                return var_create_info

        def make_access_control():
            if _elm.sz_Var_access_control.strip() in clt.Variable.tuple_var_access_control:
                return _elm.sz_Var_access_control.strip()
            else:
                return "public"

        def make_type():
            if _elm.sz_TD_ArrSize is not None and len(_elm.sz_TD_ArrSize) > 1:
                return sz_type + "_arr_1"
            else:
                return sz_type

        sz_var_info = ""
        if _data["var_type"] == "fn_arg":
            sz_var_info = make_type() + ' ' + _elm.sz_ELM_Name
        elif _data["var_type"] == "com_member":
            sz_var_info = make_access_control() + " " + make_type() + ' ' + _elm.sz_ELM_Name + make_var_create() + ';\n'

        return sz_var_info, sz_other_info


########################################
#            以下为数据类型
########################################

class JnaBuildin(MappingCore):
    dict_buildin_map = {
        "int": ("int", "c_int", "u_int", "c_u_int"),
        "byte": ("char", "c_char", "u_char", "c_u_char"),
        "short": ("short", "c_short", "u_short", "c_u_short"),
        "long": ("longlong", "c_longlong", "u_longlong", "c_u_longlong",
                 "int64", "u_int64", "c_int64", "c_u_int64"),
        "float": ("float", "c_float"),
        "double": ("double", "c_double"),
        "String": ("p_char", 'p_c_char', 'p_u_char', 'p_c_u_char'),
        "NativeLong": ("long", "u_long", "c_long", "c_u_long"),
        "Pointer": ('p_short', 'p_int', 'p_long', 'p_longlong',
                    'p_int64', 'p_float', 'p_double', 'p_u_short',
                    'p_u_int', 'p_u_long', 'p_u_longlong', 'p_u_int64',
                    'p_c_short', 'p_c_int', 'p_c_long', 'p_c_longlong',
                    'p_c_int64', 'p_c_float', 'p_c_double', 'p_c_u_short',
                    'p_c_u_int', 'p_c_u_long', 'p_c_u_longlong', 'p_c_u_int64',
                    'p_void'),
        "void": ("void",)
    }

    def __init__(self):
        super(JnaBuildin, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        for key in self.dict_buildin_map:
            if _elm.sz_BI_Type in self.dict_buildin_map[key]:
                return key, ['', '']
        return "$$unknown$$", ['', '']


class JnaDPointer(MappingCore):
    def __init__(self):
        super(JnaDPointer, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        if type(_elm.stru_DP_Type) is clt.Compound:
            sz_t_other = ['', '']
            if _data["var_type"] == 'fn_arg':
                if _data["g_evn"].find(_elm.stru_DP_Type, 'com') is False:
                    '''
                    若该复合类型未被检索过
                    '''
                    _data["g_evn"].arr_obj_com.append(_elm.stru_DP_Type)
                    obj_rule = CompoundMappingRule(_elm.stru_DP_Type)
                    sz_type, sz_t_other = obj_rule.mapping(JnaCompound(), _data)
            elif _data["var_type"] == 'com_member':
                if _data["com_evn"].find(_elm.stru_DP_Type, 'com') is False \
                        and _data["g_evn"].find(_elm.stru_DP_Type, 'com') is False:
                    '''
                    若该复合类型未被检索过
                    '''
                    obj_rule = CompoundMappingRule(_elm.stru_DP_Type)
                    sz_type, sz_t_other = obj_rule.mapping(JnaCompound(), _data)
                    if _elm.stru_DP_Type.is_inline() is True:
                        _data["com_evn"].arr_obj_com.append(_elm.stru_DP_Type)
                    else:
                        _data["g_evn"].arr_obj_com.append(_elm.stru_DP_Type)
            return "Pointer ", sz_t_other
        elif type(_elm.stru_DP_Type) is clt.AnotherName:
            # obj_rule = AnotherNameMappingRule(_elm.stru_DP_Type)
            return "Pointer ", ['', '']
        elif type(_elm.stru_DP_Type) is clt.BuildIn:
            # obj_rule = AnotherNameMappingRule(_elm.stru_DP_Type)
            if _elm.stru_DP_Type.sz_BI_Type in JnaBuildin.dict_buildin_map['byte']:
                return 'String ', ['', '']
            return "Pointer ", ['', '']
        elif type(_elm.stru_DP_Type) is clt.DPointer:
            # TODO: 多级指针，目前代码中没有，暂不处理
            obj_rule = DPointerMappingRule(_elm.stru_DP_Type)
            sz_type, sz_t_other = obj_rule.mapping(JnaDPointer(), _data)
            if sz_type.strip() == "Pointer":
                return "PointerByReference ", ['', '']
            else:
                return "Pointer ", ['', '']
        else:
            raise "_elm type must in { Compound DPointer AnotherName}"


class JnaFPointer(MappingCore):
    def __init__(self):
        super(JnaFPointer, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        if type(_elm) is not clt.FPointer:
            raise "type(_elm) is not clt.FPointer"
        sz_fp_info = "public interface " + _elm.sz_ELM_Name + " extends Callback{\n"
        _data['cb'] = 1
        obj_rule = FunctionMappingRule(_elm.stru_FP_fn)
        fp_type, fp_other_info = obj_rule.mapping(JnaFunction(), _data)
        sz_fp_info = sz_fp_info + fp_type + "}\n"
        return _elm.sz_ELM_Name + ' ', [fp_other_info[0], sz_fp_info + fp_other_info[1]]


class JnaReference(MappingCore):
    def __init__(self):
        super(JnaReference, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class JnaCompound(MappingCore):
    class JnaCompoundEvn(MappingEvn):
        def __init__(self):
            super(JnaCompound.JnaCompoundEvn, self).__init__(g_sz_lang)
            self.arr_inline_compound = []
            self.arr_variable = []
            self.arr_function = []

    def __init__(self):
        super(JnaCompound, self).__init__(g_sz_lang)
        self.obj_com_evn = JnaCompound.JnaCompoundEvn()

    def mapping_core(self, _elm, _data=None):
        sz_com_info = "public static class "
        sz_other_info = ""
        sz_com_info = sz_com_info + _elm.sz_ELM_Name + ' extends '
        if _elm.i_Com_Type == 1:
            '''
            struct
            '''
            sz_com_info = sz_com_info + "Structure {\n"
        elif _elm.i_Com_Type == 2:
            '''
            class
            '''
            pass
        elif _elm.i_Com_Type == 3:
            '''
            union
            '''
            sz_com_info = sz_com_info + "Union {\n"
        else:
            pass
        if _elm.sz_ELM_Name == "inner_struct_3":
            pass
        for member in _elm.tree_Com_members:
            '''
            遍历成员对象
            '''
            inline_flag = 1  # biaozhi
            if type(member) is clt.Variable:
                obj_rule = VariableMappingRule(member)
                sz_var_info, t_sz_other_info = obj_rule.mapping(JnaVariable(), _data={"var_type": "com_member",
                                                                                      "com_evn": self.obj_com_evn,
                                                                                      "g_evn": _data["g_evn"]})
                self.obj_com_evn.arr_variable.append(sz_var_info)

                # FIXME: 无法判断t_sz_other_info返回的附加信息是内联还是外部
                if t_sz_other_info != ['', '']:
                    if t_sz_other_info[0] != '':
                        '''
                        成员变量类型是内联
                        '''
                        self.obj_com_evn.arr_inline_compound.append(t_sz_other_info[0])
                    else:
                        '''
                        成员变量类型是非内联
                        '''
                        sz_other_info = sz_other_info + t_sz_other_info[1]
                        if _data["var_type"] == 'fn_arg':
                            _data["g_evn"].arr_obj_com.append(_elm)
                        elif _data["var_type"] == 'com_member':
                            if _elm.is_inline() is True:
                                # self.obj_com_evn.arr_inline_compound.append(sz_var_info)
                                pass
                            else:
                                _data["g_evn"].arr_obj_com.append(_elm)
            elif type(member) is clt.Function:
                # self.obj_com_evn.arr_function.append(xxx)
                pass
            else:
                raise "_elm type must in { Variable Function }"

        # 增加getFieldOrder成员方法
        sz_com_info = sz_com_info + self.__make_contend(_elm) + "}\n"

        if _elm.is_inline() is True:
            return _elm.sz_ELM_Name, [sz_com_info, sz_other_info]
        else:
            return _elm.sz_ELM_Name, ['', sz_other_info + sz_com_info]

    def __make_contend(self, _elm):

        def make_member_var_list():
            sz_member_var = ""
            for i in range(len(_elm.tree_Com_members)):
                if i != 0:
                    sz_member_var = sz_member_var + ', '
                sz_member_var = sz_member_var + "\"" + _elm.tree_Com_members[i].sz_ELM_Name + "\""
            return sz_member_var

        sz_evn = ""
        for it in self.obj_com_evn.arr_inline_compound:
            sz_evn = sz_evn + it
        for it in self.obj_com_evn.arr_variable:
            sz_evn = sz_evn + it
        for it in self.obj_com_evn.arr_function:
            sz_evn = sz_evn + it
        sz_evn = sz_evn + "@Override\nprotected List<String> getFieldOrder() {\nreturn Arrays.asList(" \
                 + make_member_var_list() + ");\n}\n"
        return sz_evn


class JnaEnum(MappingCore):
    def __init__(self):
        super(JnaEnum, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "int ", ['', '']
