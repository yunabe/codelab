public class Data {
  private Data(int size) {
    data = new byte[size];
  }

  public static Data create(int size) {
    return new Data(size);
  }

  private byte[] data;
}
