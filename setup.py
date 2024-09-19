from setuptools import setup, find_packages

setup(
    name='LocalRequirement',
    version='0.1',
    author="liyaozhong",
    author_email="yun.zhongyue@163.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'LocalRequirement=local_requirement.local_requirement:main',
        ],
    },
    install_requires=[
        'setuptools',  # 这里改为 setuptools
    ],
)