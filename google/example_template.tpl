{{! Forces a space or new line by BI_NEWLINE and BI_SPACE when
    STRIP_WHITESPACE is used. }}
var == {{VAR}}{{BI_NEWLINE}}
{{! html-escape by modifier
    http://google-ctemplate.googlecode.com/svn/trunk/doc/reference.html#template_modifier }}
escaped == {{ESCAPED:H=snippet}}{{BI_NEWLINE}}
{{! A section is hidden by default }}
{{#HELLO}}
  Hello world.{{BI_NEWLINE}}
{{/HELLO}}
{{#REPEATED}}
  {{REPEATED_VAR}}
  {{#SEPARATOR}}
    ,{{BI_SPACE}}
  {{/SEPARATOR}}
  {{#NEWLINE}}
    {{BI_NEWLINE}}
  {{/NEWLINE}}
{{/REPEATED}}
{{>SUB}}
