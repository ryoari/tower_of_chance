from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tower_of_chance",
    version="1.0.0",
    author="ryoar",
    author_email="your.email@example.com",  # Replace with your email
    description="A colorful, modular game of luck and skill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tower_of_chance",  # Replace with your repo URL
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "tower_of_chance": ["challenges.json", "tower_config.json"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust based on your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "tower-of-chance=tower_of_chance:main",
        ],
    },
)