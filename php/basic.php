<?php

function fact($n) {
  if ($n > 1) {
    return $n * fact($n - 1);
  } else {
    return 1;
  }
}

function play_with_array() {
  echo "### play with array ###\n";
  $array = array("apple", "banana");
  $array[] = "cake";
  $array[] = "donuts";
  print_r($array);
  echo $array[0] . ", " . $array[1] . ", " . $array[2] . "\n";
  echo "length of array == " . count($array) . "\n";

  echo "slice array\n";
  $sliced = array_slice($array, 1, 2);
  // As PHP slice copies contents of an array like Python,
  // this operation does not affect to the original array.
  $sliced[0] = "***";
  print_r($sliced);

  echo "array_pop: " . array_pop($array) . "\n";
  print_r($array);
}

function main() {
  $n = 6;
  echo "fact($n) == " . fact($n) . "\n";
  play_with_array();
}

main();
?>
