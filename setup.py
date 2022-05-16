from typing import Optional

import setuptools

# Get version info
__version__: Optional[str] = None
exec(open('src/pyscoresaber/version.py').read())

if __version__ is None:
    raise RuntimeError("Failed to get version!")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Requirements
requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements += f.read().splitlines()

extras_require = {
    'test': [
        'coverage',
        'pytest',
        'pytest-asyncio',
        'pytest-cov'
    ]
}

setuptools.setup(
    name="PyScoreSaber",
    version=__version__,
    author="LuCkEr-",
    author_email="lucker@lucker.xyz",
    description="Score Saber API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kiyomi-Parents/PyScoreSaber",
    project_urls={
        "Bug Tracker": "https://github.com/Kiyomi-Parents/PyScoreSaber/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extras_require,
)
