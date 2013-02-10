import org.aspectj.lang.Signature;

aspect HelloWorldTracing {
  pointcut atSayHello(): call(void HelloWorld.sayHello());

 before(): atSayHello() {
    System.out.println("[[Before sayHello]]");
  }
 after(): atSayHello() {
    System.out.println("[[After sayHello]]");
  }

  pointcut atCreateMessage(String message):
      call(String MyLib.createMessage(String)) && args(message);

  String around(String message): atCreateMessage(message) {
    Signature sig = thisJoinPoint.getSignature();
    System.out.println(">> Sig == " + sig);
    
    // kind changes with 'call' and 'execution'.
    // this is a caller object, target is a callee object.
    System.out.println(">> Kind == " + thisJoinPoint.getKind()
        + ", This == " + thisJoinPoint.getThis()
        + ", Target == " + thisJoinPoint.getTarget()
        + ", args.len == " + thisJoinPoint.getArgs().length);
    return "New hello '" + message + "'!?";
  }
}
