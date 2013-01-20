import java.lang.reflect.Method;

import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

class Foo {
  public void doSomething() {
    System.out.println("doSomething is called.");
  }
}

class MyMethodIntercepter implements MethodInterceptor {
  public Object intercept(Object obj, Method method,
                          Object[] args, MethodProxy proxy) throws Throwable {
    System.out.printf("Hook: %s\n", method.getName());
    return proxy.invokeSuper(obj, args);
  }
}

public class Main {
  public static void main(String[] args) {
    Enhancer enhancer = new Enhancer();
    enhancer.setSuperclass(Foo.class);
    enhancer.setCallback(new MyMethodIntercepter());

    Foo foo = (Foo)enhancer.create();
    foo.doSomething();
  }
}
