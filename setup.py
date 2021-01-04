from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='domains-api',
    version='0.1.3.6',
    description='auto updates dynamic dns rules on domains.google.com',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nihilok/domains-api',
    author='Michael Jarvis',
    author_email='mjfullstack@gmail.com',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['requests']
)