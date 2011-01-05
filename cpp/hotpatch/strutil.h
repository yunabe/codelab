#ifndef YUNABE_UTIL_CPP_STRUTIL_H_
#define YUNABE_UTIL_CPP_STRUTIL_H_

#include <string>
#include <vector>

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

using std::string;
using std::vector;

namespace strutil {

static string format(const char* fmt, ...) {
  va_list args;
  char* buffer = NULL;
  va_start(args, fmt);
  int rc = vasprintf(&buffer, fmt, args);
  va_end(args);
  string result;
  if (rc >= 0) {
    result = buffer;
  }
  if (buffer != NULL) {
    free(buffer);
  }
  return result;
}

static void split(const string& s, char sep, vector<string>* result) {
  size_t seek_pos = 0;
  while (seek_pos < s.size() + 1) {
    size_t sep_pos = s.find_first_of(sep, seek_pos);
    if (sep_pos == string::npos) {
      sep_pos = s.size();
    }
    result->push_back(s.substr(seek_pos, sep_pos - seek_pos));
    seek_pos = sep_pos + 1;
  }
}

static string join(const string& combinator, const vector<string>& list) {
  if (list.size() == 0) {
    return "";
  }
  size_t total_size = 0;
  for (int i = 0; i < list.size(); ++i) {
    total_size += list[i].length();
  }
  total_size += combinator.length() * (list.size() - 1);
  string result;
  result.reserve(total_size);
  for (int i = 0; i < list.size(); ++i) {
    if(i != 0) {
      result.append(combinator);
    }
    result.append(list[i]);
  }
  return result;
}

inline bool __is_whitespace(char c) {
  return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f';
}

static string strip(const string& s) {
  size_t start, end;
  for (start = 0; start < s.length(); ++start) {
    if (!__is_whitespace(s[start])) {
      break;
    }
  }
  for (end = s.length() - 1; end > start; --end) {
    if (!__is_whitespace(s[end])) {
      break;
    }
  }
  return s.substr(start, end + 1 - start);
}

static string lstrip(const string& s) {
  size_t start;
  for (start = 0; start < s.length(); ++start) {
    if (!__is_whitespace(s[start])) {
      break;
    }
  }
  return s.substr(start, s.length() - start);
}

static string rstrip(const string& s) {
  int end; // Note that we can not use size_t here because end can be negative.
  for (end = s.length() - 1; end >= 0; --end) {
    if (!__is_whitespace(s[end])) {
      break;
    }
  }
  return s.substr(0, end + 1);
}

inline string trim(const string& s) {
  return strip(s);
}

inline string ltrim(const string& s) {
  return lstrip(s);
}

inline string rtrim(const string& s) {
  return rstrip(s);
}

}  // namespace strutil
#endif  // YUNABE_UTIL_CPP_STRUTIL_H_
