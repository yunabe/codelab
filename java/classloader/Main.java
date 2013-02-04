import java.lang.ClassLoader;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

class Main {
  public static void main(String[] args) {
    try {
      System.out.println("-- main --");
      URLClassLoader fooLoader = new URLClassLoader(new URL[] {
          new URL("file:foo/")});
      System.out.println(fooLoader.loadClass("Module"));
      Module foo = (Module)fooLoader.loadClass("FooModule").newInstance();
      foo.registerToGlobalManager();
      URLClassLoader barLoader = new URLClassLoader(new URL[] {
          new URL("file:bar/")});
      Module bar = (Module)barLoader.loadClass("BarModule").newInstance();
      bar.registerToGlobalManager();

      System.out.println("-- invokeDoSomething --");
      ModuleManager.getInstance().invokeDoSomething();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
