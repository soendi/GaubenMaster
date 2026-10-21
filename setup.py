from setuptools import setup
import os
import json

# Version aus version.json lesen
VERSION = "1.0.0"
version_path = os.path.join(os.path.dirname(__file__), "version.json")
if os.path.exists(version_path):
    with open(version_path, "r") as f:
        version_data = json.load(f)
        VERSION = version_data.get("version", "1.0.0")

# README lesen
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Requirements lesen
with open("requirements.txt", "r") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

setup(
    name="gaubenmaster",
    version=VERSION,
    author="soendi",
    author_email="soendi@users.noreply.github.com",
    description="Dreiecksberechnung und -visualisierung für Gaubenbau (3 Seitenlängen)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soendi/GaubenMaster",
    project_urls={
        "Bug Tracker": "https://github.com/soendi/GaubenMaster/issues",
        "Documentation": "https://github.com/soendi/GaubenMaster#readme",
        "Source Code": "https://github.com/soendi/GaubenMaster",
        "Releases": "https://github.com/soendi/GaubenMaster/releases",
    },
    py_modules=["main", "calculator", "gui", "plot", "update"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
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
            "gaubenmaster=main:main",
        ],
        "gui_scripts": [
            "gaubenmaster-gui=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
