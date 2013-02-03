
public class HelloWorld {
    
  public static void main(String[] args) {
    System.out.println("start main.");
    new HelloWorld().sayHello("world!");
    System.out.println("end main.");
  }

  void sayHello(String name) {
    System.out.println("Hello " + name);
  }
}

