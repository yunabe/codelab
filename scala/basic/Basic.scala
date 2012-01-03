
object Basic {

  def sum0(a: Int, b: Int) : Int = {
    return a + b
  }

  def sum1(a: Int, b: Int) : Int = {
    a + b
  }

  def sum2(a: Int, b: Int) = {
    a + b
    // NG: return a + b
    // error: method sum2 has return statement; needs result type
  }

  // Equivalent to def sayHello(name: String) : Unit = {
  def sayHello(name: String) {
    printf("Hello %s!\n", name)
  }

  // recursive method fact needs result type
  def fact(n: Int) : Int = {
    if (n > 0) {
      n * fact(n - 1)
    } else {
      1
    }
  }

  def main(args: Array[String]) {
    printf("sum0(%d, %d) == %d\n", 3, 4, sum0(3, 4))
    printf("sum1(%d, %d) == %d\n", 3, 4, sum1(3, 4))
    printf("sum2(%d, %d) == %d\n", 3, 4, sum2(3, 4))
    sayHello("scala")
    printf("fact(10) == %d\n", fact(10))
  }
}
