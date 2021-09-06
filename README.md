# PyPi Packaging Boilerplate

A client for working with the ClickUp API V2

## Instructions
### 1) Installing
- ```pip install clickupy```

### 2) Adding your code
- Insert your code into ```/package```
- Rename ```/package``` folder with your package's name
- Rename the package name in ```/package/__init__.py```
- Insert your package requirements in ```requirements.txt```

### 3) Configuring the build
- In ```setup.py```, follow the instructions in the comments:
```python
setuptools.setup(
      name='', # Insert your package name
      version='1.0',
      description='', # Change the description
      url='', # Change the repository url
      author='', # Insert your name
      author_email='', # Insert your email
      license='GPL-3.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=requirements
)
```
- To edit the long description of your package, write, in ```DESCRIPTION.md``` the markdown contents of your choice

### 4) Uploading to PyPi
- Simply run ```./updatepip.sh```