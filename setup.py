from setuptools import setup, find_packages

def get_requirements():
    with open('src/requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(
    name='flongo_framework',
    version='0.3.0',
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=get_requirements(),
    author='Peter Swanson',
    author_email='pswanson@ucdavis.edu',
    description='Flask framework with out of the box Logging, MongoDB, JWT, CORs, Sentry and Docker support',
    license='LICENSE',
    url='https://github.com/Topazoo/Flongo-Framework',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
