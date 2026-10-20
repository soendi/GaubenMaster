from setuptools import setup, find_packages
import os

# Version aus version.json lesen
import json
with open('version.json', 'r') as f:
    version_data = json.load(f)
    VERSION = version_data['version']

# README lesen
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Requirements lesen
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="triangle-calculator",
    version=VERSION,
    author="Ihr Name",
    author_email="ihre.email@example.com",
    description="Dreiecksberechnung und -visualisierung mit 3 Seitenlängen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IHR_USERNAME/TriangleCalculator",
    project_urls={
        "Bug Tracker": "https://github.com/IHR_USERNAME/TriangleCalculator/issues",
        "Documentation": "https://github.com/IHR_USERNAME/TriangleCalculator#readme",
        "Source Code": "https://github.com/IHR_USERNAME/TriangleCalculator",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "flake8>=6.0",
            "black>=23.0",
            "mypy>=1.0",
            "pyinstaller>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "triangle-calculator=main:main",
        ],
        "gui_scripts": [
            "triangle-calculator-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["version.json"],
    },
    zip_safe=False,
)