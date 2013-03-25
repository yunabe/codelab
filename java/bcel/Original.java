
public class Original {

  public static int sum(int x, int y) {
    return x + y;
  }

  public static int fact(int n) {
    return n > 0 ? n * fact(n - 1) : 1;
  }

  static int get10() {
    return 10;
  }

  private static void voidFunc() {
  }

  public static Integer refArgReturn(Integer i) {
    return i * 2;
  }

  public static int[] arrayArgReturn(int[] array) {
    int[] doubled = new int[array.length];
    for (int i = 0; i < array.length; i++) {
      doubled[i] = array[i] * 2;
    }
    return doubled;
  }

  public String sayHello(String name) {
    return "Hello " + name + "!";
  }

  public static void main(String[] args) {
    System.out.println("sum  == " + sum(2, 3));
    System.out.println("fact  == " + fact(3));
    System.out.println("get10 == " + get10());
    voidFunc();
    System.out.println("refArgReturn == " + refArgReturn(10));
    System.out.println("arrayArgReturn == " +
                       arrayArgReturn(new int[]{1, 2, 3}));

    System.out.println("===========================");
    Original original = new Original();
    original.sayHello("original");
    System.out.println("+++++++++++++++++++++++++++");
  }
}
