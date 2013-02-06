import org.python.core.PySystemState;
import org.python.core.PyObject;
import org.python.core.PyModule;
import org.python.core.Py;

public class Reload {

  private static int RELOAD_LOOP = 5;

  private static int LOOP = 5;

  private static boolean USE_SET_SYSTEMSTATE = false;
  
  public static void main(String[] args) {
    PyModule reloadModule = null;
    for (int i = 0; i < RELOAD_LOOP; ++i) {
      // reload.py is reloaded per this loop body.
      PySystemState state;
      if (USE_SET_SYSTEMSTATE) {
        state = new PySystemState();
        // This looks like that we replace sys module (and sys.modules).
        Py.setSystemState(state);
      } else {
        state = Py.getSystemState();
        if (reloadModule != null) {
          // reload(mod)
          // This updates reloadModule rather than replace it with a new module.
          state.getBuiltins().__getitem__(Py.newString("reload"))
            .__call__(reloadModule);
        }
      }
      for (int j = 0; j < LOOP; ++j) {
        PyObject importer = state.getBuiltins()
          .__getitem__(Py.newString("__import__"));
        if (reloadModule == null) {
          reloadModule = (PyModule) importer.__call__(Py.newString("reload"));
        }
        reloadModule.__getattr__("method").__call__();
      }
    }
  }
}
