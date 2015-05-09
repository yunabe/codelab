package jp.yunabe;

import javax.inject.Inject;

import dagger.Component;
import dagger.Module;
import dagger.Provides;

/**
 * Hello world!
 */
public class App {
  public static void main( String[] args ) {
    MyComponent component = DaggerMyComponent.create();
    Client client = component.getClient();
    client.sayHello();
  }
}

class Client {
  private Service service;

  @Inject
  Client(Service service) {
    this.service = service;
  }

  public void sayHello() {
    System.out.println("Invoke service.sayHello.");
    service.sayHello();
  }
}

interface Service {
  public void sayHello();
}

class MyServiceImpl implements Service {
  public void sayHello() {
    System.out.println("Hello MyServiceImpl!");
  }
}

@Module
class MyModule {
  @Provides
  Service createRealService() {
    return new MyServiceImpl();
  }
}

@Component(modules = MyModule.class)
interface MyComponent {
  Client getClient();
}
