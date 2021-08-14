package SafeJna;

import com.sun.jna.Library;

import java.lang.reflect.Proxy;
import java.util.Collections;
import java.util.Map;

public class SafeJnaNative {
  public static <T> T loadLibrary(String name, Class<T> interfaceClass) {
    return loadLibrary(name, interfaceClass, Collections.emptyMap());
  }
  public static <T> T loadLibrary(String name, Class<T> interfaceClass, Map<?, ?> options) {
    SafeJnaLibrary.Handler handler = new SafeJnaLibrary.Handler(name, interfaceClass, options);
    ClassLoader loader = interfaceClass.getClassLoader();
    Object proxy = Proxy.newProxyInstance(loader, new Class[]{interfaceClass}, handler);
    return interfaceClass.cast(proxy);
  }
}
