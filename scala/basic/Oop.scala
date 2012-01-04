

class Complex(r: Double, i: Double) {
  val real = r
  val imaginary = i

  // constructor
  def this(r: Double) {
    this(r, 0)
  }

  def +(c: Complex) = {
    new Complex(real + c.real, imaginary + c.imaginary)
  }

  override def toString() = {
    "%f + %f*i".format(real, imaginary)
  }
}

object Oop {
  def main(args: Array[String]) {
    val a = new Complex(1, 0)
    val b = new Complex(0, 1)
    val c = a + b
    printf("c == %s\n", c)
  }
}
