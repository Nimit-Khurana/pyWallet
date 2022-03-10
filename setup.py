from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'Licence :: OSI Approved :: MIT Licence',
	'Programming Language :: Python :: 3'
]

setup(
	name="pyWallet",
	version='0.1',
	description='save passwords and details',
	Long_description=open('README.txt').read()+open('CHANGELOG.txt').read(),
	url='',
	author='Nimit Khurana',
	author_email='nimitkhuranaa@gmail.com',
	Licence='MIT',
	classifiers=classifiers,
	keywords='passwordwallet',
	packages=find_packages(),
	install_requires=['']
