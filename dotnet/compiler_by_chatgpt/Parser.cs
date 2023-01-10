using System;
namespace cil_compiler
{
    using System;
    using System.Collections.Generic;
    using System.Reflection.Emit;

        public class Parser
        {
            private readonly Lexer lexer;
            private Token currentToken;

            public Parser(Lexer lexer)
            {
                this.lexer = lexer;
                this.currentToken = lexer.GetNextToken();
            }

            public ASTNode Program()
            {
                var functions = new List<FunctionNode>();
                while (currentToken.Type != TokenType.EOF)
                {
                    functions.Add(Function());
                }
                return new ProgramNode(functions);
            }

            private FunctionNode Function()
            {
                Eat(TokenType.FN);
                Eat(TokenType.LPAREN);
                var parameters = new List<string>();
                while (currentToken.Type == TokenType.ID)
                {
                    parameters.Add((string)currentToken.Value);
                    Eat(TokenType.ID);
                    if (currentToken.Type == TokenType.COMMA)
                    {
                        Eat(TokenType.COMMA);
                    }
                }
                Eat(TokenType.RPAREN);
                Eat(TokenType.LBRACE);
                var body = Block();
                Eat(TokenType.RBRACE);
                return new FunctionNode(parameters, body);
            }

            private List<ASTNode> Block()
            {
                var statements = new List<ASTNode>();
                while (currentToken.Type != TokenType.RBRACE)
                {
                    statements.Add(Statement());
                }
                return statements;
            }

            private ASTNode Statement()
            {
                if (currentToken.Type == TokenType.ID)
                {
                    var variable = (string)currentToken.Value;
                    Eat(TokenType.ID);
                    Eat(TokenType.ASSIGN);
                    var value = Expr();
                    Eat(TokenType.SEMI);
                    return new AssignNode(currentToken, variable, value);
                }
                if (currentToken.Type == TokenType.RETURN)
                {
                    var token = currentToken;
                    Eat(TokenType.RETURN);
                    var value = Expr();
                    Eat(TokenType.SEMI);
                    return new ReturnNode(token, value);
                }
                if (currentToken.Type == TokenType.FN)
                {
                    return Function();
                }
                if (currentToken.Type == TokenType.IF)
                {
                    Eat(TokenType.IF);
                    Eat(TokenType.LPAREN);
                    var condition = Expr();
                    Eat(TokenType.RPAREN);
                    Eat(TokenType.LBRACE);
                    var thenBlock = Block();
                    Eat(TokenType.RBRACE);
                    List<ASTNode> elseBlock = null;
                    if (currentToken.Type == TokenType.ELSE)
                    {
                        Eat(TokenType.ELSE);
                        Eat(TokenType.LBRACE);
                        elseBlock = Block();
                        Eat(TokenType.RBRACE);
                    }
                    return new IfNode(condition, thenBlock, elseBlock);
                }
                if (currentToken.Type == TokenType.ID)
                {
                    var function = (string)currentToken.Value;
                    Eat(TokenType.ID);
                    Eat(TokenType.LPAREN);
                    var arguments = new List<ASTNode>();
                    while (currentToken.Type != TokenType.RPAREN)
                    {
                        arguments.Add(Expr());
                        if (currentToken.Type == TokenType.COMMA)
                        {
                            Eat(TokenType.COMMA);
                        }
                    }
                    Eat(TokenType.RPAREN);
                    Eat(TokenType.SEMI);
                    return new CallNode(currentToken, function, arguments);
                }
                throw new Exception("Invalid token: " + currentToken.Type);
            }

            private ASTNode Expr()
            {
                var node = Term();
                while (new[] { TokenType.PLUS, TokenType.MINUS }.Contains(currentToken.Type))
                {
                    var token = currentToken;
                    if (token.Type == TokenType.PLUS)
                    {
                        Eat(TokenType.PLUS);
                    }
                    else
                    {
                        Eat(TokenType.MINUS);
                    }
                    node = new BinOpNode(node, token, Term());
                }
                return node;
            }

            private ASTNode Term()
            {
                var node = Factor();
                while (new[] { TokenType.MULTIPLY, TokenType.DIVIDE }.Contains(currentToken.Type))
                {
                    var token = currentToken;
                    if (token.Type == TokenType.MULTIPLY)
                    {
                        Eat(TokenType.MULTIPLY);
                    }
                    else
                    {
                        Eat(TokenType.DIVIDE);
                    }
                    node = new BinOpNode(node, token, Factor());
                }
                return node;
            }

            private ASTNode Factor()
            {
                var token = currentToken;
                if (token.Type == TokenType.INTEGER)
                {
                    Eat(TokenType.INTEGER);
                    return new IntegerNode(token);
                }
                if (token.Type == TokenType.LPAREN)
                {
                    Eat(TokenType.LPAREN);
                    var node = Expr();
                    Eat(TokenType.RPAREN);
                    return node;
                }
                if (token.Type == TokenType.ID)
                {
                    Eat(TokenType.ID);
                    return new VariableNode(token);
                }
                if (token.Type == TokenType.FN)
                {
                    return Function();
                }
                if (token.Type == TokenType.IF)
                {
                    Eat(TokenType.IF);
                    Eat(TokenType.LPAREN);
                    var condition = Expr();
                    Eat(TokenType.RPAREN);
                    Eat(TokenType.LBRACE);
                    var thenBlock = Block();
                    Eat(TokenType.RBRACE);
                    List<ASTNode> elseBlock = null;
                    if (currentToken.Type == TokenType.ELSE)
                    {
                        Eat(TokenType.ELSE);
                        Eat(TokenType.LBRACE);
                        elseBlock = Block();
                        Eat(TokenType.RBRACE);
                    }
                    return new IfNode(condition, thenBlock, elseBlock);
                }
                throw new Exception("Invalid token: " + token.Type);
            }

            private void Eat(TokenType type)
            {
                if (currentToken.Type == type)
                {
                    currentToken = lexer.GetNextToken();
                }
                else
                {
                    throw new Exception($"Invalid token: expected {type}, got {currentToken.Type}");
                }
            }
        }

        public abstract class ASTNode
        {
        }

        public class ProgramNode : ASTNode
        {
            public List<FunctionNode> Functions { get; }

            public ProgramNode(List<FunctionNode> functions)
            {
                this.Functions = functions;
            }
        }

        public class FunctionNode : ASTNode
        {
            public List<string> Parameters { get; }
            public List<ASTNode> Body { get; }

            public FunctionNode(List<string> parameters, List<ASTNode> body)
            {
                this.Parameters = parameters;
                this.Body = body;
            }
        }

        public class BinOpNode : ASTNode
        {
            public ASTNode Left { get; }
            public Token Op { get; }
            public ASTNode Right { get; }

            public BinOpNode(ASTNode left, Token op, ASTNode right)
            {
                this.Left = left;
                this.Op = op;
                this.Right = right;
            }
        }

        public class IntegerNode : ASTNode
        {
            public Token Token { get; }

            public IntegerNode(Token token)
            {
                this.Token = token;
            }
        }

        public class VariableNode : ASTNode
        {
            public Token Token { get; }

            public VariableNode(Token token)
            {
                this.Token = token;
            }
        }

        public class AssignNode : ASTNode
        {
            public Token Token { get; }
            public string Variable { get; }
            public ASTNode Value { get; }

            public AssignNode(Token token, string variable, ASTNode value)
            {
                this.Token = token;
                this.Variable = variable;
                this.Value = value;
            }
        }

        public class IfNode : ASTNode
        {
            public ASTNode Condition { get; }
            public List<ASTNode> ThenBlock { get; }
            public List<ASTNode> ElseBlock { get; }

            public IfNode(ASTNode condition, List<ASTNode> thenBlock, List<ASTNode> elseBlock)
            {
                this.Condition = condition;
                this.ThenBlock = thenBlock;
                this.ElseBlock = elseBlock;
            }
        }

        public class ReturnNode : ASTNode
        {
            public Token Token { get; }
            public ASTNode Value { get; }

            public ReturnNode(Token token, ASTNode value)
            {
                this.Token = token;
                this.Value = value;
            }
        }

        public class CallNode : ASTNode
        {
            public Token Token { get; }
            public string Function { get; }
            public List<ASTNode> Arguments { get; }

            public CallNode(Token token, string function, List<ASTNode> arguments)
            {
                this.Token = token;
                this.Function = function;
                this.Arguments = arguments;
            }
        }
    }


