
object Collection {
  def main(args: Array[String]) {
    // Abbreviation of
    // var list: List[Int] = List[Int](0, 1, 2, 3, 4, 5)
    val list = List(0, 1, 2, 3, 4, 5)
    list.foreach(x => println(x))

    def sum(x: Int, y: Int) = {
      printf("x: %d, y: %d\n", x, y)
      x + y
    }
    println(list.foldLeft(0)(sum))
    println(list.foldRight(0)(sum))

    print("list.filter(x => x % 2 == 0) : ")
    println(list.filter(x => x % 2 == 0))

    print("list.map(x => x * x) : ")
    println(list.map(x => x * x))

    for (x <- list) {
      println(x)
    }
  }
}
