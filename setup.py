"""Setup script para VulnLab Scanner."""
from setuptools import setup, find_packages

setup(
    name="vulnlab-scanner",
    version="1.4.3",
    author="VulnLab Team",
    author_email="contact@vulnlab.com",
    description="Herramienta profesional de escaneo de vulnerabilidades web basada en OWASP Top 10",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.0",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "vulnlab-scan=app.cli:main",
        ],
    },
)
