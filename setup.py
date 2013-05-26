from distutils.core import setup

classifiers = [
    'Topic :: Communications :: Chat :: Internet Relay Chat',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ]

setup(
    name='Yapil',
    description='Yet another python IRC lib'
    version='0.1dev',
    url='https://github.com/C4ptainCrunch/yapil/',
    author='Nikita Marchant',
    author_email='nikita.marchant@gmail.com',
    maintainer='Nikita Marchant',
    maintainer_email='nikita.marchant@gmail.com',
    packages=['yapil',],
    license='AGPLv3+ : GNU Affero General Public License version 3 or later',
    long_description=open('README.rst').read(),
    install_requires=["spool >= 0.0.1",],
    classifiers=classifiers,
)