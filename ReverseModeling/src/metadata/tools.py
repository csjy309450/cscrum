from metadata import clang_type as clt


class Stack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.items = []

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return len(self.items) == 0

    # 返回栈顶元素
    def top(self):
        if len(self.items) == 0:
            return None
        return self.items[len(self.items) - 1]

    def bottom(self):
        if len(self.items) == 0:
            return None
        return self.items[0]

    # 返回栈的大小
    def size(self):
        return len(self.items)

    # 把新的元素堆进栈里面（程序员喜欢把这个过程叫做压栈，入栈，进栈……）
    def push(self, item):
        self.items.append(item)

    # 把栈顶元素丢出去（程序员喜欢把这个过程叫做出栈……）
    def pop(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()


class TDSize:
    def __init__(self):
        self.i_size = -1  # 数据类型长度
        self.dict_init_offset = {}  # 成员对象起始偏移量
        self.i_max_member_size = -1  # 最大成员长度

    def count_size(self, _obj_dt):
        if _obj_dt is None or issubclass(type(_obj_dt), clt.TData) is False:
            raise "_obj_dt is None or issubclass(type(_obj_dt), TData)"
        if type(_obj_dt) is clt.BuildIn:
            self.i_max_member_size = \
                self.i_size = get_buildin_size(_obj_dt.sz_BI_Type)
        elif type(_obj_dt) is clt.FPointer or type(_obj_dt) is clt.DPointer:
            self.i_max_member_size = \
                self.i_size = get_pointer_size()
            pass
        elif type(_obj_dt) is clt.Compound:
            """
            结合 Compound 对象校正后的成员树形列表，递归计算复合类型数据长度
            :return None:
            """
            if _obj_dt.sz_ELM_Name == "NET_DVR_IGNORE_STRING":
                pass
            if _obj_dt.i_Com_Type == 1 or _obj_dt.i_Com_Type == 2:
                '''
                struct、class累加计算到最后一个元素截止时长度，还需要做复合类型整体的长度调整
                '''
                t_offset = self.__count_size_struct(_obj_dt)
                pass
            elif _obj_dt.i_Com_Type == 3:
                '''
                union计算到最后一个元素截止时最大长度，还需要做复合类型整体的长度调整
                '''
                t_offset = self.__count_size_union(_obj_dt)
                pass
            else:
                raise "not support this compound type"
            self.i_size = self.__min_N_greater(
                min(g_dev_evn.i_package_size, self.i_max_member_size),
                t_offset)
            pass
        else:
            pass
        pass

    def __count_size_union(self, _obj_dt):
        '''
        计算联合体大小
        :param _obj_dt:
        :return:
        '''
        if _obj_dt is None or _obj_dt.tree_Com_members is None or _obj_dt.i_Com_Type != 3:
            raise "self.obj_td_com is None or self.obj_td_com.tree_Com_members is None"
        if g_dev_evn is None or type(g_dev_evn) is not DevEnv:
            raise "tools.g_dev_evn is None or type(tools.g_dev_evn) is tools.DevEnv"
        t_i_max_size = 0
        for i in range(len(_obj_dt.tree_Com_members)):
            # TODO:<20190428> 遍历成员列表，计算t_i_pre_member_offset
            member = _obj_dt.tree_Com_members[i]
            if type(member) not in (clt.Variable, clt.Function):
                raise "type(member) not in (clt.Variable, clt.Function)"
            if type(member) is clt.Function:
                continue
            member_dtype = member.stru_Var_TData
            while type(member_dtype) is clt.AnotherName:
                member_dtype = member_dtype.stru_AN_DT
            if member_dtype is None \
                    or issubclass(type(member_dtype), clt.TData) is False \
                    or member_dtype.obj_TD_size is None \
                    or member_dtype.obj_TD_size.i_size == -1:
                raise "member.stru_Var_TData is None"
            if member_dtype.obj_TD_size.i_size * self.__sum_arr_size(member.get_all_dim_size()) > t_i_max_size:
                t_i_max_size = member_dtype.obj_TD_size.i_size * self.__sum_arr_size(member.get_all_dim_size())
            if member_dtype.obj_TD_size.i_max_member_size > self.i_max_member_size:
                self.i_max_member_size = member_dtype.obj_TD_size.i_max_member_size
            pass
        return self.__min_N_greater(
            min(g_dev_evn.i_package_size, self.i_max_member_size),
            t_i_max_size)

    def __count_size_struct(self, _obj_dt):
        if _obj_dt is None or _obj_dt.tree_Com_members is None \
                or (_obj_dt.i_Com_Type != 1 and _obj_dt.i_Com_Type != 2):
            raise "self.obj_td_com is None or self.obj_td_com.tree_Com_members is None"
        if g_dev_evn is None or type(g_dev_evn) is not DevEnv:
            raise "tools.g_dev_evn is None or type(tools.g_dev_evn) is tools.DevEnv"
        t_i_pre_member_offset = 0
        # 长度计算
        for i in range(len(_obj_dt.tree_Com_members)):
            '''
            遍历成员列表
            '''
            member = _obj_dt.tree_Com_members[i]
            if type(member) not in (clt.Variable, clt.Function):
                raise "type(member) not in (clt.Variable, clt.Function)"
            if type(member) is clt.Function:
                continue
            member_dtype = member.stru_Var_TData
            while type(member_dtype) is clt.AnotherName:
                member_dtype = member_dtype.stru_AN_DT
            if member_dtype is None or ((issubclass(type(member_dtype),
                                                    clt.TData) is False or member_dtype.obj_TD_size is None
                                         or member_dtype.obj_TD_size.i_size == -1) and (
                                                issubclass(type(member_dtype), clt.Enum) is not True)):
                raise "member.stru_Var_TData is None"
            if issubclass(type(member_dtype), clt.Enum) is True:
                t_m_size = 4
                t_max_m_size = 4
                b_is_buildin = True
            else:
                t_m_size = member_dtype.obj_TD_size.i_size
                t_max_m_size = member_dtype.obj_TD_size.i_max_member_size
                b_is_buildin = len(member_dtype.obj_TD_size.dict_init_offset) == 0
            # 1.计算成员偏移量
            if i == 0:
                '''
                Nothing todo.
                '''
                if self.i_max_member_size < t_m_size:
                    self.i_max_member_size = t_m_size
                pass
            else:
                '''
                计算偏移量
                '''
                if b_is_buildin:
                    '''
                    计算内建对象起始偏移量
                    '''
                    t_i_pre_member_offset = self.__min_N_greater(
                        min(g_dev_evn.i_package_size, t_m_size),
                        t_i_pre_member_offset)
                    # 2.更新最大成员长度
                    if self.i_max_member_size < t_m_size:
                        self.i_max_member_size = t_m_size
                    pass
                else:
                    '''
                    计算复合对象的起始偏移量
                    '''
                    t_i_pre_member_offset = self.__min_N_greater(
                        min(g_dev_evn.i_package_size, t_max_m_size),
                        t_i_pre_member_offset)
                    # 2.更新最大成员长度
                    if self.i_max_member_size < t_max_m_size:
                        self.i_max_member_size = t_max_m_size
                    pass
                pass
            # 3.保存成员变量的起始偏移量
            self.dict_init_offset[member.sz_ELM_Name] = t_i_pre_member_offset
            # 4.跟新成员变量的结束偏移量
            t_i_pre_member_offset = t_i_pre_member_offset + t_m_size * self.__sum_arr_size(
                member.get_all_dim_size())
        return t_i_pre_member_offset

    def __min_N_greater(self, _x, _threshold):
        i_base = _x
        while i_base < _threshold:
            i_base = i_base + _x
        return i_base

    def __sum_arr_size(self, _arr_size):
        if type(_arr_size) is not list:
            raise "type(_arr_size) is not list"
        i_sum_arr_size = 1
        for it_dim in _arr_size:
            if type(it_dim) is not str or it_dim.isdigit() is False:
                raise "type(it_dim) is not str or it_dim.isdigit()"
            i_sum_arr_size = i_sum_arr_size * int(it_dim)
        return i_sum_arr_size


dict_buildin_type = {
    'bool': '((bool)(( )*))',
    'void': '((void)(( )*))',
    'p_void': '(((void)(( )*)\*)(( )*))',
    'pp_void': '((void)(( )*)(\*(( )*))\*(( )*))',
    # 'c_p_void': '(((void)(( )*)\*)(( )*))',
    # 'p_c_void': '((void)(( )*)(\*(( )*))\*(( )*))',

    # int & signed int
    'int': '(((signed(( )+))?(int)|((int)))(( )*))',
    'p_int': '((((signed(( )+))?(int))|((int)))((( )*)\*(( )*)))',
    'pp_int': '(((((signed(( )+))?(int))|((int))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned int
    'u_int': '(((unsigned(( )+))(int))(( )*))',
    'p_u_int': '(((unsigned(( )+))(int))(( )*)\*(( )*))',
    'pp_u_int': '(((unsigned(( )+))(int))((( )*)\*(( )*)\*)(( )*))',
    # const int & const signed int & signed int const
    'c_int': '((((const)(( )+)(signed(( )+))?(int))|((signed(( )+))?(int)(( )+)(const)))(( )*))',
    'p_c_int': '(((const)(( )+)(signed(( )+))?(int))|((signed(( )+))?(int)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_int': '((((const)(( )+)(signed(( )+))?(int))|((signed(( )+))?(int)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned int & unsigned int const
    'c_u_int': '((((const)(( )+)(unsigned(( )+))(int))|((unsigned(( )+))(int)(( )+)(const)))(( )*))',
    'p_c_u_int': '((((const)(( )+)(unsigned(( )+))(int))|((unsigned(( )+))(int)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_int': '((((const)(( )+)(unsigned(( )+))(int))|((unsigned(( )+))(int)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # short & signed short
    'short': '(((signed(( )+))?(short)|((short)))(( )*))',
    'p_short': '((((signed(( )+))?(short))|((short)))((( )*)\*(( )*)))',
    'pp_short': '(((((signed(( )+))?(short))|((short))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned short
    'u_short': '(((unsigned(( )+))(short))(( )*))',
    'p_u_short': '(((unsigned(( )+))(short))(( )*)\*(( )*))',
    'pp_u_short': '(((unsigned(( )+))(short))((( )*)\*(( )*)\*)(( )*))',
    # const short & const signed short & signed short const
    'c_short': '((((const)(( )+)(signed(( )+))?(short))|((signed(( )+))?(short)(( )+)(const)))(( )*))',
    'p_c_short': '(((const)(( )+)(signed(( )+))?(short))|((signed(( )+))?(short)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_short': '((((const)(( )+)(signed(( )+))?(short))|((signed(( )+))?(short)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned short & unsigned short const
    'c_u_short': '((((const)(( )+)(unsigned(( )+))(short))|((unsigned(( )+))(short)(( )+)(const)))(( )*))',
    'p_c_u_short': '((((const)(( )+)(unsigned(( )+))(short))|((unsigned(( )+))(short)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_short': '((((const)(( )+)(unsigned(( )+))(short))|((unsigned(( )+))(short)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # char & signed char
    'char': '(((signed(( )+))?(char)|((char)))(( )*))',
    'p_char': '((((signed(( )+))?(char))|((char)))((( )*)\*(( )*)))',
    'pp_char': '(((((signed(( )+))?(char))|((char))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned char
    'u_char': '(((unsigned(( )+))(char))(( )*))',
    'p_u_char': '(((unsigned(( )+))(char))(( )*)\*(( )*))',
    'pp_u_char': '(((unsigned(( )+))(char))((( )*)\*(( )*)\*)(( )*))',
    # const char & const signed char & signed char const
    'c_char': '((((const)(( )+)(signed(( )+))?(char))|((signed(( )+))?(char)(( )+)(const)))(( )*))',
    'p_c_char': '(((const)(( )+)(signed(( )+))?(char))|((signed(( )+))?(char)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_char': '((((const)(( )+)(signed(( )+))?(char))|((signed(( )+))?(char)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned char & unsigned char const
    'c_u_char': '((((const)(( )+)(unsigned(( )+))(char))|((unsigned(( )+))(char)(( )+)(const)))(( )*))',
    'p_c_u_char': '((((const)(( )+)(unsigned(( )+))(char))|((unsigned(( )+))(char)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_char': '((((const)(( )+)(unsigned(( )+))(char))|((unsigned(( )+))(char)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # long & signed long
    'long': '(((signed(( )+))?(long)|((long)))(( )*))',
    'p_long': '((((signed(( )+))?(long))|((long)))((( )*)\*(( )*)))',
    'pp_long': '(((((signed(( )+))?(long))|((long))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned long
    'u_long': '(((unsigned(( )+))(long))(( )*))',
    'p_u_long': '(((unsigned(( )+))(long))(( )*)\*(( )*))',
    'pp_u_long': '(((unsigned(( )+))(long))((( )*)\*(( )*)\*)(( )*))',
    # const long & const signed long & signed long const
    'c_long': '((((const)(( )+)(signed(( )+))?(long))|((signed(( )+))?(long)(( )+)(const)))(( )*))',
    'p_c_long': '(((const)(( )+)(signed(( )+))?(long))|((signed(( )+))?(long)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_long': '((((const)(( )+)(signed(( )+))?(long))|((signed(( )+))?(long)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned long & unsigned long const
    'c_u_long': '((((const)(( )+)(unsigned(( )+))(long))|((unsigned(( )+))(long)(( )+)(const)))(( )*))',
    'p_c_u_long': '((((const)(( )+)(unsigned(( )+))(long))|((unsigned(( )+))(long)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_long': '((((const)(( )+)(unsigned(( )+))(long))|((unsigned(( )+))(long)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # longlong & signed longlong
    'longlong': '(((signed(( )+))?(long( )+long)|((long( )+long)))(( )*))',
    'p_longlong': '((((signed(( )+))?(long( )+long))|((long( )+long)))((( )*)\*(( )*)))',
    'pp_longlong': '(((((signed(( )+))?(long( )+long))|((long( )+long))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned longlong
    'u_longlong': '(((unsigned(( )+))(long( )+long))(( )*))',
    'p_u_longlong': '(((unsigned(( )+))(long( )+long))(( )*)\*(( )*))',
    'pp_u_longlong': '(((unsigned(( )+))(long( )+long))((( )*)\*(( )*)\*)(( )*))',
    # const long long & long long const  & const signed long long & signed long long const
    'c_longlong': '((((const)(( )+)(signed(( )+))?(long( )+long))|((signed(( )+))?(long( )+long)(( )+)(const)))(( )*))',
    'p_c_longlong': '(((const)(( )+)(signed(( )+))?(long( )+long))|((signed(( )+))?(long( )+long)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_longlong': '((((const)(( )+)(signed(( )+))?(long( )+long))|((signed(( )+))?(long( )+long)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned long long & unsigned long long const
    'c_u_longlong': '((((const)(( )+)(unsigned(( )+))(long( )+long))|((unsigned(( )+))(long( )+long)(( )+)(const)))(( )*))',
    'p_c_u_longlong': '((((const)(( )+)(unsigned(( )+))(long( )+long))|((unsigned(( )+))(long( )+long)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_longlong': '((((const)(( )+)(unsigned(( )+))(long( )+long))|((unsigned(( )+))(long( )+long)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # __int64 & signed __int64
    'int64': '(((signed(( )+))?(__int64)|((__int64)))(( )*))',
    'p_int64': '((((signed(( )+))?(__int64))|((__int64)))((( )*)\*(( )*)))',
    'pp_int64': '(((((signed(( )+))?(__int64))|((__int64))))((( )*)\*(( )*)\*(( )*)))',
    # unsigned __int64
    'u_int64': '(((unsigned(( )+))(__int64))(( )*))',
    'p_u_int64': '(((unsigned(( )+))(__int64))(( )*)\*(( )*))',
    'pp_u_int64': '(((unsigned(( )+))(__int64))((( )*)\*(( )*)\*)(( )*))',
    # const __int64 & const signed __int64 & signed __int64 const
    'c_int64': '((((const)(( )+)(signed(( )+))?(__int64))|((signed(( )+))?(__int64)(( )+)(const)))(( )*))',
    'p_c_int64': '(((const)(( )+)(signed(( )+))?(__int64))|((signed(( )+))?(__int64)(( )+)(const)))((( )*)\*(( )*))',
    'pp_c_int64': '((((const)(( )+)(signed(( )+))?(__int64))|((signed(( )+))?(__int64)(( )+)(const)))((( )*)\*(( )*)\*(()*)))',
    # const unsigned __int64 & unsigned __int64 const
    'c_u_int64': '((((const)(( )+)(unsigned(( )+))(__int64))|((unsigned(( )+))(__int64)(( )+)(const)))(( )*))',
    'p_c_u_int64': '((((const)(( )+)(unsigned(( )+))(__int64))|((unsigned(( )+))(__int64)(( )+)(const)))((( )*)\*(( )*)))',
    'pp_c_u_int64': '((((const)(( )+)(unsigned(( )+))(__int64))|((unsigned(( )+))(__int64)(( )+)(const)))((( )*)\*(( )*)\*(( )*)))',

    # float
    'float': '((float)(( )*))',
    'p_float': '((float)(( )*)\*(( )*))',
    'pp_float': '((float)(( )*)(\*(( )*))\*)',
    # const float
    'c_float': '(((const)(( )+)(float)(( )*)))',
    'p_c_float': '((((const)(( )+)(float)(( )*)))\*)',
    'pp_c_float': '(((const)(( )+)(float)(( )*))(\*(( )*))\*)',
    # double
    'double': '((double)(( )*))',
    'p_double': '((double)(( )*)\*(( )*))',
    'pp_double': '((double)(( )*)(\*(( )*))\*)',
    # const double
    'c_double': '(((const)(( )+)(double)(( )*)))',
    'p_c_double': '((((const)(( )+)(double)(( )*)))\*)',
    'pp_c_double': '(((const)(( )+)(double)(( )*))(\*(( )*))\*)',
}
dict_buildin_size = {}
g_dev_evn = None


def get_buildin_size(_sz_type):
    if type(_sz_type) is not str or _sz_type not in dict_buildin_size.keys():
        raise "type(_sz_type) is not str or _sz_type not in dict_buildin_size.keys()"
    return dict_buildin_size[_sz_type]


class DevEnv:
    def __init__(self, _long_bit=32, _plate_form="win", _package_size=4):
        if _long_bit not in (32, 64):
            raise "_long_bit must in (32, 64):"
        if _plate_form not in ("win", "linux"):
            raise "_plate_form must in (\"win\", \"linux\"):"
        if _package_size not in (1, 4, 8):
            raise "_package_size must in (1, 4, 8):"
        self.i_long_bit = _long_bit
        self.sz_plateform = _plate_form
        self.i_package_size = _package_size
        pass


def set_dev_evn(_long_bit=32, _plate_form="win", _package_size=4):
    """
    设置平台环境参数，此函数必须在def_parser2模块加载前调用
    :param _long_bit: cpu架构(32, 64)
    :param _plate_form: 开发平台(“win”, "linux")
    :param _package_size: 内存对齐长度(1, 4, 8)
    :return:
    """
    global g_dev_evn
    g_dev_evn = DevEnv(_long_bit, _plate_form, _package_size)
    make_buildin_size()
    pass


def get_pointer_size():
    if g_dev_evn is None or type(g_dev_evn) is not DevEnv:
        raise g_dev_evn is None
    return (4 if (g_dev_evn.sz_plateform == "win" or (g_dev_evn.sz_plateform == "linux" and _dev_evn.i_long_bit == 32))
            else (8 if (g_dev_evn.sz_plateform == "linux" and g_dev_evn.i_long_bit == 64) else -1))


def make_buildin_size():
    """
    根据平台环境参数，构造c内建对象的长度
    :param _dev_evn:
    :return:
    """

    global dict_buildin_size
    global g_dev_evn

    if g_dev_evn is None or type(g_dev_evn) is not DevEnv:
        raise "type(_dev_evn) must be DevEnv"

    dict_buildin_size = {
        'bool': 1,
        'void': -1,
        'p_void': get_pointer_size(),
        'pp_void': get_pointer_size(),

        # int & signed int
        'int': 4,
        'p_int': get_pointer_size(),
        'pp_int': get_pointer_size(),
        # unsigned int
        'u_int': 4,
        'p_u_int': get_pointer_size(),
        'pp_u_int': get_pointer_size(),

        # const int & const signed int & signed int const
        'c_int': 4,
        'p_c_int': get_pointer_size(),
        'pp_c_int': get_pointer_size(),
        # const unsigned int & unsigned int const
        'c_u_int': 4,
        'p_c_u_int': get_pointer_size(),
        'pp_c_u_int': get_pointer_size(),

        # short & signed short
        'short': 2,
        'p_short': get_pointer_size(),
        'pp_short': get_pointer_size(),

        # unsigned short
        'u_short': 2,
        'p_u_short': get_pointer_size(),
        'pp_u_short': get_pointer_size(),

        # const short & const signed short & signed short const
        'c_short': 2,
        'p_c_short': get_pointer_size(),
        'pp_c_short': get_pointer_size(),
        # const unsigned short & unsigned short const
        'c_u_short': 2,
        'p_c_u_short': get_pointer_size(),
        'pp_c_u_short': get_pointer_size(),

        # char & signed char
        'char': 1,
        'p_char': get_pointer_size(),
        'pp_char': get_pointer_size(),

        # unsigned char
        'u_char': 1,
        'p_u_char': get_pointer_size(),
        'pp_u_char': get_pointer_size(),

        # const char & const signed char & signed char const
        'c_char': 1,
        'p_c_char': get_pointer_size(),
        'pp_c_char': get_pointer_size(),

        # const unsigned char & unsigned char const
        'c_u_char': 1,
        'p_c_u_char': get_pointer_size(),
        'pp_c_u_char': get_pointer_size(),

        # long & signed long
        'long': get_pointer_size(),
        'p_long': get_pointer_size(),
        'pp_long': get_pointer_size(),

        # unsigned long
        'u_long': get_pointer_size(),
        'p_u_long': get_pointer_size(),
        'pp_u_long': get_pointer_size(),

        # const long & const signed long & signed long const
        'c_long': get_pointer_size(),
        'p_c_long': get_pointer_size(),
        'pp_c_long': get_pointer_size(),

        # const unsigned long & unsigned long const
        'c_u_long': get_pointer_size(),
        'p_c_u_long': get_pointer_size(),
        'pp_c_u_long': get_pointer_size(),

        # longlong & signed longlong
        'longlong': 8,
        'p_longlong': get_pointer_size(),
        'pp_longlong': get_pointer_size(),
        # unsigned longlong
        'u_longlong': 8,
        'p_u_longlong': get_pointer_size(),
        'pp_u_longlong': get_pointer_size(),

        # const long long & long long const  & const signed long long & signed long long const
        'c_longlong': 8,
        'p_c_longlong': get_pointer_size(),
        'pp_c_longlong': get_pointer_size(),

        # const unsigned long long & unsigned long long const
        'c_u_longlong': 8,
        'p_c_u_longlong': get_pointer_size(),
        'pp_c_u_longlong': get_pointer_size(),

        # __int64 & signed __int64
        'int64': 8,
        'p_int64': get_pointer_size(),
        'pp_int64': get_pointer_size(),

        # unsigned __int64
        'u_int64': 8,
        'p_u_int64': get_pointer_size(),
        'pp_u_int64': get_pointer_size(),
        # const __int64 & const signed __int64 & signed __int64 const
        'c_int64': 8,
        'p_c_int64': get_pointer_size(),
        'pp_c_int64': get_pointer_size(),

        # const unsigned __int64 & unsigned __int64 const
        'c_u_int64': 8,
        'p_c_u_int64': get_pointer_size(),
        'pp_c_u_int64': get_pointer_size(),

        # float
        'float': 4,
        # const float
        'c_float': 4,
        'p_c_float': get_pointer_size(),
        'pp_c_float': get_pointer_size(),
        # double
        'double': 8,
        'p_double': get_pointer_size(),
        'pp_double': get_pointer_size(),
        # const double
        'c_double': 8,
        'p_c_double': get_pointer_size(),
        'pp_c_double': get_pointer_size(),
    }
    pass


import re

tuple_win_buildin_type = (
    "DWORD", "WORD", "USHORT", "SHORT", "LONG", "BYTE", "UINT", "LPVOID", "HANDLE", "LPDWORD", "UINT64", "INT64",
    "BOOL"
)


def isWinBuildinType(_szType):
    if type(_szType) is not str:
        raise "param _szType must str"
    for key in tuple_win_buildin_type:
        if re.match(key, _szType) is not None:
            return key
    return None


def isPointer(_szType):
    if type(_szType) is not str:
        raise "param _szType must str"
    _szType.strip()
    return _szType.count('*'), _szType.rstrip('*')


def makePointer(_obj_type, _pflag):
    '''
    根据参数构造指针类型
    :param _obj_type:
    :param _pflag: 几级指针，0表示非指针
    :return: DPointer of _obj_type
    '''
    if _pflag < 0:
        raise "_pflag must >= 0"
    obj_type = _obj_type
    for i in range(0, _pflag):
        t_type = clt.DPointer('P_' + obj_type.sz_ELM_Name, obj_type)
        obj_type = t_type
    if type(obj_type) is clt.DPointer:
        obj_type.obj_TD_size = TDSize()
        obj_type.obj_TD_size.count_size(obj_type)
    return obj_type


def parserType(_szType):
    '''
    解析修饰类型的关键字const, extern, static, register, 指针* 等
    :param _szType:
    :return:
    '''
    if type(_szType) is not str:
        raise "param _szType must str"
    out_type = {'type': '', 'const': 0, 'extern': 0, 'static': 0, 'register': 0, 'compound': '', 'pflag': 0}
    l_type = _szType.split(' ')
    l_type = [x.strip() for x in l_type if x != '']
    for it in l_type:
        pflag = it.count('*')
        out_type['pflag'] = out_type['pflag'] + pflag
        it = it.strip('*')
        if it == '':
            continue
        if it == "const":
            out_type['const'] = 1
        elif it == "extern":
            out_type['extern'] = 1
        elif it == "static":
            out_type['static'] = 1
        elif it == "register":
            out_type['register'] = 1
        elif it == "class":
            out_type['compound'] = 'class'
        elif it == "struct":
            out_type['compound'] = 'struct'
        elif it == "union":
            out_type['compound'] = 'union'
        else:
            out_type['type'] = it
    return out_type


def isBuildinType(_szType):
    if type(_szType) is not str:
        raise "param _szType must str"
    for key in dict_buildin_type.keys():
        if re.fullmatch(dict_buildin_type[key], _szType.strip()) is not None:
            return key
    return None


def isEnumType(_szType):
    if type(_szType) is not str:
        raise "param _szType must str"
    if re.fullmatch("(enum( )+([a-zA-Z_0-9]+))( )*", _szType) is not None:
        sz_enum_name = _szType[re.match("(enum(( )+))", _szType).span()[1]:]
        return sz_enum_name
    return None


def isPFunType(_szType):
    if type(_szType) is not str:
        raise "param _szType must str"
    if re.search("\((( )*)CALLBACK(( )*)\\*(( )*)", _szType) is not None:
        return "_"
    return None
