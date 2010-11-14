#include <stdio.h>
#include <google/protobuf/text_format.h>

#include "example.pb.h"

using google::protobuf::TextFormat;

int main(int argc, char** argv) {
  example::Person person;
  person.set_name("yunabe");
  person.set_id(1234);
  person.set_gender(example::Person::MALE);
  example::Birthday* birthday = person.mutable_birthday();
  birthday->set_year(1990);
  birthday->set_month(7);
  birthday->set_day(15);
  // Classname of internal message is Parent_Child.
  example::Person_Attribute* attr;
  attr = person.add_attribute();
  attr->set_name("Nationality");
  attr->set_value("Japan");
  attr = person.add_attribute();
  attr->set_name("Job title");
  attr->set_value("Software Engineer");
  std::string output;
  TextFormat::PrintToString(person, &output);
  printf("%s", output.c_str());
  person.Clear();
  TextFormat::ParseFromString("id: 77\n"
                              "name: 'piyo'",
                              &person);
  printf("id is %d\n", person.id());
  printf("name is %s\n", person.name().c_str());
  return 0;
}
