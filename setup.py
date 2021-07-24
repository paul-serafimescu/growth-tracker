import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "terminal-message",
  version = "0.1.0",
  author = "Paul Serafimescu",
  author_email = "paulserafimescu@gmail.com",
  description = "tool to automate backing up discord friends",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/PaulSera1/discord-friends-backup",
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  packages = setuptools.find_packages(where = "."),
  python_requires = ">=3.5",
)
