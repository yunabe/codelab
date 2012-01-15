package com.yunabe.time;

public class Time {
  public Time(int hour, int minute, int second) {
    this.second = hour * 3600 + minute * 60 + second;
  }

  public int hour() {
    return second / (60 * 60);
  }

  public int minute() {
    return (second / 60) % 60;
  }
  
  public int second() {
    return second % 60;
  }

  public String toString() {
    return String.format("%02d:%02d:%02d", hour(), minute(), second());
  }

  private int second;
}
