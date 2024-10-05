from setuptools import find_packages, setup
from typing import List

# Define a constant for the string '-e .' which is typically used in pip to install local packages.
HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements file and returns a list of dependencies.
    
    Args:
    file_path (str): Path to the requirements file.
    
    Returns:
    List[str]: A list of package dependencies without newline characters.
               If '-e .' is found, it is removed from the list as it is used 
               to signify local package installation.
    """
    requirements = []
    

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()

        requirements = [req.replace("\n", "") for req in requirements]
        
        # Remove '-e .' if it is present, as it's used for local installation.
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name='mlgenericproject',  
    version='0.0.1',  
    author='robin',  
    author_email='robinkphilip2001@gmail.com',  
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
