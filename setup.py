from setuptools import setup

setup(
    name='django-webmoney-merchant',
    version=__import__('webmoney_merchant').__version__,
    description='WebMoney Merchant Interface for Django.',
    author='Evstropov Nikita',
    author_email='evstropov.n@gmail.com',
    url='https://github.com/evstropov/django-webmoney_merchant-merchant',
    packages=['webmoney_merchant'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.7",
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
