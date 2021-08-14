package SafeJna.InterTest;

import SafeJna.SafeJnaLocalCallback;
import SafeJna.SafeJnaRemoteInvoke;
import com.sun.jna.Native;

/**
 * Hello world!
 *
 */
public class InterTestApp {

  public static class MySafeJnaLocalCallback implements SafeJnaLocalCallback {
    @Override
    public Object invoke(Object [] args) throws Throwable {
      return null;
    }
  }

  public static class MyThread0 extends Thread
  {
    @Override
    public void run()
    {
      SafeJnaUtil INSTANCE = Native.loadLibrary(
              "E:\\VMware\\YZ\\github\\SafeJna\\JnaTest\\JnaTest\\x64\\Debug\\JnaTest.dll"
              , SafeJnaUtil.class);
      int ret = INSTANCE.fnJnaTest1(1);
      SafeJnaRemoteInvoke.bindCallback(SafeJnaUtil.MyCallBack.class.getName(), new MySafeJnaLocalCallback());
      int ret2 = INSTANCE.fnJnaTest2(new SafeJnaUtil.MyCallBack());
      try {
        Thread.sleep(100000);
      } catch (Throwable a) {

      } finally {

      }
    }
  }

  public static void main(String[] args) {
    MyThread0 mythread=new MyThread0();
    mythread.start();

//    SafeJnaUtil INSTANCE2 = SafeJnaNative.loadLibrary(
//            "E:\\VMware\\YZ\\github\\SafeJna\\JnaTest\\JnaTest\\x64\\Debug\\JnaTest.dll"
//            , SafeJnaUtil.class);
//    String strSafeJnaUtil = SafeJnaUtil.class.getSimpleName() + ".class";
//    URL fileURL=SafeJnaUtil.class.getResource(strSafeJnaUtil);
//    INSTANCE2.fnJnaTest1(1);
//    System.out.println("Hello World!");
  }
}
