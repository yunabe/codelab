
public class Hook {

  public interface Runner {
    Object run(Object[] args);
  }

  static private String join(String sep, Object[] args) {
    StringBuilder builder = new StringBuilder();
    for (int i = 0; i < args.length; i++) {
      if (i != 0) {
        builder.append(sep);
      }
      builder.append(args[i].toString());
    }
    return builder.toString();
  }

  static Object hook(String name, Runner runner, Object[] args) {
    Object returnVal = runner.run(args);
    System.out.println(name + ": args == [" + join(", ", args) +
                       "], : return: [" + returnVal + "]");
    return returnVal;
  }
}
