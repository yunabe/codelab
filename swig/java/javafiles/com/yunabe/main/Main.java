package com.yunabe.main;

import com.yunabe.BasicModule;
import com.yunabe.DirectorRoot;
import com.yunabe.IncludeAndImportModule;
import com.yunabe.Lib;
import com.yunabe.MyClass;
import com.yunabe.NoDirectorRoot;

import com.yunabe.TimeModule;
import com.yunabe.Subtractor;
import com.yunabe.time.Time;

import com.yunabe.Manager;
import com.yunabe.Runner;

class Child0 extends DirectorRoot {
  @Override
  public void PrintName() {
    System.out.println("I'm Child0.");
  }
}

class JavaSubtractor extends Subtractor {
  @Override
  public Time subtract(Time x, Time y) {
    System.out.printf("Java: subtract '%s' from '%s'\n", y, x);
    return new Time(x.hour() - y.hour(),
                    x.minute() - y.minute(),
                    x.second() - y.second());
  }
}

class MyRunner extends Runner {
  private final Manager manager;
  private final byte[] dummyData;
  MyRunner(Manager manager) {
    this.manager = manager;
    this.dummyData = new byte[10 * 1000 * 1000];
  }
  
  public void run() {
    System.out.println("Myrunner.run()");
  }
}

public class Main {
  public static void main(String[] args) {
    System.loadLibrary("BasicModule");
    System.loadLibrary("DirectorModule");
    System.loadLibrary("TimeModule");
    int x = 3;
    int y = 4;
    System.out.printf("BasicModule.int_sum(%d, %d) == %d\n", x, y, BasicModule.int_sum(x, y));
    System.out.printf("Lib.int_mul(%d, %d) == %d\n", x, y, Lib.int_mul(x, y));
    System.out.printf("BasicModule.get_hello() == %s\n", BasicModule.get_hello());

    int[] list = new int[1];
    list[0] = 9;
    BasicModule.dbl(list);
    System.out.printf("list[0] == %d\n", list[0]);

    MyClass myclass = new MyClass(34);
    System.out.printf("myclass.getX() == %d\n", myclass.getX());

    System.out.println("--------- Import and Include ------------");
    myclass = IncludeAndImportModule.createMyClass(897);
    System.out.printf("myclass.getX() == %d\n", myclass.getX());

    System.out.println("--------- Director ------------");

    DirectorRoot director = new DirectorRoot() {
        @Override
        public void PrintName() {
          System.out.println("I'm a child of DirectorRoot in Java!");
        }
      };
    // Overrided Java code are executed.
    director.PrintName();
    // Overrided Java code are executed from C++
    // because it is declared as "director" in swig.
    DirectorRoot.CallPrintName(director);

    NoDirectorRoot nodirector = new NoDirectorRoot() {
        @Override
        public void PrintName() {
          System.out.println("I'm a child of NoDirectorRoot in Java!");
        }
      };
    // Overrided Java code are executed.
    nodirector.PrintName();
    // Unfortunately, C++ codes of base class is called here.
    NoDirectorRoot.CallPrintName(nodirector);

    System.out.println("--------- Typemap ------------");
    Time t0 = new Time(1, 20, 30);
    Time t1 = new Time(2, 40, 30);
    System.out.println(TimeModule.sumTimeAsValue(t0, t1));

    System.out.println("--- typemap & director ---");
    JavaSubtractor subtractor = new JavaSubtractor();
    // Release an ownership of object from Java.
    // If you don't call this, the registered subtractor will be destroyed
    // by Java GC and calling TimeModule.subtractTime might cause segv.
    //
    // Also, please note that adding %delobject to registerSubtractor in
    // SWIG file does not solve this ownership issue.
    subtractor.swigReleaseOwnership();
    TimeModule.registerSubtractor(subtractor);
    System.out.printf("Java: The result is %s\n",
                      TimeModule.subtractTime(t1, t0));

    /////// Memory Leak /////////
    for (int i = 0; i < 30; ++i) {
      Manager manager = new Manager();
      manager.set_runner(new MyRunner(null));
      // manager.set_runner(new MyRunner(manager));  // <- memory leak
    }
  }
}
