from setuptools import setup, find_packages

setup(
    name="PyFlexAPI",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["boto3", "botocore", "moto"],
    include_package_data=True,
    license="MIT",
    description="A client for handling requests to Amazon DynamoDB.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Eric Macedo, Carlos Eduardo Yuichi Hashimoto",
    author_email="ericthr42@gmail.com, yuichihashimotobiz@gmail.com",
    url="https://github.com/ericDK89/PyFlexAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
