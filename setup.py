import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
    name="osrs_botter", # Replace with your own username
    version="0.0.1",
    author="Alexander Nordin",
    author_email="alexander.f.nordin@gmail.com",
    description="Boots n stoofs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anordin95/replay_mouse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)