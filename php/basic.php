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

function play_with_map() {
  echo "### play with array ###\n";
  $map = array("a" => "apple", "b" => "banana");
  $map["c"] = "cake";
  $map["d"] = "donuts";
  print_r($map);
  echo 'size of $map == ' .  count($map) . "\n";
  echo '$map["a"] == ' .  $map["a"] . "\n";
  // Hmm...
  unset($map["a"]);
  print_r($map);
}

function play_with_if() {
  echo "### play with if ###\n";
  $x = true;
  $y = true;
  if ($x) {
    echo "x is true.\n";
  } elseif ($y) {
    echo "y is true.\n";
  } else {
    echo "Neither x or y is true.\n";
  }

  if ($x)
    echo "x is true.\n";
  elseif ($y)
    echo "y is true.\n";
  else
    echo "Neither x or y is true.\n";

  if ($x) :
    echo "x is true.\n";
  elseif ($y) :
    echo "y is true.\n";
  else :
    echo "Neither x or y is true.\n";
  endif;  // Don't forget this semicolon.
}

function play_with_loop() {
  echo "### play with loop ###\n";
  for ($i = 0; $i < 3; $i++ ) {
    echo "\$i == " . $i . "\n";
  }
  for ($i = 0; $i < 3; $i++ ):
    echo "\$i == " . $i . "\n";
  endfor;

  $array = array(5, 8, 9, 'a' => 'apple');
  foreach ($array as $val) {
    echo "\$val == " . $val . "\n";
  }
  foreach ($array as $key => $val) {
    echo "(\$key, \$val) == (" . $key . ", " . $val . ")\n";
  }

  $count = 0;
  while ($count < 5) {
    echo "\$count == " . $count . "\n";
    $count += 1;
  }
}

function play_with_string() {
  echo "### play with loop ###\n";
  $val = 10;
  echo '>> $val\t\n' . "<<\n";
  echo "[[ $val\t\n" . "]]\n";
  
  // Here document
  // (1) EOF; should not be indented.
  // (2) Newline before EOF is NOT included in a here-document.
  // (3) Like double-quoted string, escaped-string and $val are evaluated.
  print <<< EOF
This\tis\there-document (\$val == $val.)

EOF;

  // Nowdoc
  // With '', escaped-string or $val are not converted.
  print <<< 'EOF'
This\tis\there-document (\$val == $val.)

EOF;
}

function main() {
  $n = 6;
  echo "fact($n) == " . fact($n) . "\n";
  play_with_array();
  play_with_map();
  play_with_if();
  play_with_loop();
  play_with_string();
}

main();
?>
