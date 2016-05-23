from distutils.core import setup

setup(
    name='pylibratometrics',
    version='0.6',
    packages=['pylibratometrics',],
    license='MIT License',
    long_description=open('README.md').read(),
    author = "Ricardo Niederberger Cabral",
    author_email = "ricardo@isnotworking.com",
    description = "Simple script to send psutil (host network/cpu/disk) stats into Librato",
    download_url = 'https://github.com/digesto/pylibratometrics/tarball/0.6',
    keywords = "librato metrics",
    url = "https://github.com/digesto/pylibratometrics",
    install_requires = ["requests", "psutil"],
    entry_points={
        'console_scripts': [
            'pylibratometrics = pylibratometrics.pylibratometrics:main',
        ],
	}
)