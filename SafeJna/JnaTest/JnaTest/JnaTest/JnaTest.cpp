// JnaTest.cpp : ���� DLL Ӧ�ó���ĵ���������
//

#include "stdafx.h"
#include <stdio.h>
#include "JnaTest.h"

DWORD WINAPI Fun(LPVOID lpParamter)
{
    MyCallBack pcb = (MyCallBack)lpParamter;
    for (int i = 0; i < 10; i++) {
        ::Sleep(5000);
        pcb(1);
    }
    return 0L;
}


// ���ǵ���������һ��ʾ����
JNATEST_API int fnJnaTest1(int x)
{
    printf("fnJnaTest1 %d\n", x);
	return 42;
}

JNATEST_API int fnJnaTest2(MyCallBack cb)
{
    HANDLE hThread = CreateThread(NULL, 0, Fun, cb, 0, NULL);
    return 0;
}