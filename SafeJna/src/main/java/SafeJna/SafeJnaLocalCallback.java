package SafeJna;

import com.sun.jna.Callback;

import java.lang.reflect.Method;

public interface SafeJnaLocalCallback {
  public abstract Object invoke(Object [] args) throws Throwable;
}
