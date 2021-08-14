package SafeJna.InterTest;

import SafeJna.SafeJnaLibrary;
import SafeJna.SafeJnaRemoteInvoke;
import com.sun.jna.Callback;
import com.sun.jna.Library;

public interface SafeJnaUtil extends Library, SafeJnaLibrary {

  public class MyCallBack implements Callback {
    public int invoke(int a) {
      SafeJnaRemoteInvoke rinv = new SafeJnaRemoteInvoke(MyCallBack.class.getName());
      Object ret = null;
      try {
        ret = rinv.invoke(new Object[]{a});
      } catch (Throwable e) {

      }
      return 0;
    }
  }

  // dll interface
  int fnJnaTest1(Integer x);
  int fnJnaTest2(MyCallBack cb);
}
