#include <ctemplate/template.h>
#include <stdio.h>
#include <string>
#include <vector>

RegisterTemplateFilename(EXAMPLE_TEMPLATE, "example_template.tpl");
#include "example_template.tpl.varnames.h"
RegisterTemplateFilename(EXAMPLE_SUBTEMPLATE, "example_subtemplate.tpl");
#include "example_subtemplate.tpl.varnames.h"

using ctemplate::ExpandTemplate;
using ctemplate::TemplateDictionary;
using ctemplate::STRIP_WHITESPACE;
using std::string;
using std::vector;

void fill_subtemplate(TemplateDictionary* dict, int value) {
  dict->SetFilename(EXAMPLE_SUBTEMPLATE);
  dict->SetIntValue(kes_VALUE, value);
}

int main(int argc, char** argv) {
  // name ("example dict") is used only for debugging.
  TemplateDictionary dict("example dict");
  dict.SetValue(ket_VAR, "foo");
  dict.SetValue(ket_ESCAPED, "<script>alert('hello!');</script><b>Bold</b>");
  dict.ShowSection(ket_HELLO);
  vector<string> vars;
  vars.push_back("foo");
  vars.push_back("bar");
  vars.push_back("baz");
  for (int i = 0; i < vars.size(); ++i) {
    TemplateDictionary* repeated_dict =
      dict.AddSectionDictionary(ket_REPEATED);
    if (i != vars.size() - 1) {
      repeated_dict->ShowSection(ket_SEPARATOR);
    } else {
      repeated_dict->ShowSection(ket_NEWLINE);
    }
    repeated_dict->SetValue(ket_REPEATED_VAR, vars[i]);
  }
  vector<int> subvalues;
  subvalues.push_back(22);
  subvalues.push_back(11);
  subvalues.push_back(15);
  for (int i = 0; i < subvalues.size(); ++i) {
    TemplateDictionary* sub_dict = dict.AddIncludeDictionary(ket_SUB);
    fill_subtemplate(sub_dict, subvalues[i]);
  }
  string dict_dump;
  dict.DumpToString(&dict_dump);
  printf("-- Dictionary dump --\n%s", dict_dump.c_str());
  string output;
  // http://google-ctemplate.googlecode.com/svn/trunk/doc/reference.html#strip
  // STRIP_WHITESPACE  : Removes whitespace (including a new line)
  //                     at the beginning and end of each line.
  // STRIP_BLANK_LINES : Remove all blank lines.
  // DO_NOT_STRIP      : Do nothing.
  ExpandTemplate(EXAMPLE_TEMPLATE, ctemplate::STRIP_WHITESPACE, &dict, &output);
  printf("-- Result --\n%s", output.c_str());
  return 0;
}
