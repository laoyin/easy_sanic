# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


def do_setup():
    setup(
        name='easy_sanic',
        description='easily build sanic project, powerful orm and restful',
        license='',
        version='0.0.2',
        packages=find_packages(where='src',exclude=['tests*', '*.pyc']),
        include_package_data=True,
        package_dir={'': 'src'},
        zip_safe=False,
        scripts=[],
        install_requires=[
            "sanic==0.8.3",
            "PyJWT==1.7.1",
            "requests==2.21.0",
            "aioredis==1.2.0",
            "opentracing==2.0.0",
            "asyncpg==0.18.3",
            "aiohttp==3.5.4"
        ],
        setup_requires=[
        ],
        extras_require={
        },
        classifiers=[
        ],
        author='yinxingpan',
        author_email='yinxingpan@163.com',
        url='https://github.com/laoyin/easy_sanic',
        download_url=(),
        cmdclass={
            'extra_clean': CleanCommand,
        },
    )


if __name__ == "__main__":
    do_setup()


