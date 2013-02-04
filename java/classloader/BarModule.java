public class BarModule implements Module {
  public void doSomething() {
    System.out.println("BarModule: doSomething!");
  }

  public void registerToGlobalManager() {
    ModuleManager.getInstance().addModule(this);
  }
}
