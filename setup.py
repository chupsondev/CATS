from setuptools import setup

setup(
    name='CATS',
    version='0.1.0',
    description='Competitive Algorithms Tool Set (CATS) - a small set of tools, empowering people practicing for competitive programming competitions',
    url='https://github.com/chupsondev/CATS',
    author='chupson',
    author_email='chupson@chupson.dev',
    license='MIT',
    packages=['cats', 'cats.commands', 'cats.generators'],
    install_requires=['requests',
                      'requests_toolbelt',
                      ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'cats = cats:main',
        ],
    }
)