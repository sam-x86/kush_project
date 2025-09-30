# kush-framework/setup.py
from setuptools import setup, find_packages

setup(
    name="kush-framework",
    version="3.0.0",
    description="Empire-inspired Penetration Testing Framework",
    author="Kush Team",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "cryptography>=3.4",
        "requests>=2.25",
        "pyyaml>=5.4",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'kush=kush.main:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)