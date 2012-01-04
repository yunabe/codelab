
object Functional {

  def twice[A](f: A=>A) = (x:A) => f(f(x))

  def dbl(x: Int) = x * 2

  def bracket(s: String) = "{%s}".format(s)

  def main(args: Array[String]) {
    printf("twice(dbl)(3) == %d\n", twice(dbl)(3))
    printf("twice(bracket)(\"scala\") == %s\n", twice(bracket)("scala"))
    playWithPartial()
  }

  def sum(x: Int, y: Int) = x + y

  def playWithPartial() {
    var addTwo0 = (x: Int) => sum(x, 2)
    var addTwo1: Int => Int = x => sum(x, 2)
    var addTwo2 = sum(_: Int, 2)
    var addTwo3: Int => Int = sum(_, 2)

    val n = 10
    printf("addTwo0(%d) == %d\n", n, addTwo0(n))
    printf("addTwo1(%d) == %d\n", n, addTwo1(n))
    printf("addTwo2(%d) == %d\n", n, addTwo2(n))
    printf("addTwo3(%d) == %d\n", n, addTwo3(n))

    println(List(1, 2, 3).map(x => sum(x, 2)))
    println(List(1, 2, 3).map(sum(_, 2)))
  }
}
