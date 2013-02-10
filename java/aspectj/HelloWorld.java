
class MyLib {
  String createMessage(String name) {
    return "Hello '" + name + "'!";
  }
}

public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("start main.");
    new HelloWorld().sayHello();
    System.out.println("end main.");
  }

  void sayHello() {
    MyLib mylib = new MyLib();
    System.out.println(mylib.createMessage("world"));
  }
}
