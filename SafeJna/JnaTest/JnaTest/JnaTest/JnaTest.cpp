// JnaTest.cpp : 定义 DLL 应用程序的导出函数。
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


// 这是导出函数的一个示例。
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