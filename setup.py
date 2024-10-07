from setuptools import setup, find_packages

setup(
    name='ffmpeg-gmic-plus',
    version='0.1.0',
    description="Use G'MIC plugins with ffmpeg (finally!) thanks to the wonderful ffmpeg-python and gmic for Python. A useful high-level feature ensures correct integer size after float scaling.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='7557867+poikilos@users.noreply.github.com',
    url='https://github.com/Hierosoft/ffmpeg-gmic-plus',
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
            'ffmpeg-gmic = ffmpeggmicplus.main:main',
        ],
    },
)
