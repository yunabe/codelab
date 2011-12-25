package com.yunabe.main;

import com.yunabe.BasicModule;
import com.yunabe.Lib;

public class Main {
  public static void main(String[] args) {
    System.loadLibrary("BasicModule");
    int x = 3;
    int y = 4;
    System.out.printf("BasicModule.int_sum(%d, %d) == %d\n", x, y, BasicModule.int_sum(x, y));
    System.out.printf("Lib.int_mul(%d, %d) == %d\n", x, y, Lib.int_mul(x, y));
    System.out.printf("BasicModule.get_hello() == %s\n", BasicModule.get_hello());
  }
}
