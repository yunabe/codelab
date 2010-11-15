class Root;
class Leaf;

class Root {
 public:
  Root(const Leaf& left, const Leaf& right) : left_(left), right_(right) { };
  const Leaf& get_left() { return left_; };
  const Leaf& get_right() { return right_; };
 private:
  const Leaf& left_;
  const Leaf& right_;
};

class Leaf {
 public:
  Leaf(int value) : value_(value) { };
  int get_value() { return value_; };
 private:
  const int value_;
};
