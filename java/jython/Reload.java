import org.python.core.PySystemState;
import org.python.core.PyObject;
import org.python.core.Py;

public class Reload {

  private static int RELOAD_LOOP = 5;

  private static int LOOP = 5;
  
  public static void main(String[] args) {
    PyObject old_builtin = null;
    for (int i = 0; i < RELOAD_LOOP; ++i) {
      // reload.py is reloaded per this loop body.
      PySystemState state = new PySystemState();
      Py.setSystemState(state);
      for (int j = 0; j < LOOP; ++j) {
        PyObject importer = state.getBuiltins()
          .__getitem__(Py.newString("__import__"));
        importer.__call__(Py.newString("reload")).__getattr__("method")
          .__call__();
      }
    }
  }
}
