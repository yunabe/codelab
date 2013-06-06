<?php

class MyParent {
  public $prop;

  // Constructor
  function __construct($prop) {
    $this->prop = $prop;
  }

  function addProp($val) {
    return $this->prop + $val;
  }
}

class MyChild extends MyParent {
  function __construct($x, $y) {
    parent::__construct($x + $y);
  }

  function addProp($val) {
    return parent::addProp($val * 2);
  }
}

interface MyInterface {
  function sayHello();
}

class MyImpl implements MyInterface {
  function sayHello() {
    echo "Hello MyImpl!\n";
  }
}

abstract class MyAbstract {
  abstract function absMethod();
}

abstract class MyConcrete extends MyAbstract {
  function absMethod() {}
}

function main() {

  $parent = new MyParent(4);
  echo "myclass.prop == " . $parent->prop . "\n";
  echo "myclass.addProp == " . $parent->addProp(3) . "\n";

  $child = new MyChild(8, 7);
  echo "child.prop == " . $child->prop . "\n";
  echo "child.addProp == " . $child->addProp(3) . "\n";

  $myimp = new MyImpl();
  $myimp->sayHello();
  // Syntax error.
  // (new MyImpl())->sayHello();
}

main();

?>
