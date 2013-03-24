
public class Hook {

  public interface Runner {
    Object run(Object[] args);
  }

  static Object hook(String name, Runner runner, Object[] args) {
    System.out.println("hook: name == " + name);
    return runner.run(args);
  }
}
