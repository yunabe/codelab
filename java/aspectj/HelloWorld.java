
public class HelloWorld {
    
  public static void main(String[] args) {
    System.out.println("start main.");
    new HelloWorld().sayHello();
    System.out.println("end main.");
  }

  void sayHello() {
    System.out.println(createMessage("world"));
  }

  String createMessage(String name) {
    return "Hello '" + name + "'!";
  }
}
