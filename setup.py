from distutils.core import setup
import setuptools

setup(
    name="turkishnlp",
    version="0.0.6",
    packages=['turkishnlp'],
    description="A python script that processes Turkish language",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/MeteHanC/turkishnlp",
    author="Metehan Cetinkaya",
    author_email="metehancet@gmail.com",
    maintainer="Metehan Cetinkaya",
    maintainer_email="metehancet@gmail.com",
    keywords=['turkishnlp', 'python', 'nlp', 'language processing'],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
