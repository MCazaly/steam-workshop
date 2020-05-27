from setuptools import setup


setup(
    name="Example Python Package",
    version="0.0.1",
    description="A package to scrape Collection information from the Steam Workshop.",
    url="https://github.com/Fakas/steam-workshop",
    author="Matthew Cazaly",
    packages=["steam_workshop"],
    install_requires=["requests", "beautifulsoup4"],
    include_package_data=True,
)
