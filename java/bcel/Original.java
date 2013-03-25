
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

  public static void main(String[] args) {
    System.out.println("sum  == " + sum(2, 3));
    System.out.println("fact  == " + fact(3));
    System.out.println("get10 == " + get10());
    voidFunc();
  }
}
