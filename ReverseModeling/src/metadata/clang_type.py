class Element:
    def __init__(self, _name):
        self.sz_ELM_Define = ''
        self.sz_ELM_Header = ''
        self.sz_XFile_refid = ''
        if type(_name) is not str:
            raise 'arg <_name> must a str'
        self.sz_ELM_Name = _name
        self.b_is_complete = False


class AnotherName(Element):
    def __init__(self, _name):
        super(AnotherName, self).__init__(_name)
        self.stru_AN_DT = None
        self.sz_AN_refid = ''


class Enumerator(Element):
    def __init__(self, _name, _ivalue=None):
        super(Enumerator, self).__init__(_name)
        self.i_Emor_value = _ivalue
        self.sz_Enumor_refid = ''


class Function(Element):
    def __init__(self, _name):
        super(Function, self).__init__(_name)
        self.arr_Fn_args = []
        self.sz_Fn_refid = ''
        self.obj_Fn_DT_Ret = None


class Define(Element):
    dict_Def_Type = {
        0: 'Unknown',
        1: 'OtherDef',
        2: 'VarDef',
        3: 'DDef',
        4: 'FnDef',
    }

    def __init__(self, _name, _itype=0):
        super(Define, self).__init__(_name)
        self.i_Def_Type = _itype
        self.sz_Def_value = None
        self.sz_Def_refid = ''
        self.obj_real_value = None


class TData(Element):
    dict_TD_Type = {
        0: 'Unknown',
        1: 'DPointer',
        2: 'Reference',
        3: 'BuildIn',
        4: 'Compound',
        5: 'Enum',
        6: 'DDefine',
    }

    def __init__(self, _name, _itype=0):
        super(TData, self).__init__(_name)
        self.arr_Data_AnotherName = []
        if _itype < 0 or _itype >= self.dict_TD_Type.__len__():
            raise 'arg <_itype> must in \'self.dict_TD_Type\''
        self.i_TD_Type = _itype
        self.obj_TD_size = None


class DPointer(TData):
    def __init__(self, _name, _data=None):
        super(DPointer, self).__init__(_name, 1)
        # if not issubclass(type(_data), TData):
        #     raise 'arg <_data> must a \'class TData\''
        self.stru_DP_Type = _data


class FPointer(TData):
    def __init__(self, _name):
        super(FPointer, self).__init__(_name)
        self.stru_FP_fn = None  # 函数指针指向的函数对象 Function
        self.sz_PFn_refid = ''


class Reference(TData):
    def __init__(self, _name):
        super(Reference, self).__init__(_name, 2)


class BuildIn(TData):
    dict_BI_Type = {
        'Unknown',
        'bool',
        'void',
        'p_void',

        # 数值
        'char',
        'short',
        'int',
        'long',
        'longlong',
        'int64',
        'float',
        'double',

        'u_char',
        'u_short',
        'u_int',
        'u_long',
        'u_longlong',
        'u_int64',

        'c_char',
        'c_short',
        'c_int',
        'c_long',
        'c_longlong',
        'c_int64',
        'c_float',
        'c_double',

        'c_u_char',
        'c_u_short',
        'c_u_int',
        'c_u_long',
        'c_u_longlong',
        'c_u_int64',

        'p_char',
        'p_short',
        'p_int',
        'p_long',
        'p_longlong',
        'p_int64',
        'p_float',
        'p_double',

        'p_u_char',
        'p_u_short',
        'p_u_int',
        'p_u_long',
        'p_u_longlong',
        'p_u_int64',

        'p_c_char',
        'p_c_short',
        'p_c_int',
        'p_c_long',
        'p_c_longlong',
        'p_c_int64',
        'p_c_float',
        'p_c_double',

        'p_c_u_char',
        'p_c_u_short',
        'p_c_u_int',
        'p_c_u_long',
        'p_c_u_longlong',
        'p_c_u_int64',

        'pp_char',
        'pp_short',
        'pp_int',
        'pp_long',
        'pp_longlong',
        'pp_int64',
        'pp_float',
        'pp_double',

        'pp_c_char',
        'pp_c_short',
        'pp_c_int',
        'pp_c_long',
        'pp_c_longlong',
        'pp_c_int64',
        'pp_c_double',
        'pp_c_float',

        'pp_u_char',
        'pp_u_short',
        'pp_u_int',
        'pp_u_long',
        'pp_u_longlong',
        'pp_u_int64',

        'pp_c_u_char'
        'pp_c_u_short',
        'pp_c_u_int',
        'pp_c_u_long',
        'pp_c_u_longlong',
        'pp_c_u_int64',
    }

    def __init__(self, _name, _sztype='Unknown'):
        super(BuildIn, self).__init__(_name, 3)
        if _sztype not in self.dict_BI_Type:
            print("error:" + _sztype)
            raise 'arg <_itype> must in \'self.dict_BI_Type\''
        self.sz_BI_Type = _sztype


class Compound(TData):
    dict_Com_Type = {
        0: 'Unknown',
        1: 'Struct',
        2: 'Class',
        3: 'Union',
    }

    def __init__(self, _name, _itype=0):
        super(Compound, self).__init__(_name, 4)
        if type(_name) is not str:
            raise "_name must str"
        self.arr_Com_members = []
        # 复合数据类型的树状成员变量关系，用于最终输出
        self.tree_Com_members = []
        self.i_Com_Type = _itype  # dict_Com_Type复合类型中的一个
        self.b_is_inline = False

    def is_contain_inline_member(self):
        return len(self.arr_Com_members) > len(self.tree_Com_members)

    def is_inline(self):
        return self.b_is_inline

    def is_anonymity(self):
        return self.sz_ELM_Name == ''

    def find_member(self, _refid):
        if type(_refid) is not str:
            raise "_refid must str"
        for it in self.arr_Com_members:
            if type(it) is Variable:
                if it.sz_Var_refid == _refid:
                    return it
            elif type(it) is Function:
                if it.sz_Fn_refid == _refid:
                    return it
        return None

    def find_member_by_name(self, _name):
        if type(_name) is not str:
            raise "_refid must str"
        for it in self.arr_Com_members:
            if type(it) is Variable:
                if it.sz_ELM_Name == _name:
                    return it
            elif type(it) is Function:
                if it.sz_ELM_Name == _name:
                    return it
        return None

    def remove_member_by_value(self, _val):
        """
        移除 self.arr_Com_members 列表中第一个匹配_val值得成员，目的是避免内联类型结构矫正时错误
        :param _val:
        :return:
        """
        self.arr_Com_members.remove(_val)


class Enum(TData):
    def __init__(self, _name):
        super(Enum, self).__init__(_name, 5)
        if type(_name) is not str:
            raise "_name must str"
        self.arr_Enum_members = []
        self.sz_Enum_refid = ''


class DDefine(Define, TData):
    def __init__(self, _name, _tdata, _def=None):
        Define.__init__(_name)
        TData.__init__(_name, 6)
        if type(_tdata) is not TData:
            raise 'arg <_data> must a \'class TData\''
        self.stru_TData = _tdata
        if type(_def) is Define:
            self.sz_ELM_Name = _def.sz_ELM_Name
            self.sz_ELM_Define = _def.sz_ELM_Define
            self.sz_ELM_Header = _def.sz_ELM_Header
            self.sz_Def_refid = _def.sz_Def_refid
            self.sz_Def_value = _def.sz_Def_value


class Variable(Element):
    tuple_var_access_control = (
        "static",
        "public",
        "protected",
        "private"
    )

    def __init__(self, _name):
        super(Variable, self).__init__(_name)
        # if type(_data) is not TData:
        #     raise 'arg <_data> must a \'TData\''
        if type(_name) is not str:
            raise "_name must str"
        self.stru_Var_TData = None
        self.var_value = None
        self.sz_Var_refid = ''
        self.sz_Var_access_control = ''
        self.b_is_const = False
        self.sz_TD_ArrSize = []  # 数组维数

    def get_all_dim_size(self):
        if type(self.sz_TD_ArrSize) is not list:
            raise "type(self.sz_TD_ArrSize) is not list"
        arr_size = []
        for i in range(len(self.sz_TD_ArrSize)):
            arr_size.append(self.get_dim_size(i))
        return arr_size

    def get_dim_size(self, _dim):
        """
        计算指定数组维数，重点是解析数字宏、全局变量、常亮等
        :param _dim:
        :return:
        """
        if type(_dim) is not int \
                or _dim < 0 or _dim >= len(self.sz_TD_ArrSize):
            raise "_dim err"
        if type(self.sz_TD_ArrSize[_dim]) is Define and self.sz_TD_ArrSize[_dim].i_Def_Type in (2, 3):
            return str(self.sz_TD_ArrSize[_dim].obj_real_value)
        else:
            return self.sz_TD_ArrSize[_dim]

    def make_arr_size(self):
        if self.sz_TD_ArrSize is not None:
            sz_out = ''
            for it in self.sz_TD_ArrSize:
                sz_out = sz_out + '['
                sz_out = sz_out + str(it)
                sz_out = sz_out + ']'
            return sz_out
        else:
            return ''


def test_fn(data):
    if data.i_TD_Type == 1:
        a = data.stru_DP_Type
    elif data.i_TD_Type == 3:
        a = data.i_BI_Type


if __name__ == '__main__':
    obj_int = BuildIn('sss', 3)
    print(obj_int.i_TD_Type)
    test_fn(obj_int)
    a = [1, '1', {0: 1, 1: 2}]
    pass
