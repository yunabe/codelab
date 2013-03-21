import org.apache.bcel.generic.ClassGen;
import org.apache.bcel.generic.MethodGen;
import org.apache.bcel.Constants;
import org.apache.bcel.generic.Type;
import org.apache.bcel.generic.InstructionList;
import org.apache.bcel.generic.InstructionFactory;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * An example of runtime class generation with BCEL.
 * How to run:
 *   javac -cp bcel-5.2.jar *.java && java -cp bcel-5.2.jar:. Dynamic
 */
class Dynamic {
  public interface Adder {
    int add(int n);
  }

  static Pattern NAME_PATTERN = Pattern.compile("$\\+(\\d+)^");

  static class AdderLoader extends ClassLoader {
    private int index = 0;
    
    protected Class<?> createAdderClass(int value) {
      String className = String.format("AdderImpl%d", index);
      index++;
      ClassGen cgen = new ClassGen(className, "java.lang.Object", null,
                                   Constants.ACC_PUBLIC,
                                   new String[] {"Dynamic$Adder"});
      cgen.addEmptyConstructor(Constants.ACC_PUBLIC);

      InstructionList ilist = new InstructionList();
      MethodGen addGen = new MethodGen(Constants.ACC_PUBLIC,
                                       Type.INT,
                                       new Type[]{Type.INT},
                                       null,
                                       "add",
                                       className,  // for what?
                                       ilist,
                                       cgen.getConstantPool());

      InstructionFactory ifact = new InstructionFactory(cgen);
      ilist.append(ifact.createLoad(Type.INT, 1));
      ilist.append(ifact.createConstant(value));
      ilist.append(ifact.createBinaryOperation("+", Type.INT));
      ilist.append(ifact.createReturn(Type.INT));

      addGen.setMaxStack();
      // We don't need to call addGen.setMaxLocals().
      
      // NOTE: getMethod fails with NullPointerException if ilist has no instruction.
      cgen.addMethod(addGen.getMethod());
      ilist.dispose();
      
      byte[] binary = cgen.getJavaClass().getBytes();
      return defineClass(className, binary, 0, binary.length);
    }
  }
  
  public static void main(String[] args) {
    try {
      AdderLoader loader = new AdderLoader();
      Class<?> cls;
      Adder adder;

      int n = 11;
      cls = loader.createAdderClass(25);
      adder = (Adder)cls.newInstance();
      System.out.println(String.format("adder.add(%d) == %d", n, adder.add(n)));
      
      cls = loader.createAdderClass(12);
      adder = (Adder)cls.newInstance();
      System.out.println(String.format("adder.add(%d) == %d", n, adder.add(n)));
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
