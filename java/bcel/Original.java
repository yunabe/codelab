
public class Original {

  public static int sum(int x, int y) {
    return x + y;
  }

  public static int fact(int n) {
    return n > 0 ? n * fact(n - 1) : 1;
  }

  public static void main(String[] args) {
    System.out.println("sum == " + sum(2, 3));
    System.out.println("sum == " + fact(3));
  }
}
