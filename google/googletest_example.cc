#include <gtest/gtest.h>

class ExampleTest : public testing::Test {
};

TEST_F(ExampleTest, SimpleTest) {
  EXPECT_EQ(7, 3 + 4);
}
