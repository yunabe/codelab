package jp.yunabe;

import java.util.Set;
import javax.inject.Inject;

import dagger.Component;
import dagger.Module;
import dagger.Provides;

/**
 * Hello world!
 */
public class App {
  public static void main( String[] args ) {
    ClassA a = DaggerMyComponent.create().getClassA();
    System.out.println(a.b.c);
    System.out.println(a.items.size());
  }
}

class ClassA {
  ClassB b;
  MyInterface i;
  Set<MyItem> items;

  @Inject
  ClassA(ClassB b, MyInterface i, Set<MyItem> items) {
    this.b = b;
    this.i = i;
    this.items = items;
  }
}

class ClassB {
  @Inject
  ClassC c;

  @Inject
  ClassB() {
  }
}

class ClassC {
  @Inject
  ClassC() {
  }
}

interface MyInterface {
}

class MyInterfaceImpl implements MyInterface {
}

interface MyItem {
}

@Module
class MyModule {
  // For interface and abstract class, you can not use @Inject. Use @Provides.
  @Provides
  MyInterface createMyService() {
    return new MyInterfaceImpl();
  }

  @Provides(type=Provides.Type.SET)
  MyItem createItem() {
    return new MyItem() {
    };
  }
}

@Component(modules = MyModule.class)
interface MyComponent {
  ClassA getClassA();
}
