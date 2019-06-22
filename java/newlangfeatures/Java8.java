package jp.yunabe.codelab;

import java.util.stream.Collectors;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Java8 {

  private static void learnStream() {
    System.out.println("#### stream in Java 8 ###");
    ArrayList<Integer> input = new ArrayList(Arrays.asList(0, 1, 2, 3, 4, 5, 6, 7, 8, 9));
    Stream<Integer> filtered = input.stream().filter(i -> i % 3 == 0);
    Stream<String> mapped = filtered.map(i -> String.format("%03d", i));
    List<String> output = mapped.collect(Collectors.toList());
    System.out.printf("output: %s\n", output);
  }
  
  public static void main(String[] args) {
      learnStream();
  }
}
