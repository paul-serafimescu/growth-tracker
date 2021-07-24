import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "growth-tracker",
  version = "0.1.0",
  author = "Paul Serafimescu",
  author_email = "paulserafimescu@gmail.com",
  description = "see how a discord server changes over time idk",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/PaulSera1/growth-tracker",
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  packages = setuptools.find_packages(where = "."),
  python_requires = ">=3.8",
)
