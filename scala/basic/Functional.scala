
object Functional {

  def twice[A](f: A=>A) = (x:A) => f(f(x))

  def dbl(x: Int) = x * 2

  def bracket(s: String) = "{%s}".format(s)
  
  def main(args: Array[String]) {
    printf("twice(dbl)(3) == %d\n", twice(dbl)(3))
    printf("twice(bracket)(\"scala\") == %s\n", twice(bracket)("scala"))
  }
}
