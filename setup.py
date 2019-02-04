from setuptools import setup, find_packages

setup(
    name='python-ffmpeg',
    version='1.0.7',
    description='A python interface for FFmpeg',
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