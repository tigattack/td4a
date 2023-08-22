from setuptools import setup

# gross.
with open('requirements.txt', 'r', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name='td4a',
    version='2.0.3',
    description='A browser based jinja template renderer',
    url='http://github.com/tigattack/td4a',
    author='Bradley A. Thornton (fork by tigattack)',
    license='MIT',
    include_package_data=True,
    packages=['src/td4a'],
    scripts=['src/td4a-server'],
    install_requires=required,
    zip_safe=False,
)
