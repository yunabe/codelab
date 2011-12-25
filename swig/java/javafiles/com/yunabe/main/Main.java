package com.yunabe.main;

import com.yunabe.BasicModule;
import com.yunabe.Lib;
import com.yunabe.MyClass;

public class Main {
  public static void main(String[] args) {
    System.loadLibrary("BasicModule");
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
  }
}
