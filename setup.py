from setuptools import setup

setup(
   name='WireBug',
   version='1.0',
   description='WireBug is a toolset for Voice-over-IP penetration testing ',
   license="MIT",
   long_description=open('README.md', 'r').read(),
   long_description_content_type='text/markdown',
   author='Moritz Abrell',
   author_email='moritz.abrell@syss.de',
   url="https://github.com/SySS-Research/WireBug",
   install_requires=[
    'pyshark', 
    'scapy' 
   ], 
   scripts=[
    'configure.sh',
   ]
)

