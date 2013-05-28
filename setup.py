from distutils.core import setup
from pip.req import parse_requirements

classifiers = [
    'Topic :: Communications :: Chat :: Internet Relay Chat',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ]

parsed_req = parse_requirements("requirements.txt")

requirements =  []
dependency_links = []

for item in parsed_req:
    if item.url:
        uri = "{}#egg={}".format(item.url,item.req)
        dependency_links.append(uri)
        req = '-'.join(str(item.req).split('-')[:-1])
        requirements.append(req)
    else:
        requirements.append(str(item.req))


setup(
    name='Yapil',
    description='Yet another python IRC lib',
    version='0.2dev',
    url='https://github.com/C4ptainCrunch/yapil/',
    author='Nikita Marchant',
    author_email='nikita.marchant@gmail.com',
    maintainer='Nikita Marchant',
    maintainer_email='nikita.marchant@gmail.com',
    packages=['yapil'],
    license='AGPLv3+ : GNU Affero General Public License version 3 or later',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    dependency_links=dependency_links,
    classifiers=classifiers,
)