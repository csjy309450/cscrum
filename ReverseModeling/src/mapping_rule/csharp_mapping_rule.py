# -*-encoding=utf-8-*-

from mapping_rule.mapping_rule_base import *

g_sz_lang = 'csharp'


# TODO: 将数据写到文件中，由于字符数量大且不定长度，使用临时文件
class CSharpMappingEngine(MappingEngine):
    class CSharpGlobalEvn(MappingEvn):
        def __init__(self, _file_name, _lib_name):
            super(self.__class__, self).__init__(g_sz_lang)
            self.sz_file_name = _file_name
            self.sz_lib_name = _lib_name
            self.sz_csharp_public_class_code = []  # 公共代码，命名空间，公共类
            self.arr_sz_func_modifier = []  # 导出接口的修饰符
            self.sz_class_modifier = ""  # 结构体修饰符
            self.sz_dep_packages = ""  # 依赖包
            self.arr_sz_com = []
            self.arr_sz_def = []

    def __init__(self, _file_name, _lib_name):
        super(self.__class__, self).__init__(g_sz_lang)
        self.csharp_evn = CSharpMappingEngine.CSharpGlobalEvn(_file_name, _lib_name)
        self.writer = CodeWriter(_file_name + ".cs")
        self.__make_auto_code()

    def run(self, _l_mapping):
        if type(_l_mapping) is not MappingList:
            raise "type(_l_mapping) is not MappingList"
        sz_code = ""
        # 1.包引入code
        # sz_code = sz_code + self.csharp_evn.sz_dep_packages
        self.writer.wirte_to_file(self.csharp_evn.sz_dep_packages)
        # 2.public class code
        # sz_code = sz_code + self.csharp_evn.sz_csharp_public_class_code[0]
        self.writer.wirte_to_file(self.csharp_evn.sz_csharp_public_class_code[0])
        # 3.接口，数据结构等
        # sz_code = sz_code + self.__make_content(_l_mapping)
        self.writer.wirte_to_file(self.__make_content(_l_mapping))
        # 4.结束 "}" code
        # sz_code = sz_code + self.csharp_evn.sz_csharp_public_class_code[1]
        self.writer.wirte_to_file(self.csharp_evn.sz_csharp_public_class_code[1])
        return sz_code

    def __make_auto_code(self):
        self.csharp_evn.sz_dep_packages = "using System;\n" \
                                          "using System.Collections.Generic;\n" \
                                          "using System.Linq;\n" \
                                          "using System.Text;\n" \
                                          "using System.Threading.Tasks;\n" \
                                          "using System.Runtime.InteropServices;\n\n"
        self.sz_dep_packages = "[StructLayoutAttribute(LayoutKind.Sequential)]"
        if self.csharp_evn.sz_file_name != '' and self.csharp_evn.sz_lib_name != '':
            self.csharp_evn.sz_csharp_public_class_code = [
                "namespace " + self.csharp_evn.sz_file_name.upper() + "\n{\nclass " +
                self.csharp_evn.sz_file_name.lower() + "\n{\n/**\n* @class MemCopyer\n* @brief 用于结构体相关内存拷贝\n*/\npublic static class MemCopyer\n{\n// 相当于序列化与反序列化，但是不用借助外部文件\n//1、struct转换为Byte[]\npublic static Byte[] StructToBytes(Object structure, Byte[] bytes)\n{\nInt32 size = Marshal.SizeOf(structure);\nIntPtr buffer = Marshal.AllocHGlobal(size);\n\ntry\n{\nMarshal.StructureToPtr(structure, buffer, false);\nMarshal.Copy(buffer, bytes, 0, size);\n\nreturn bytes;\n}\nfinally\n{\nMarshal.FreeHGlobal(buffer);\n}\n\n}\n\n//2、Byte[]转换为struct\npublic static Object BytesToStruct(Byte[] bytes, Type strcutType)\n{\nInt32 size = Marshal.SizeOf(strcutType);\nIntPtr buffer = Marshal.AllocHGlobal(size);\n\ntry\n{\nMarshal.Copy(bytes, 0, buffer, size);\n\nreturn Marshal.PtrToStructure(buffer, strcutType);\n}\nfinally\n{\nMarshal.FreeHGlobal(buffer);\n}\n}\n\npublic static Byte[] PtrToBytes(IntPtr ptr, int size)\n{\ntry\n{\nByte[] bytes = new Byte[size];\nMarshal.Copy(ptr, bytes, 0, size);\n\nreturn bytes;\n}\nfinally\n{\n}\n\n}\n}\n\n"
                                                       "[StructLayoutAttribute(LayoutKind.Sequential)]\npublic struct Ptr_Core\n{\npublic IntPtr ptr;\n}\n\n[StructLayoutAttribute(LayoutKind.Sequential)]\npublic struct MultiDimPtr<T>\nwhere T : new()\n{\n\npublic Ptr_Core outer_mptr;\npublic IntPtr inner_mptr;\nint ndim;\n\npublic MultiDimPtr(int _ndim)\n{\nif (_ndim == 0)\n{\nthrow new Exception();\n}\nndim = _ndim;\nouter_mptr = new Ptr_Core();\ninner_mptr = new IntPtr();\n\nfor(int i=0;i<_ndim-1;++i)\n{\nPtr_Core pcore = new Ptr_Core();\nIntPtr t_ptr = Marshal.AllocHGlobal(Marshal.SizeOf(pcore));\npcore.ptr = outer_mptr.ptr;\nMarshal.StructureToPtr(pcore, t_ptr, false);\nouter_mptr.ptr = t_ptr;\ninner_mptr = t_ptr;\n}\n}\n\npublic void Set(IntPtr _ptr)\n{\nPtr_Core pwork;\nif (ndim == 1)\n{\npwork = outer_mptr;\n}\nelse\n{\npwork = (Ptr_Core)Marshal.PtrToStructure(inner_mptr, typeof(Ptr_Core));\n}\n\npwork.ptr = _ptr;\nMarshal.StructureToPtr(pwork, inner_mptr, false);\n}\n\npublic void Set(T obj)\n{\nPtr_Core pwork;\nif(ndim == 1)\n{\npwork = outer_mptr;\n}\nelse\n{\npwork = (Ptr_Core)Marshal.PtrToStructure(inner_mptr, typeof(Ptr_Core));\n}\n\n\nunsafe\n{\npwork.ptr = Marshal.AllocHGlobal(Marshal.SizeOf(obj));\n}\nMarshal.StructureToPtr(obj, pwork.ptr, false);\nMarshal.StructureToPtr(pwork, inner_mptr, false);\n}\n\npublic T Get()\n{\nPtr_Core pwork;\nif (ndim == 1)\n{\npwork = outer_mptr;\n}\nelse\n{\npwork = (Ptr_Core)Marshal.PtrToStructure(inner_mptr, typeof(Ptr_Core));\n}\n\nT obj = (T)Marshal.PtrToStructure(pwork.ptr, typeof(T));\nreturn obj;\n}\n}\n\n"
                                                       "public struct UmArray<T> where T:new()\n{\npublic UmArray(params int[] args)\n{\ntype = typeof(T);\ndim = args;\nelm_size = Marshal.SizeOf(new T());\nint arr_size = 1;\nfor (int i = 0; i < args.Length;++i)\n{\nif (args[i]==0)\n{\nthrow new IndexOutOfRangeException();\n}\narr_size *= (args[i]);\n}\narr = Marshal.AllocHGlobal((int)arr_size * elm_size);\nfor(int j=0;j<arr_size;++j)\n{\nMarshal.StructureToPtr(0, (IntPtr)((int)(arr + j * elm_size)), false);\n}\n}\n\npublic T this[params int[] args]\n{\nget\n{\nreturn Get(args);\n}\nset\n{\nSet(value, args);\n}\n}\n\nprivate T Get(params int[] args)\n{\nif (args.Length != dim.Length)\n{\nthrow new IndexOutOfRangeException();\n}\nint indx = 0;\nfor (int i = 0; i < args.Length - 1; ++i)\n{\nif (args[i] >= dim[i])\n{\nthrow new IndexOutOfRangeException();\n}\nint t_size = 1;\nfor (int j = i + 1; j < dim.Length; ++j)\n{\nt_size *= dim[j];\n}\nindx += (args[i]) * (t_size);\n}\nif (args[args.Length - 1] >= dim[args.Length - 1])\n{\nthrow new IndexOutOfRangeException();\n}\nindx += (args[args.Length - 1]);\nindx *= elm_size;\nreturn (T)Marshal.PtrToStructure((IntPtr)((int)(arr + indx)), typeof(T));\n}\n\nprivate void Set(T val, params int[] args)\n{\nif (args.Length != dim.Length)\n{\nthrow new IndexOutOfRangeException();\n}\nint indx = 0;\nfor (int i = 0; i < args.Length - 1; ++i)\n{\nif (args[i] >= dim[i])\n{\nthrow new IndexOutOfRangeException();\n}\nint t_size = 1;\nfor (int j = i + 1; j < dim.Length; ++j)\n{\nt_size *= dim[j];\n}\nindx += (args[i]) * (t_size);\n}\nif (args[args.Length - 1] >= dim[args.Length - 1])\n{\nthrow new IndexOutOfRangeException();\n}\nindx += (args[args.Length - 1]);\nindx *= elm_size;\nMarshal.StructureToPtr(val, (IntPtr)((int)(arr + indx)), false);\n}\n\npublic IntPtr arr;\npublic Type type;\npublic int[] dim;\nprivate int elm_size;\n}\n\npublic struct MArray<T> where T : new()\n{\npublic MArray(params int[] args)\n{\ntype = typeof(T);\ndim = args;\nint arr_size = 1;\nfor (int i = 0; i < args.Length;++i)\n{\nif (args[i]==0)\n{\nthrow new IndexOutOfRangeException();\n}\narr_size *= (args[i]);\n}\narr = new T[arr_size];\n}\n\npublic T this[params int[] args]\n{\nget\n{\nreturn Get(args);\n}\nset\n{\nSet(value, args);\n}\n}\n\nprivate T Get(params int[] args)\n{\nif(args.Length != dim.Length)\n{\nthrow new IndexOutOfRangeException();\n}\nint indx = 0;\nfor (int i = 0; i < args.Length - 1; ++i)\n{\nif(args[i] >= dim[i])\n{\nthrow new IndexOutOfRangeException();\n}\nint t_size = 1;\nfor (int j = i + 1; j < dim.Length; ++j)\n{\nt_size*=dim[j];\n}\nindx += (args[i])*(t_size);\n}\nif (args[args.Length - 1] >= dim[args.Length - 1])\n{\nthrow new IndexOutOfRangeException();\n}\nindx += (args[args.Length-1]);\nreturn arr[indx];\n}\n\nprivate void Set(T val, params int[] args)\n{\nif (args.Length != dim.Length)\n{\nthrow new IndexOutOfRangeException();\n}\nint indx = 0;\nfor (int i = 0; i < args.Length-1; ++i)\n{\nif (args[i] >= dim[i])\n{\nthrow new IndexOutOfRangeException();\n}\nint t_size = 1;\nfor (int j = i + 1; j < dim.Length; ++j)\n{\nt_size *= dim[j];\n}\nindx += (args[i]) * (t_size);\n}\nif (args[args.Length - 1] >= dim[args.Length - 1])\n{\nthrow new IndexOutOfRangeException();\n}\nindx += (args[args.Length - 1]);\narr[indx] = val;\n}\n\npublic T[] arr;\npublic Type type;\npublic int[] dim;\n}\n\n",
                "}\n}"]
            self.arr_sz_func_call_rule = ["[System.Runtime.InteropServices.DllImport(\"" + self.csharp_evn.sz_lib_name +
                                          "\", EntryPoint = \"",
                                          "\", SetLastError = true,CharSet = CharSet.Auto, ExactSpelling = false, "
                                          "CallingConvention = CallingConvention.StdCall)]"]

    def __make_content(self, _l_mapping):
        if type(_l_mapping) is not MappingList:
            raise "type(_l_mapping) must MappingList"
        # 遍历映射API列表，逐个将function模型->csharp代码
        sz_fun_info = ""
        for fn in _l_mapping.arr_function:
            print(fn.sz_ELM_Name)
            if self.csharp_evn.find(fn, "func") is False:
                '''
                在CSharp全局上下文中未找到函数对象，若未找到说明之前未转换，执行转换工作
                '''
                obj_rule = FunctionMappingRule(fn)
                fn_type, fn_other_info = obj_rule.mapping(CSharpFunction(),
                                                          {'var_type': "fn_arg", 'g_evn': self.csharp_evn})
                sz_fun_info = sz_fun_info + fn_type
                if fn_other_info != ['', '']:
                    self.csharp_evn.arr_sz_com.append(fn_other_info[0] + fn_other_info[1])
                self.csharp_evn.arr_obj_fn.append(fn)
        # 遍历映射复合类型列表，输出
        sz_com_info = ""
        for sz_com in self.csharp_evn.arr_sz_com:
            sz_com_info = sz_com_info + sz_com
        return sz_com_info + sz_fun_info


class CSharpEnumerator(MappingCore):
    def __init__(self):
        super(CSharpEnumerator, self).__init__(g_sz_lang)
        pass

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class CSharpFunction(MappingCore):
    class CSharpFunctionEvn(MappingEvn):
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
        super(CSharpFunction, self).__init__(g_sz_lang)
        self.obj_fn_evn = CSharpFunction.CSharpFunctionEvn()

    def mapping_core(self, _elm, _data=None):
        """
        函数对象映射
        :param _elm:
        :param _data: CSharp全局上下文对象 CSharpGlobalEvn 或 CSharpCompoundEvn
        :return: 返回CSharp函数原型, 以及函数附加信息，函数涉及的复合类型
        """
        if type(_elm) is not clt.Function:
            raise "type(_elm) must clt.Function"
        if "cb" in _data.keys() and _data['cb'] == 1:
            self.obj_fn_evn.sz_fn_name = 'invoke'
        else:
            self.obj_fn_evn.sz_fn_name = _elm.sz_ELM_Name

        # 1.转换返回值
        sz_ret_other_info = ['', '']  # 返回值的附带信息，如果返回值类型涉及某种复合数据类型，信息则为该复合类型的csharp代码
        sz_ret_type = ""  # 返回值csharp类型名
        if type(_elm.obj_Fn_DT_Ret) is clt.Compound:
            if _data is None \
                    or (issubclass(_data['g_evn'].__class__, MappingEvn) and _data['g_evn'].find(_elm.stru_Var_TData,
                                                                                                 'com') is False):
                '''
                若该复合类型未被转换过, 则进行CSharp转换
                '''
                obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                sz_type, sz_t_ret_other_info = obj_rule.mapping(CSharpCompound(), _data)
                sz_ret_other_info = sz_t_ret_other_info
                _data.arr_obj_com.append(_elm.stru_Var_TData)  # 记录复合类型已转换
            sz_ret_type = _elm.stru_Var_TData.sz_ELM_Name
        elif type(_elm.obj_Fn_DT_Ret) is clt.DPointer:
            obj_rule = DPointerMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(CSharpDPointer(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif type(_elm.obj_Fn_DT_Ret) is clt.BuildIn:
            obj_rule = BuildinMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(CSharpBuildin(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif type(_elm.obj_Fn_DT_Ret) is clt.AnotherName:
            obj_rule = AnotherNameMappingRule(_elm.obj_Fn_DT_Ret)
            sz_ret_type, sz_t_ret_other = obj_rule.mapping(CSharpAnotherName(), _data)
            sz_ret_other_info = sz_t_ret_other
        elif _elm.obj_Fn_DT_Ret is None:
            sz_ret_type = "void"
        else:
            raise "_elm type must in { Compound DPointer BuildIn }"
        sz_ret_type = sz_ret_type.strip()
        '''
        向CSharp上下文添加附加信息
        '''
        self.obj_fn_evn.sz_ret_type = sz_ret_type
        # if type(_data) is CSharpCompound.CSharpCompoundEvn:
        #     _data.arr_inline_compound.append(sz_ret_other_info)
        # elif type(_data) is CSharpMappingEngine.CSharpGlobalEvn:
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
            sz_arg_type, sz_t_arg_other_info = obj_rule.mapping(CSharpVariable(), _data)
            sz_arg_other_info[0] = sz_arg_other_info[0] + sz_t_arg_other_info[0]
            sz_arg_other_info[1] = sz_arg_other_info[1] + sz_t_arg_other_info[1]
            sz_arg_type = sz_arg_type.strip()
            self.obj_fn_evn.arr_args_info.append(sz_arg_type)
            # self.obj_fn_evn.arr_args_info[arg.sz_ELM_Name] = sz_arg_type
            # '''
            # 向CSharp上下文添加附加信息
            # '''
            # if type(_data) is CSharpCompound.CSharpCompoundEvn:
            #     _data.arr_inline_compound.append(sz_arg_other_info)
            # elif type(_data) is CSharpMappingEngine.CSharpGlobalEvn:
            #     _data.arr_sz_com.append(sz_arg_other_info)
            # else:
            #     pass
        _data['var_type'] = sz_var_type
        sz_fn_info = "public " + str(self.obj_fn_evn) + ";\n"
        return sz_fn_info, [sz_ret_other_info[0] + sz_arg_other_info[0], sz_ret_other_info[1] + sz_arg_other_info[1]]


class CSharpDefine(MappingCore):
    def __init__(self):
        super(CSharpDefine, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class CSharpAnotherName(MappingCore):
    def __init__(self):
        super(CSharpAnotherName, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        sz_other_info = ['', '']
        if type(_elm.stru_AN_DT) is clt.Compound:
            if _data is not None:
                if _data['g_evn'].find(_elm.stru_AN_DT, 'com') is False:
                    obj_rule = CompoundMappingRule(_elm.stru_AN_DT)
                    sz_type, sz_other_info = obj_rule.mapping(CSharpCompound(), _data)
                    _data['g_evn'].arr_obj_com.append(_elm.stru_AN_DT)
                else:
                    sz_type = _elm.stru_AN_DT.sz_ELM_Name + ' '
            else:
                if _elm.stru_AN_DT.is_inline() is True:
                    obj_rule = CompoundMappingRule(_elm.stru_AN_DT)
                    sz_type, sz_other_info = obj_rule.mapping(CSharpCompound(), _data)
                else:
                    sz_type = _elm.stru_AN_DT.sz_ELM_Name + ' '
        elif type(_elm.stru_AN_DT) is clt.DPointer:
            obj_rule = DPointerMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(CSharpDPointer(), _data)
        elif type(_elm.stru_AN_DT) is clt.BuildIn:
            obj_rule = BuildinMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(CSharpBuildin())
        elif type(_elm.stru_AN_DT) is clt.AnotherName:
            obj_rule = AnotherNameMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(CSharpAnotherName(), _data)
        elif type(_elm.stru_AN_DT) is clt.FPointer:
            obj_rule = FPointerMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(CSharpFPointer(), _data)
        elif type(_elm.stru_AN_DT) is clt.Enum:
            obj_rule = EnumMappingRule(_elm.stru_AN_DT)
            sz_type, sz_other_info = obj_rule.mapping(CSharpEnum())
        else:
            raise "_elm type must in { Compound DPointer BuildIn }"
        return sz_type, sz_other_info


class CSharpVariable(MappingCore):
    tuple_var_type = ("fn_arg", "com_member")

    def __init__(self):
        super(CSharpVariable, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        if _data is None or type(_data) is not dict \
                or _data["var_type"] is None or _data["var_type"] not in self.tuple_var_type:
            raise "type(_data) must dict"

        # [RECORD] 20190410 变量映射
        sz_other_info = ['', '']
        sz_type = ""
        if type(_elm.stru_Var_TData) is clt.Compound:
            """
            @brief 复合类型转换，分开处理的原因，复合类型成员变量类型可能是内联，此时其映射代码需要写入复合类型的环境对象中
                   而函数参数的类型映射代码,需要写入csharp的环境对象中
            """
            if _data["var_type"] == 'fn_arg':
                '''
                变量为函数参数
                '''
                if _data["g_evn"].find(_elm.stru_Var_TData, 'com') is False:
                    _data["g_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                    obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                    sz_type, sz_t_other = obj_rule.mapping(CSharpCompound(), _data)
                    sz_other_info = sz_t_other
                else:
                    sz_type = _elm.stru_Var_TData.sz_ELM_Name
            elif _data["var_type"] == 'com_member':
                '''
                变量为复合类型成员
                '''
                if _data["com_evn"].find(_elm.stru_Var_TData, 'com') is False \
                        and _data["g_evn"].find(_elm.stru_Var_TData, 'com') is False:
                    obj_rule = CompoundMappingRule(_elm.stru_Var_TData)
                    sz_type, sz_t_other = obj_rule.mapping(CSharpCompound(), _data)
                    sz_other_info = sz_t_other

                    """
                    内联和非内联类型成员处理
                    """
                    if _elm.stru_Var_TData.is_inline() is True:
                        _data["com_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                    else:
                        _data["g_evn"].arr_obj_com.append(_elm.stru_Var_TData)
                else:
                    sz_type = _elm.stru_Var_TData.sz_ELM_Name
        elif type(_elm.stru_Var_TData) is clt.DPointer:
            """
            @brief 变量为指针类型
            """
            obj_rule = DPointerMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other = obj_rule.mapping(CSharpDPointer(), _data)
            sz_other_info = sz_t_other
        elif type(_elm.stru_Var_TData) is clt.BuildIn:
            """
            @brief 变量为c++内建对象
            """
            obj_rule = BuildinMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other, = obj_rule.mapping(CSharpBuildin())
            sz_other_info = sz_t_other
        elif type(_elm.stru_Var_TData) is clt.AnotherName:
            """
            @brief 变量为重命名对象
            """
            obj_rule = AnotherNameMappingRule(_elm.stru_Var_TData)
            sz_type, sz_t_other = obj_rule.mapping(CSharpAnotherName(), _data)
            sz_other_info = sz_t_other
        else:
            print(type(_elm.stru_Var_TData))
            raise "_elm type must in { Compound DPointer BuildIn }"
        sz_type = sz_type.strip()

        def make_access_control():
            if _elm.sz_Var_access_control.strip() in clt.Variable.tuple_var_access_control:
                return _elm.sz_Var_access_control.strip()
            else:
                return "public"

        def make_decorator():

            def make_arr_size(_sz_TD_ArrSize):
                iSize = 0
                for it_dim in _sz_TD_ArrSize:
                    if type(it_dim) is int:
                        iSize = iSize + it_dim
                    elif type(it_dim) is str:
                        pass
                    elif type(it_dim) is clt.Define:
                        iSize = iSize + it_dim.obj_real_value
                    else:
                        raise "type(it_dim) must in {int str DDefine}"
                return str(iSize)

            if _elm.sz_TD_ArrSize is not None and len(_elm.sz_TD_ArrSize) > 1:
                return "[MarshalAsAttribute(UnmanagedType.ByValArray, SizeConst = " + make_arr_size(_elm.sz_TD_ArrSize) + \
                       ", ArraySubType = UnmanagedType.I1)]\n"
            else:
                return ""

        def make_type():
            if _elm.sz_TD_ArrSize is not None and len(_elm.sz_TD_ArrSize) > 1:
                return sz_type + "[]"
            else:
                return sz_type

        sz_var_info = ""
        if _data["var_type"] == "fn_arg":
            sz_var_info = make_type() + ' ' + _elm.sz_ELM_Name
        elif _data["var_type"] == "com_member":
            sz_var_info = make_decorator() + make_access_control() + " " + make_type() + ' ' + _elm.sz_ELM_Name + ';\n'

        return sz_var_info, sz_other_info


########################################
#            以下为数据类型
########################################

class CSharpBuildin(MappingCore):
    dict_buildin_map = {
        "int": ("int", "c_int", "u_int", "c_u_int"),
        "byte": ("char", "c_char", "u_char", "c_u_char"),
        "short": ("short", "c_short", "u_short", "c_u_short"),
        "System.Int64": ("longlong", "c_longlong", "u_longlong", "c_u_longlong",
                         "int64", "u_int64", "c_int64", "c_u_int64"),
        "float": ("float", "c_float"),
        "double": ("double", "c_double"),
        "System.Int32": ("long", "u_long", "c_long", "c_u_long"),
        "System.IntPtr": ('p_short', 'p_int', 'p_long', 'p_longlong',
                          'p_int64', 'p_float', 'p_double', 'p_u_short',
                          'p_u_int', 'p_u_long', 'p_u_longlong', 'p_u_int64',
                          'p_c_short', 'p_c_int', 'p_c_long', 'p_c_longlong',
                          'p_c_int64', 'p_c_float', 'p_c_double', 'p_c_u_short',
                          'p_c_u_int', 'p_c_u_long', 'p_c_u_longlong', 'p_c_u_int64',
                          'p_void', "p_char", 'p_c_char', 'p_u_char', 'p_c_u_char'),
        "void": ("void",)
    }

    def __init__(self):
        super(CSharpBuildin, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        for key in self.dict_buildin_map:
            if _elm.sz_BI_Type in self.dict_buildin_map[key]:
                return key, ['', '']
        return "$$unknown$$", ['', '']


class CSharpDPointer(MappingCore):
    def __init__(self):
        super(CSharpDPointer, self).__init__(g_sz_lang)

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
                    sz_type, sz_t_other = obj_rule.mapping(CSharpCompound(), _data)
            elif _data["var_type"] == 'com_member':
                if _data["com_evn"].find(_elm.stru_DP_Type, 'com') is False \
                        and _data["g_evn"].find(_elm.stru_DP_Type, 'com') is False:
                    '''
                    若该复合类型未被检索过
                    '''
                    obj_rule = CompoundMappingRule(_elm.stru_DP_Type)
                    sz_type, sz_t_other = obj_rule.mapping(CSharpCompound(), _data)
                    if _elm.stru_DP_Type.is_inline() is True:
                        _data["com_evn"].arr_obj_com.append(_elm.stru_DP_Type)
                    else:
                        _data["g_evn"].arr_obj_com.append(_elm.stru_DP_Type)
            return "System.IntPtr ", sz_t_other
        elif type(_elm.stru_DP_Type) is clt.AnotherName:
            # obj_rule = AnotherNameMappingRule(_elm.stru_DP_Type)
            return "System.IntPtr ", ['', '']
        elif type(_elm.stru_DP_Type) is clt.BuildIn:
            # obj_rule = AnotherNameMappingRule(_elm.stru_DP_Type)
            # if _elm.stru_DP_Type.sz_BI_Type in CSharpBuildin.dict_buildin_map['byte']:
            #     return 'String ', ['', '']
            return "System.IntPtr ", ['', '']
        elif type(_elm.stru_DP_Type) is clt.DPointer:
            # TODO: 多级指针，目前代码中没有，暂不处理
            obj_rule = DPointerMappingRule(_elm.stru_DP_Type)
            sz_type, sz_t_other = obj_rule.mapping(CSharpDPointer(), _data)
            if sz_type.strip() == "System.IntPtr":
                return "Ptr_Core ", ['', '']
            else:
                return "System.IntPtr ", ['', '']
        else:
            raise "_elm type must in { Compound DPointer AnotherName}"


class CSharpFPointer(MappingCore):
    def __init__(self):
        super(CSharpFPointer, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        if type(_elm) is not clt.FPointer:
            raise "type(_elm) is not clt.FPointer"
        sz_fp_info = "public interface " + _elm.sz_ELM_Name + " extends Callback{\n"
        _data['cb'] = 1
        obj_rule = FunctionMappingRule(_elm.stru_FP_fn)
        fp_type, fp_other_info = obj_rule.mapping(CSharpFunction(), _data)
        sz_fp_info = sz_fp_info + fp_type + "}\n"
        return _elm.sz_ELM_Name + ' ', [fp_other_info[0], sz_fp_info + fp_other_info[1]]


class CSharpReference(MappingCore):
    def __init__(self):
        super(CSharpReference, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "$$unknown$$", ['', '']


class CSharpCompound(MappingCore):
    class UnionMaker:
        arr_sz_head = (
            "[StructLayoutAttribute(LayoutKind.Sequential)]\npublic struct ",
            "{\npublic static int GetSize()\n{\nreturn size;\n}\n\n// SizeConst需要保证大于等于联合体最大元素长度\n[MarshalAsAttribute(UnmanagedType.ByValArray, SizeConst = ",
            ", ArraySubType = UnmanagedType.I1)]\npublic byte[] handle;\npublic static int size = ",
            ";\n\npublic void Init()\n{\nhandle = new byte[GetSize()];\nfor (int i = 0; i < GetSize(); ++i)\n{\nhandle[i] = 0;\n}\n}\n",
            "}\n"
        )
        sz_fn_Get = "public $RET$ Get_$MEMBER$()\n{\n$RET$ stru = ($RET$)MemCopyer.BytesToStruct(handle, typeof($RET$));\nreturn stru;\n}\n"
        sz_fn_Set = "public void Set_$MEMBER$($RET$ stru)\n{\nMemCopyer.StructToBytes(stru,handle);\n}\n"

        @staticmethod
        def make_head(_sz_un_name, _un_size):
            if type(_sz_un_name) is not str or _sz_un_name == "":
                raise "type(_sz_un_name) is not str or _sz_un_name == NULL"
            if type(_un_size) is not int: #or _un_size <= 0:
                raise "type(_un_size) is not int or _un_size <= 0"
            return CSharpCompound.UnionMaker.arr_sz_head[0] + _sz_un_name + \
                   CSharpCompound.UnionMaker.arr_sz_head[1] + str(_un_size) + \
                   CSharpCompound.UnionMaker.arr_sz_head[2] + str(_un_size) + \
                   CSharpCompound.UnionMaker.arr_sz_head[3]

        @staticmethod
        def make_contend(_obj_com_evn, _elm):
            """
            构造结构体成员代码
            :param _obj_com_evn: CSharpCompound 对象的环境对象
            :param _elm: Element 对象
            :return:
            """

            def __make_GetSet_fn(_sz_ret_type, _sz_var_name):
                sz_g_fn = CSharpCompound.UnionMaker.sz_fn_Get.replace("$RET$", _sz_ret_type)
                sz_g_fn = sz_g_fn.replace("$MEMBER$", _sz_var_name)
                sz_s_fn = CSharpCompound.UnionMaker.sz_fn_Set.replace("$RET$", _sz_ret_type)
                sz_s_fn = sz_s_fn.replace("$MEMBER$", _sz_var_name)
                return sz_g_fn + "\n" + sz_s_fn + "\n"

            sz_evn = ""
            for it in _obj_com_evn.arr_inline_compound:
                sz_evn = sz_evn + it
            for member in _elm.tree_Com_members:
                if type(member) is clt.Variable:
                    sz_evn = sz_evn + __make_GetSet_fn(member.stru_Var_TData.sz_ELM_Name, member.sz_ELM_Name)
            for it in _obj_com_evn.arr_function:
                sz_evn = sz_evn + it
            return sz_evn

    class StructMaker:
        @staticmethod
        def make_contend(_obj_com_evn, _elm):
            """
            构造结构体成员代码
            :param _obj_com_evn: CSharpCompound 对象的环境对象
            :param _elm: Element 对象
            :return:
            """

            sz_evn = ""
            for it in _obj_com_evn.arr_inline_compound:
                sz_evn = sz_evn + it
            for it in _obj_com_evn.arr_variable:
                sz_evn = sz_evn + it
            for it in _obj_com_evn.arr_function:
                sz_evn = sz_evn + it
            return sz_evn

    class CSharpCompoundEvn(MappingEvn):
        def __init__(self):
            super(CSharpCompound.CSharpCompoundEvn, self).__init__(g_sz_lang)
            self.arr_inline_compound = []
            self.arr_variable = []
            self.arr_function = []

    def __init__(self):
        super(CSharpCompound, self).__init__(g_sz_lang)
        self.obj_com_evn = CSharpCompound.CSharpCompoundEvn()

    def mapping_core(self, _elm, _data=None):
        if type(_elm) is not clt.Compound:
            raise "issubclass(_elm, clt.TData) is not True"
        sz_com_info = ""
        sz_other_info = ""

        # 1.产生复合类型头代码
        if _elm.i_Com_Type == 1:
            '''
            struct
            '''
            sz_com_info = "[StructLayoutAttribute(LayoutKind.Sequential)]\npublic struct " + _elm.sz_ELM_Name + "\n{\n"
        elif _elm.i_Com_Type == 2:
            '''
            class
            '''
            pass
        elif _elm.i_Com_Type == 3:
            '''
            union
            '''
            sz_com_info = CSharpCompound.UnionMaker.make_head(_elm.sz_ELM_Name, _elm.obj_TD_size.i_size)
        else:
            raise "_elm.i_Com_Type must in {1,2,3}"

        # 解析复合类型成员
        for member in _elm.tree_Com_members:
            '''
            遍历成员对象，逐个解析成员对象类型
            '''
            if type(member) is clt.Variable:
                obj_rule = VariableMappingRule(member)
                sz_var_info, t_sz_other_info = obj_rule.mapping(CSharpVariable(), _data={"var_type": "com_member",
                                                                                         "com_evn": self.obj_com_evn,
                                                                                         "g_evn": _data["g_evn"]})
                self.obj_com_evn.arr_variable.append(sz_var_info)

                # FIXMED: 判断t_sz_other_info返回的附加信息是内联还是外部，进行不同处理
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

        # 产生复合类型成源代码
        sz_com_info = sz_com_info + self.__make_contend(_elm) + "}\n"

        if _elm.is_inline() is True:
            return _elm.sz_ELM_Name, [sz_com_info, sz_other_info]
        else:
            return _elm.sz_ELM_Name, ['', sz_other_info + sz_com_info]

    def __make_contend(self, _elm):
        sz_evn = ""
        if _elm.i_Com_Type == 1 or _elm.i_Com_Type == 2:
            '''
            struct
            '''
            sz_evn = CSharpCompound.StructMaker.make_contend(self.obj_com_evn, _elm)
            pass
        elif _elm.i_Com_Type == 3:
            '''
            union
            '''
            sz_evn = CSharpCompound.UnionMaker.make_contend(self.obj_com_evn, _elm)
            pass
        else:
            raise "_elm.i_Com_Type must in {1,2,3}"
        return sz_evn


class CSharpEnum(MappingCore):
    def __init__(self):
        super(CSharpEnum, self).__init__(g_sz_lang)

    def mapping_core(self, _elm, _data=None):
        return "int ", ['', '']
