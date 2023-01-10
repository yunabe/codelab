using System;
namespace cil_compiler
{
    using System;
    using System.Collections.Generic;
    using System.Reflection;
    using System.Reflection.Emit;

    public class InstructionGenerator
    {
        private ILGenerator ilGenerator;
        private MethodBuilder methodBuilder;
        private List<Type> parameterTypes;

        public InstructionGenerator(TypeBuilder typeBuilder, MethodBuilder methodBuilder)
        {
            this.ilGenerator = methodBuilder.GetILGenerator();
            this.methodBuilder = methodBuilder;
            this.parameterTypes = new List<Type>();
        }

        public void Generate(ProgramNode node)
        {
            foreach (var function in node.Functions)
            {
                Generate(function);
            }
        }

        public void Generate(FunctionNode node)
        {
            // Generate code for function header
            foreach (var parameter in node.Parameters)
            {
                parameterTypes.Add(typeof(int));
            }
            methodBuilder.SetSignature(null, null, null, parameterTypes.ToArray(), null, null);
            // Generate code for function body
            foreach (var statement in node.Body)
            {
                Generate(statement);
            }
            // Generate code for function footer
            ilGenerator.Emit(OpCodes.Ret);
        }

        public void Generate(BinOpNode node)
        {
            Generate(node.Left);
            Generate(node.Right);
            switch (node.Op.Type)
            {
                case TokenType.PLUS:
                    ilGenerator.Emit(OpCodes.Add);
                    break;
                case TokenType.MINUS:
                    ilGenerator.Emit(OpCodes.Sub);
                    break;
                case TokenType.MULTIPLY:
                    ilGenerator.Emit(OpCodes.Mul);
                    break;
                case TokenType.DIVIDE:
                    ilGenerator.Emit(OpCodes.Div);
                    break;
                default:
                    throw new Exception("Invalid operator: " + node.Op.Type);
            }
        }

        public void Generate(IntegerNode node)
        {
            ilGenerator.Emit(OpCodes.Ldc_I4, (int)node.Token.Value);
        }

        public void Generate(VariableNode node)
        {
            ilGenerator.Emit(OpCodes.Ldarg, (short)parameterTypes.IndexOf(typeof(int)));
        }

        public void Generate(AssignNode node)
        {
            Generate(node.Value);
            ilGenerator.Emit(OpCodes.Starg, (short)parameterTypes.IndexOf(typeof(int)));
        }

        public void Generate(ReturnNode node)
        {
            Generate(node.Value);
            ilGenerator.Emit(OpCodes.Ret);
        }

        public void Generate(IfNode node)
        {
            Generate(node.Condition);
            var elseLabel = ilGenerator.DefineLabel();
            var endLabel = ilGenerator.DefineLabel();
            ilGenerator.Emit(OpCodes.Brfalse, elseLabel);
            foreach (var statement in node.ThenBlock)
            {
                Generate(statement);
            }
            ilGenerator.Emit(OpCodes.Br, endLabel);
            ilGenerator.MarkLabel(elseLabel);
            if (node.ElseBlock != null)
            {
                foreach (var statement in node.ElseBlock)
                {
                    Generate(statement);
                }
            }
            ilGenerator.MarkLabel(endLabel);
        }

        public void Generate(CallNode node)
        {
            foreach (var argument in node.Arguments)
            {
                Generate(argument);
            }
            ilGenerator.Emit(OpCodes.Call, methodBuilder);
        }

        public void Generate(ASTNode node)
        {
            if (node is BinOpNode binOpNode)
            {
                Generate(binOpNode);
            }
            else if (node is IntegerNode integerNode)
            {
                Generate(integerNode);
            }
            else if (node is VariableNode variableNode)
            {
                Generate(variableNode);
            }
            // Add similar dispatch logic for other AST node types
        }

    }
}

