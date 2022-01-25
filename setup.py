from setuptools import setup, find_packages

with open('README.md', 'r') as input_file:
    long_description = input_file.read()

setup(
    name='python-ffmpeg',
    version='1.0.12',
    description='A python interface for FFmpeg',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jonghwanhyeon/python-ffmpeg',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='ffmpeg',
    packages=find_packages(),
    install_requires=['pyee'],
)
