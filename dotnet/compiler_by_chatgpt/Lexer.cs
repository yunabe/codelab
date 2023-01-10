using System;
// using System.Collections.Generic;
// using System.Linq;

namespace cil_compiler
{
    public enum TokenType
    {
        INTEGER,
        ID,
        FN,
        LET,
        RETURN,
        IF,
        ELSE,
        PLUS,
        MINUS,
        MULTIPLY,
        DIVIDE,
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        SEMI,
        COMMA,  // Added by human.
        ASSIGN,  // Added by human
        EOF
    }

    public class Token
    {
        public TokenType Type { get; }
        public object Value { get; }

        public Token(TokenType type, object value)
        {
            this.Type = type;
            this.Value = value;
        }
    }

    public class Lexer
    {
        private readonly string input;
        private int position;
        private char currentChar;
        private readonly Dictionary<string, TokenType> keywords;

        public Lexer(string input)
        {
            this.input = input;
            this.position = 0;
            this.currentChar = input[position];
            this.keywords = new Dictionary<string, TokenType>
        {
            { "fn", TokenType.FN },
            { "let", TokenType.LET },
            { "return", TokenType.RETURN },
            { "if", TokenType.IF },
            { "else", TokenType.ELSE }
        };
        }

        public Token GetNextToken()
        {
            while (currentChar != '\0')
            {
                if (char.IsWhiteSpace(currentChar))
                {
                    SkipWhitespace();
                    continue;
                }

                if (char.IsLetter(currentChar))
                {
                    string identifier = "";
                    while (currentChar != '\0' && char.IsLetterOrDigit(currentChar))
                    {
                        identifier += currentChar;
                        Advance();
                    }

                    if (keywords.ContainsKey(identifier))
                    {
                        return new Token(keywords[identifier], identifier);
                    }
                    else
                    {
                        return new Token(TokenType.ID, identifier);
                    }
                }

                if (char.IsDigit(currentChar))
                {
                    return new Token(TokenType.INTEGER, GetNumber());
                }

                if (currentChar == '+')
                {
                    Advance();
                    return new Token(TokenType.PLUS, '+');
                }

                if (currentChar == '-')
                {
                    Advance();
                    return new Token(TokenType.MINUS, '-');
                }

                if (currentChar == '*')
                {
                    Advance();
                    return new Token(TokenType.MULTIPLY, '*');
                }

                if (currentChar == '/')
                {
                    Advance();
                    return new Token(TokenType.DIVIDE, '/');
                }

                if (currentChar == '(')
                {
                    Advance();
                    return new Token(TokenType.LPAREN, '(');
                }

                if (currentChar == ')')
                {
                    Advance();
                    return new Token(TokenType.RPAREN, ')');
                }

                if (currentChar == '{')
                {
                    Advance();
                    return new Token(TokenType.LBRACE, '{');
                }

                if (currentChar == '}')
                {
                    Advance();
                    return new Token(TokenType.RBRACE, '}');
                }

                if (currentChar == ';')
                {
                    Advance();
                    return new Token(TokenType.SEMI, ';');
                }

                throw new Exception("Invalid character: " + currentChar);
            }

            return new Token(TokenType.EOF, null);
        }

        private void SkipWhitespace()
        {
            while (currentChar != '\0' && char.IsWhiteSpace(currentChar))
            {
                Advance();
            }
        }

        private int GetNumber()
        {
            string number = "";
            while (currentChar != '\0' && char.IsDigit(currentChar))
            {
                number += currentChar;
                Advance();
            }
            return int.Parse(number);
        }

        private void Advance()
        {
            position++;
            if (position >= input.Length)
            {
                currentChar = '\0';
            }
            else
            {
                currentChar = input[position];
            }
        }
    }
}

