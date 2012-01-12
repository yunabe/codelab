package com.yunabe.main;

import com.yunabe.BasicModule;
import com.yunabe.DirectorRoot;
import com.yunabe.Lib;
import com.yunabe.MyClass;
import com.yunabe.NoDirectorRoot;

class Child0 extends DirectorRoot {
  @Override
  public void PrintName() {
    System.out.println("I'm Child0.");
  }
}

public class Main {
  public static void main(String[] args) {
    System.loadLibrary("BasicModule");
    System.loadLibrary("DirectorModule");
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
  }
}
