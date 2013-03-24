import org.apache.bcel.classfile.Method;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.ClassParser;
import org.apache.bcel.generic.ClassGen;
import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.MethodGen;
import org.apache.bcel.generic.FieldGen;
import org.apache.bcel.generic.InstructionList;
import org.apache.bcel.generic.InstructionHandle;
import org.apache.bcel.generic.InstructionFactory;
import org.apache.bcel.generic.Type;
import org.apache.bcel.generic.ObjectType;
import org.apache.bcel.generic.LDC;
import org.apache.bcel.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.List;

class HookInjector {

  public static void castToObject(InstructionFactory ifact,
                                  InstructionList ilist,
                                  Type type) {
    switch (type.getType()) {
    case Constants.T_OBJECT:
    case Constants.T_ARRAY:
      // No cast
      break;
    case Constants.T_INT:
      ilist.append(ifact.createInvoke(
          "java.lang.Integer",
          "valueOf",
          new ObjectType("java.lang.Integer"),
          new Type[]{Type.INT},
          Constants.INVOKESTATIC));
      break;
    default:
      throw new RuntimeException("Unexpected type: " + type);
    }
  }

  public static void castToPrimitive(
      InstructionFactory ifact,
      InstructionList ilist,
      Type type) {
    switch (type.getType()) {
    case Constants.T_OBJECT:
    case Constants.T_ARRAY:
      // No cast
      break;
    case Constants.T_INT:
      ilist.append(
          ifact.createCheckCast(new ObjectType("java.lang.Integer")));
      ilist.append(
          ifact.createInvoke(
              "java.lang.Integer",
              "intValue",
              Type.INT,
              Type.NO_ARGS,
              Constants.INVOKEVIRTUAL));
      break;
    default:
      throw new RuntimeException("Unexpected type: " + type);
    }
  }

  public static JavaClass createRunner(String className, String innerName, Method method) {
    ClassGen runner = new ClassGen(innerName, "java.lang.Object", null,
                                   Constants.ACC_PUBLIC,
                                   new String[] {"Hook$Runner"});
    runner.addEmptyConstructor(Constants.ACC_PUBLIC);

    runner.addField(new FieldGen(Constants.ACC_PUBLIC | Constants.ACC_STATIC,
                                 new ObjectType(innerName),
                                 "INSTANT",
                                 runner.getConstantPool()).getField());
    InstructionFactory ifact = new InstructionFactory(runner);

    InstructionList ilist = new InstructionList();
    MethodGen staticBlock = new MethodGen(Constants.ACC_STATIC,
                                          Type.VOID,
                                          Type.NO_ARGS,
                                          null,
                                          "<clinit>",
                                          innerName,  // for what?
                                          ilist,
                                          runner.getConstantPool());
    ilist.append(ifact.createNew(new ObjectType(innerName)));
    ilist.append(ifact.createDup(1));
    ilist.append(ifact.createInvoke(innerName,
                                    "<init>",
                                    Type.VOID,
                                    Type.NO_ARGS,
                                    Constants.INVOKESPECIAL));
    ilist.append(ifact.createPutStatic(innerName,
                                       "INSTANT",
                                       new ObjectType(innerName)));
    ilist.append(ifact.createReturn(Type.VOID));
    staticBlock.setMaxStack();
    runner.addMethod(staticBlock.getMethod());
    ilist.dispose();

    ilist = new InstructionList();
    MethodGen runMethod = new MethodGen(
        Constants.ACC_PUBLIC,
        Type.OBJECT,
        Type.getArgumentTypes("([Ljava/lang/Object;)V"),
        null,
        "run",
        innerName,  // for what?
        ilist,
        runner.getConstantPool());
    Type[] argTypes = method.getArgumentTypes();
    for (int i = 0; i < argTypes.length; ++i) {
      ilist.append(ifact.createLoad(Type.OBJECT, 1));
      ilist.append(ifact.createConstant(i));
      ilist.append(ifact.createArrayLoad(Type.OBJECT));
      castToPrimitive(ifact, ilist, argTypes[i]);
    }
    ilist.append(ifact.createInvoke(
        className,
        method.getName() + "$original",
        method.getReturnType(),
        method.getArgumentTypes(),
        Constants.INVOKESTATIC));
    castToObject(ifact, ilist, method.getReturnType());
    ilist.append(ifact.createReturn(Type.OBJECT));

    runMethod.setMaxStack();
    runner.addMethod(runMethod.getMethod());
    ilist.dispose();

    return runner.getJavaClass();
  }

  public static Method createHookedMethod(ClassGen cgen, Method method, String innerName) {
    InstructionFactory ifact = new InstructionFactory(cgen);
    InstructionList ilist = new InstructionList();
    MethodGen hookMethod = new MethodGen(
        Constants.ACC_PUBLIC | Constants.ACC_STATIC,
        method.getReturnType(),
        method.getArgumentTypes(),
        null,
        method.getName(),
        cgen.getClassName(),
        ilist,
        cgen.getConstantPool());
    ilist.append(ifact.createConstant(
        cgen.getClassName() + "." + method.getName()));
    ilist.append(ifact.createGetStatic(
        innerName,
        "INSTANT",
        new ObjectType(innerName)));
    ilist.append(ifact.createConstant(method.getArgumentTypes().length));
    ilist.append(ifact.createNewArray(Type.OBJECT, (short)1));
    for (int i = 0; i < method.getArgumentTypes().length; ++i) {
      ilist.append(ifact.createDup(1));
      ilist.append(ifact.createConstant(i));
      ilist.append(ifact.createLoad(method.getArgumentTypes()[i], i));
      castToObject(ifact, ilist, method.getArgumentTypes()[i]);
      ilist.append(ifact.createArrayStore(Type.OBJECT));
    }
    ilist.append(ifact.createInvoke(
        "Hook",
        "hook",
        Type.OBJECT,
        Type.getArgumentTypes(
            "(Ljava/lang/String;LHook$Runner;[Ljava/lang/Object;)LV"),
        Constants.INVOKESTATIC));
    castToPrimitive(ifact, ilist, method.getReturnType());
    ilist.append(ifact.createReturn(method.getReturnType()));

    hookMethod.setMaxStack();

    Method returnVal = hookMethod.getMethod();
    ilist.dispose();
    return returnVal;
  }

  public static void injectHook(JavaClass cls, List<JavaClass> newClasses) {
    ClassGen cgen = new ClassGen(cls);
    ConstantPoolGen pgen = cgen.getConstantPool();
    Method[] methods = cgen.getMethods();
    System.out.println(cgen.getClassName());

    int innerClassIndex = 0;
    for (Method method : methods) {
      if (!method.isStatic()) {
        continue;
      }
      if (method.getName().equals("<clinit>") ||
          method.getName().equals("main")) {
        continue;
      }
      System.out.println("  " + method + "(static: " + method.getName() + ")");
      MethodGen originalGen = new MethodGen(method, cgen.getClassName(), pgen);
      originalGen.setName(originalGen.getName() + "$original");
      cgen.addMethod(originalGen.getMethod());

      String innerName = String.format("%s$runner%d", cgen.getClassName(), innerClassIndex);
      innerClassIndex++;
      newClasses.add(createRunner(cgen.getClassName(), innerName, method));
      cgen.replaceMethod(method, createHookedMethod(cgen, method, innerName));
    }

    newClasses.add(cgen.getJavaClass());
  }

  private static final File OUT_DIR = new File("injected");
  
  public static void main(String[] args) {
    OUT_DIR.mkdirs();
    try {
      for (String classFile : args) {
        ArrayList<JavaClass> newClasses = new ArrayList<JavaClass>();
        injectHook(new ClassParser(classFile).parse(), newClasses);
        for (JavaClass newClass : newClasses) {
          FileOutputStream fos = new FileOutputStream(
              new File(OUT_DIR, newClass.getClassName() + ".class"));
          newClass.dump(fos);
          fos.close();
        }
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
