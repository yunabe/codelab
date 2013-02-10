/**
 * Trace.aj
 */
aspect HelloWorldTracing {
  pointcut atSayHello(): call(void HelloWorld.sayHello());

 before(): atSayHello() {
    System.out.println("[[Before sayHello]]");
  }
 after(): atSayHello() {
    System.out.println("[[After sayHello]]");
  }

  pointcut atCreateMessage(String message):
    call(String HelloWorld.createMessage(String)) && args(message);

  String around(String message): atCreateMessage(message) {
    return "New hello '" + message + "'!?";
  }
}
