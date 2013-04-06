import org.python.util.PythonInterpreter;

import java.util.Properties;

public class JavaWrapperOverhead {

  public static class Calc {
    public int square(int n) {
      return n * n;
    }
  }
  
  public static void main(String[] args) {
    Properties properties = new Properties();
    properties.setProperty("python.cachedir.skip", "true");
    properties.setProperty("python.home", "jython-src");

    PythonInterpreter.initialize(System.getProperties(),
                                 properties,
                                 new String[]{});
    PythonInterpreter inter = new PythonInterpreter();
    inter.exec("import java_wrapper_overhead");
    long start, end;
    start = System.currentTimeMillis();
    inter.exec("java_wrapper_overhead.UseInherits()");
    end = System.currentTimeMillis();
    System.out.println("time: " + (end - start) + "[ms]");
    start = System.currentTimeMillis();
    inter.exec("java_wrapper_overhead.NoInherits()");
    end = System.currentTimeMillis();
    System.out.println("time: " + (end - start) + "[ms]");
    start = System.currentTimeMillis();
    inter.exec("java_wrapper_overhead.Proxy()");
    end = System.currentTimeMillis();
    System.out.println("time: " + (end - start) + "[ms]");
  }
}
