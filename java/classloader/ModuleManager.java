import java.lang.ClassLoader;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

public class ModuleManager {
  private ArrayList<Module> modules;

  private ModuleManager() {
    this.modules = new ArrayList<Module>();
  }

  public void addModule(Module module) {
    modules.add(module);
  }

  public void invokeDoSomething() {
    for (Module module : modules) {
      module.doSomething();
    }
  }

  private static final ModuleManager globalInstance = new ModuleManager();

  public static ModuleManager getInstance() {
    return globalInstance;
  }
}
