"""
TRIGNUM-300M: Subtractive Semantic Geometry for Cold-State AGI
"""

from setuptools import setup, find_packages

setup(
    name="trignum-300m",
    version="0.300.0",
    author="Trace on Lab",
    author_email="sovereign@traceonlab.ai",
    description="Subtractive Semantic Geometry for Cold-State AGI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trace-on-lab/trignum-300m",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="trignum magnetic-trillage subtractive-geometry cold-state agi",
)
