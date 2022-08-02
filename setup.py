import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncbooru",
    version="0.0.6",
    author="Nick80835",
    author_email="nick80835@gmail.com",
    description="An async library for interfacing with Danbooru and similar websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nick80835/asyncbooru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp"],
    python_requires='>=3.6'
)
