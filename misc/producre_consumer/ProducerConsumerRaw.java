import java.util.concurrent.SynchronousQueue;

public class ProducerConsumerRaw {

  private static final int LOOP_SIZE = 1000 * 1000;

  private static int value = -1;

  private static final Object sync = new Object();

  private static void Produce() throws InterruptedException {
    for (int i = 0; i < LOOP_SIZE; i++) {
      synchronized (sync) {
        if (value >= 0) {
          sync.wait();
        }
        value = i;
        sync.notify();
      }
    }
  }

  private static void Consume() throws InterruptedException{
    while (true) {
      synchronized (sync) {
        if (value < 0) {
          sync.wait();
        }
        int i = value;
        value = -1;
        sync.notify();
        if (i % (10 * 1000) == 0) {
          System.out.println("i == " + i);
        }
        if (i + 1 == LOOP_SIZE) {
          break;
        }
      }
    }
  }

  private static void mainInternal() throws InterruptedException {
    final SynchronousQueue<Integer> queue = new SynchronousQueue<Integer>();
    Thread producer = new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            Produce();
          } catch(InterruptedException e) {
            System.err.println("producer thread is interrupted.");
          }
        }
      });
    Thread consumer = new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            Consume();
          } catch(InterruptedException e) {
            System.err.println("consumer thread is interrupted.");
          }
        }
      });
    producer.start();
    consumer.start();
    System.out.println("Hello ProducerConsumer!");
    producer.join();
    consumer.join();
  }

  public static void main(String[] args) {
    try {
      mainInternal();
    } catch (InterruptedException e) {
    }
  }
}
