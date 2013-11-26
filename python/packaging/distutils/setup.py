from distutils.core import setup

setup(name='distutils-lab',
      version='1.0',
      url = 'https://github.com/yunabe/practice/tree/master/python',
      author = 'Yu Watanabe',
      author_email = 'yunabe.public@gmail.com',
      description = 'short description.',
      long_description = 'Long long long description.',
      py_modules=['foo', 'bar.baz', 'qux.foobar'],
      package_dir = {
          'qux': 'qux_dir',
          }
      )
