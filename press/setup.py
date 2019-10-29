import setuptools

setuptools.setup(
    include_package_data=True,
    name="press",
    version="0.0.1",
    url="NaN",

    author="4t2",
    author_email="info@4t2.pw",

    description="press is a KISS reporting tool.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=['Jinja2', 'matplotlib', 'bokeh', 'markdown'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
