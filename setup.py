import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'scarecrow_data',
    version = '0.0.4',
    author = 'Michael Hayman',
    author_email = 'mdghayman@gmail.com',
    description = 'Scarecrow offers low code web development for data science.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mdghayman/Scarecrow',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    python_required = '>=3.6')
