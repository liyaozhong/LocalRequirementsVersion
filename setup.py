from setuptools import setup, find_packages

setup(
    name='LocalRequirement',
    version='0.1.1',
    author="liyaozhong",
    author_email="yun.zhongyue@163.com",
    packages=find_packages(),
    install_requires=[
        "setuptools",
    ],
    entry_points={
        'console_scripts': [
            'LocalRequirement=local_requirement.local_requirement:main',
        ],
    },
    description="A tool to update requirements.txt with locally installed package versions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/liyaozhong/LocalRequirementsVersion",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)