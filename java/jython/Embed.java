import org.python.util.PythonInterpreter;
import java.util.Properties;

/*
 * How to embed Jython to Java programs.
 * 1. Download jython-2.5.3.jar from www.jython.org.
 * 2. Download jython-2.5.3-sources.jar to get Python libraries for Jython.
 * 3. Unzip sources.jar to jython-src
 *   mkdir jython-src
 *   unzip jython-2.5.3-sources.jar -d jython-src
 * 4. Build Python libraries (copy files from lib-python to Lib).
 *   cd jython-src
 *   # (There must be a better way :P)
 *   ant copy-cpythonlib -Dpython.lib=lib-python/2.5 -Djython.base.dir=. -Ddist.dir=.
 * 5. (Optional) Delete files and directories in jython-src except for Lib.
 * 6. Build this program and run.
 *   make run_embed
 */
public class Embed {
  public static void main(String[] args) {
    Properties properties = new Properties();
    properties.setProperty("python.cachedir.skip", "true");
    properties.setProperty("python.home", "jython-src");

    PythonInterpreter.initialize(System.getProperties(),
                                 properties,
                                 new String[]{});
    PythonInterpreter inter = new PythonInterpreter();
    inter.exec("import sys;print sys.path");
    inter.exec("import datetime;print datetime.datetime.now()");
    inter.exec("import os;print os.getlogin()");
    inter.exec("print map(lambda x: x * 2, range(5))");
  }
}
