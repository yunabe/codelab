public class FooModule implements Module {
  public void doSomething() {
    System.out.println("FooModule: doSomething!");
  }

  public void registerToGlobalManager() {
    ModuleManager.getInstance().addModule(this);
  }
}
