from setuptools import setup, find_packages

setup(
    name='moreffmpeg',
    version='0.1.0',
    description="Use G'MIC plugins with ffmpeg (finally!) using the wonderful ffmpeg-python and gmic for Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='7557867+poikilos@users.noreply.github.com',
    url='https://github.com/Hierosoft/moreffmpeg',
    packages=find_packages(),
    install_requires=[
        'ffmpeg-python',
        'gmic',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': [
            'moreffmpeg = moreffmpeg.main:main',
        ],
    },
)
