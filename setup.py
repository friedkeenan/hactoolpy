import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="hactoolpy",
    version="0.0.1",
    author="friedkeenan",
    description="A library for reading file formats used by the Nintendo Switch OS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/friedkeenan/hactoolpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)