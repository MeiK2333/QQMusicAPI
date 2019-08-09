import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qqmusic-api",
    version="1.0.0",
    author="MeiK2333",
    author_email="meik2333@gmail.com",
    description="some api about qqmusic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MeiK2333/QQMusicAPI",
    packages=setuptools.find_packages(),
)
