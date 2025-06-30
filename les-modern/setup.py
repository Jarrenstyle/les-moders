#!/usr/bin/env python3
"""
LES-Modern Setup Script
========================
"""

from setuptools import setup, find_packages

with open("README_LES_MODERN.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="les-modern",
    version="3.0.0-beta",
    author="LES-Modern Team",
    author_email="contact@les-modern.com",
    description="Modern Linux Exploit Suggester - CVE 2024/2025 Compatible",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/les-modern",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "les-modern=main:main",
        ],
    },
    keywords="linux, exploit, suggester, cve, security, penetration-testing",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/les-modern/issues",
        "Source": "https://github.com/your-repo/les-modern",
        "Documentation": "https://github.com/your-repo/les-modern/wiki",
    },
) 