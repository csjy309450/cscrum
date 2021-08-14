package SafeJna;

import SafeJna.InterTest.SafeJnaUtil;
import com.sun.jna.Native;

import java.io.File;
import java.io.FileFilter;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.HashSet;
import java.util.Set;
import java.util.Stack;

public class SafeJnaDaemon {
  /**
   * 加载指定类路径下指定文件名
   *
   * @param classPath
   */
  public static Class<?> loadClassByName(String classPath, String fullClassName)
          throws NoSuchMethodException, MalformedURLException {
    // 设置class文件所在根路径
    // 例如/usr/java/classes下有一个test.App类，则/usr/java/classes即这个类的根路径，
    // 而.class文件的实际位置是/usr/java/classes/test/App.class
    File clazzPath = new File(classPath);

    if (clazzPath.exists() && clazzPath.isFile()) {
      // 获取路径长度
      int clazzPathLen = clazzPath.getAbsolutePath().length() + 1;
      Method method = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
      boolean accessible = method.isAccessible();
      try {
        if (!accessible) {
          method.setAccessible(true);
        }
        // 设置类加载器
        URLClassLoader classLoader = (URLClassLoader) ClassLoader.getSystemClassLoader();
        // 将当前类路径加入到类加载器中
        method.invoke(classLoader, clazzPath.toURI().toURL());
      } catch (IllegalAccessException e) {
        e.printStackTrace();
      } catch (InvocationTargetException e) {
        e.printStackTrace();
      } finally {
        method.setAccessible(accessible);
      }
      // 加载Class类
      try {
        Class cls = Class.forName(fullClassName);
        return cls;
      } catch (ClassNotFoundException e) {
        System.out.println("ClassNotFoundException {}" + e);
      }
    }
    return null;
  }

  public static Object invokeMethod(Object newObj, String methodName, Object[] args)throws Exception {
    Class ownerClass = newObj.getClass();
    Class[] argsClass = new Class[args.length];
    for (int i = 0, j = args.length; i < j; i++) {
      argsClass[i] = args[i].getClass();
    }
    Method method = ownerClass.getMethod(methodName, argsClass);
    return method.invoke(newObj, args);

  }

  public static void main(String[] args) {
    try {
      Class cls = SafeJnaDaemon.loadClassByName("E:/VMware/YZ/github/SafeJna/target/classes/SafeJna/InterTest/SafeJnaUtil.class", "SafeJna.InterTest.SafeJnaUtil");
      System.out.println(cls.getName());
      Object lib = Native.loadLibrary(
              "E:\\VMware\\YZ\\github\\SafeJna\\JnaTest\\JnaTest\\x64\\Debug\\JnaTest.dll"
              , cls);
      Object ret = SafeJnaDaemon.invokeMethod(lib, "fnJnaTest1", new Object[]{2024});
      System.out.print(ret);
    } catch (Throwable e) {
      System.out.print(e.getCause());
    }
  }
}
