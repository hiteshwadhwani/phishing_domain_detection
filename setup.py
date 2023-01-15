from setuptools import find_packages, setup

REQUIREMENT_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = '-e .'

def get_requirements():
    with open(REQUIREMENT_FILE_NAME) as file:
        requirement_list = file.readlines()

    requirement_list = [l.replace("\n", "") for l in requirement_list]
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)

    return requirement_list

setup(
    name="phishing",
    version="0.0.1",
    author="hitesh",
    author_email="hiteshwadhwani1403@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements()
)