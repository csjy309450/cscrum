package SafeJna;

import java.util.HashMap;
import java.util.Map;

public class SafeJnaRemoteInvoke {
  private static Map<String, SafeJnaLocalCallback> s_callbackMap = new HashMap<String, SafeJnaLocalCallback>();
  public static void bindCallback(String remoteCb, SafeJnaLocalCallback localCb) {
    s_callbackMap.put(remoteCb, localCb);
  }

  private String m_clsName;
  public SafeJnaRemoteInvoke(String clsName) {
    this.m_clsName = clsName;
  }
  public Object invoke(Object[] inArgs) throws Throwable {
    System.out.println("RemoteInvoke in");
    return null;
  }
}
