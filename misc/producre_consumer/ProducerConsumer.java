import java.util.concurrent.SynchronousQueue;

public class ProducerConsumer {

  private static final int LOOP_SIZE = 1000 * 1000;

  private static void Produce(SynchronousQueue<Integer> queue) throws InterruptedException {
    for (int i = 0; i < LOOP_SIZE; i++) {
      queue.put(i);
    }
    queue.put(-1);
  }

  private static void Consume(SynchronousQueue<Integer> queue) throws InterruptedException{
    while (true) {
      int value = queue.take();
      if (value % (100 * 1000) == 0) {
        System.out.println("i == " + value);
      }
      if (value < 0) {
        break;
      }
    }
  }

  private static void mainInternal() throws InterruptedException {
    final SynchronousQueue<Integer> queue = new SynchronousQueue<Integer>();
    Thread producer = new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            Produce(queue);
          } catch(InterruptedException e) {
            System.err.println("producer thread is interrupted.");
          }
        }
      });
    Thread consumer = new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            Consume(queue);
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
