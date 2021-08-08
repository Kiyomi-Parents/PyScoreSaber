import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyScoreSaber",
    version="0.0.3",
    author="LuCkEr-",
    author_email="lucker@lucker.xyz",
    description="Score Saber API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kiyomi-Parents/PyScoreSaber",
    project_urls={
        "Bug Tracker": "https://github.com/Kiyomi-Parents/PyScoreSaber/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "python-dateutil",
        "OutCache"
    ]
)
