// ���� ifdef ���Ǵ���ʹ�� DLL �������򵥵�
// ��ı�׼�������� DLL �е������ļ��������������϶���� JNATEST_EXPORTS
// ���ű���ġ���ʹ�ô� DLL ��
// �κ�������Ŀ�ϲ�Ӧ����˷��š�������Դ�ļ��а������ļ����κ�������Ŀ���Ὣ
// JNATEST_API ������Ϊ�Ǵ� DLL ����ģ����� DLL ���ô˺궨���
// ������Ϊ�Ǳ������ġ�
#ifdef JNATEST_EXPORTS
#define JNATEST_API extern "C" __declspec(dllexport)
#else
#define JNATEST_API extern "C" __declspec(dllimport)
#endif

typedef void(*MyCallBack)(int);

JNATEST_API int fnJnaTest1(int x);

JNATEST_API int fnJnaTest2(MyCallBack cb);
