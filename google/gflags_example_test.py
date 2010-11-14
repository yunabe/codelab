import commands
import os
import sys
import unittest


class TestGflagsCppProgram(unittest.TestCase):
  def testDefault(self):
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example'))

  def testHelp(self):
    helpOutput = commands.getoutput('./gflags_example --help')
    self.assertTrue('-name (Username. Says hello to this user.) '
                    'type: string default: "world"' in helpOutput)

  def testFlags(self):
    self.assertEqual('Hello foo.',
                     commands.getoutput('./gflags_example --name=foo'))
    self.assertEqual('Hello foo.',
                     commands.getoutput('./gflags_example --name foo'))
    self.assertEqual('Hello foo.',
                     commands.getoutput('./gflags_example -name=foo'))
    self.assertEqual('Hello foo.',
                     commands.getoutput('./gflags_example -name foo'))

  def testBoolFlag(self):
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example --overwrite_name'))

  def testPositiveBoolExpressions(self):
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=true'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=yes'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=t'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=y'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=1'))

  def testNegativeBoolExpressions(self):
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=false'))
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=no'))
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=f'))
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=n'))
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=0'))

  def testBoolFlagWithNo(self):
    # --no<bool_flag> works as --<bool_flag>=false
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example --nooverwrite_name'))
    # The value for --no<bool_flag> seems to be ignored,
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--nooverwrite_name=true'))
    self.assertEqual('Hello world.',
                     commands.getoutput('./gflags_example '
                                        '--nooverwrite_name=false'))

  def testBoolFlagCaseInsensitive(self):
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=T'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=Y'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=tRue'))
    self.assertEqual('Hello %s.' % os.getlogin(),
                     commands.getoutput('./gflags_example '
                                        '--overwrite_name=yEs'))

  def testFlagValidator(self):
    self.assertEqual('Hello 0123456789.',
                     commands.getoutput('./gflags_example '
                                        '--name=0123456789'))
    output = commands.getoutput('./gflags_example '
                                '--name=01234567890')
    self.assertTrue('Value for --name: 01234567890 is too long.' in output)


if __name__ == '__main__':
  unittest.main()
