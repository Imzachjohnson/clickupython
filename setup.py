import setuptools

with open('DESCRIPTION.md', 'r') as readme:
  long_description = readme.read()

with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
      name='clickupy',
      version='1.0',
      description='A client for working with the ClickUp API V2',
      url='https://github.com/Imzachjohnson/clickupy',
      author='Zach Johnson',
      author_email='imzachjohnson@gmail.com',
      license='GPL-3.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=requirements
)