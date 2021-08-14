#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

import re
import io


class ComStructure:
    """
    复合对象结构，表征一个复合数据对象的结构
    self.sz_head: 复合数据对象的头，可能是("struct", "union", $COM-NAME)
    self.arr_member: 复合数据对象成员列表，元素类型为 ComMember
    self.arr_typedef: 重命名列表
    """

    def __init__(self):
        self.sz_head = ""
        self.arr_member = []
        self.arr_typedef = []

    def is_contain_inline_member(self):
        for it in self.arr_member:
            if it.is_inline() is True:
                return True
        return False


class ComMember:
    """
    复合对象结构，表征一个复合数据对象的结构
    self.sz_head: 当成员为内联复合类型，为复合数据对象的头，可能是("struct", "union", $COM-NAME)
    self.sz_name: 成员名
    self.i_size: 数组维度
    self.obj_type: 若成员为内联复合类型，保存类型结构
    """

    def __init__(self):
        self.sz_head = ""
        self.sz_name = ""
        self.i_size = []
        self.obj_type = []

    def is_inline(self):
        if len(self.obj_type) == 0:
            return False
        return True

    def is_anonymous(self):
        if self.sz_head == "union" \
                or self.sz_head == "struct" \
                or self.sz_head == "class":
            return True
        return False


class MemberParser:
    """
    成员对象解析器
    """

    def __init__(self, _line, _f):
        """
        构造函数
        :param _line:一行字符
        :param _f:打开的文件对象
        """
        if (type(_line) is not str) \
                and (type(_f) is not io.TextIOWrapper):
            raise "param error"
        self.sz_line = _line
        self.f = _f

    def parser(self):
        """
        解析成员
        :return: ComMember对象
        """
        obj_member = ComMember()
        if self.sz_line == '':
            return None
        if self.sz_line[-2] == ';':
            '''
            简单成员变量处理
            '''
            # obj_member.sz_name = self.sz_line[0:-2]
            self.__process_member_name(obj_member, self.sz_line)
            # obj_regx = re.search("\[.*\]", self.sz_line)
            # if obj_regx is None:
            #     obj_member.sz_name = self.sz_line[0:-2]
            # else:
            #     obj_member.sz_name = self.sz_line[0:obj_regx.span()[0]]
            #     obj_member.i_size = (self.sz_line[obj_regx.span()[0]:obj_regx.span()[1]])[1:-1]
            #     pass
            # pass
        else:
            '''
            内联复合成员变量处理
            当存在匿名复合成员时，进入此分支处理
            '''
            obj_member.sz_head = self.sz_line[0:-1].strip('\t')
            i_retract = self.sz_line.count('\t')
            sz_line = self.f.readline()
            while i_retract != sz_line.count('\t'):
                member_parser = MemberParser(sz_line, self.f)
                obj_member.obj_type.append(member_parser.parser())
                sz_line = self.f.readline()
                if sz_line == '':
                    break
            if sz_line[-2] == ';':
                # obj_member.sz_name = sz_line[0:-2]
                self.__process_member_name(obj_member, sz_line)
                # obj_regx = re.search("\[.*\]", sz_line)
                # if obj_regx is None:
                #     obj_member.sz_name = sz_line[0:-2]
                # else:
                #     obj_member.sz_name = sz_line[0:obj_regx.span()[0]]
                #     obj_member.i_size = (sz_line[obj_regx.span()[0]:obj_regx.span()[1]])[1:-1]
                #     pass
                # pass
            else:
                raise "sz_line[-2] must ';'"
        return obj_member

    def __process_member_name(self, _obj_member, _sz_line):
        """
        处理成员变量命
        :param _obj_member: 成员对象实例
        :param _sz_line: 一行字符即成员名
        :return:
        """
        obj_regx = re.search("\[([0-9a-zA-Z_\+\-\*\/ ]*)\]", _sz_line)
        if obj_regx is None:
            _obj_member.sz_name = _sz_line[0:-2].strip('\t')
        else:
            _obj_member.sz_name = _sz_line[0:obj_regx.span()[0]].strip('\t')
            _obj_member.i_size = re.findall("\[([0-9a-zA-Z_\+\-\*\/ ]*)\]", _sz_line)
            pass
        pass


class OutlineParser:
    """
    结构文件解析器
    """

    def __init__(self, _file):
        if type(_file) is not str:
            raise "_file type must str"
        self.f = None
        try:
            self.f = open(_file, "r")
        except FileNotFoundError as e:
            raise "Where is your outline file?"

        if self.f is not None:
            pass
        self.b_retain = False
        self.sz_line = ""
        pass

    def __del__(self):
        if type(self.f) is io.TextIOWrapper:
            self.f.close()

    def __parser_an_item(self):
        """
        从结构文件中解析一个复合对象
        :return: ComStructure对象
        """
        if self.f is None:
            return
        b_begin = False
        sz_line = ""
        while 1:
            if self.b_retain is False:
                self.sz_line = self.f.readline()
                if self.sz_line == '':
                    return None
            self.b_retain = False
            i_retract = self.sz_line.count('\t')
            if i_retract == 0 and b_begin is False:
                b_begin = True
                self.obj_com = ComStructure()
                self.obj_com.sz_head = self.sz_line[0:-1].strip('\t')
                continue
            if i_retract == 0 and b_begin is True:
                b_begin = False
                if self.sz_line[-2] == ';':
                    self.obj_com.arr_typedef = self.sz_line[0:-2].split(',')
                else:
                    self.b_retain = True
                    pass
                break
            if i_retract >= 1:
                member_parser = MemberParser(self.sz_line, self.f)
                self.obj_com.arr_member.append(member_parser.parser())
        return self.obj_com

    def find_by_name(self, _name):
        """
        通过名字查询复合对象
        :param _name:
        :return: ComStructure对象
        """

        def match_name(_name, _obj_com):
            if _obj_com.sz_head == _name:
                return True
            if len(_obj_com.arr_typedef) == 0:
                pass
            else:
                for it in _obj_com.arr_typedef:
                    sz_name = it.replace(' ', '')
                    obj_regx = re.findall("\*+", sz_name)
                    if len(obj_regx) == 1:
                        '''
                        指针类型别名
                        '''
                        sz_name = sz_name.lstrip('*')
                        if sz_name == _name:
                            return True
                    elif len(obj_regx) == 0:
                        '''
                        类型别名
                        '''
                        if sz_name == _name:
                            return True
            return False

        if self.f is None:
            return None
        while 1:
            obj_com = self.__parser_an_item()
            if obj_com is None:
                break
            if match_name(_name, obj_com):
                return obj_com
            pass
        return None


def get_outline_by_name(_file_path, _name):
    obj_ol = OutlineParser(_file_path)
    an_com = obj_ol.find_by_name(_name)
    return an_com


if __name__ is "__main__":
    a = OutlineParser("D:\\3_test_program\\HCStructModel\\XmlModel\\mode\\outline\\test.outline")
    an_obj = a.find_by_name("NET_DVR_PTZPOS")
    pass
