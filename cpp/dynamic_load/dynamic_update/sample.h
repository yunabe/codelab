
class Sample {
 public:
  Sample(int x, int y);
  virtual ~Sample();
  int method();
  virtual int virtual_method();
  
 private:
  int x_;
  int y_;
};
