try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='np',
    version='0.9.1',
    description='Electricity infrastructure prototyping system',
    author='Roy Hyunjin Han',
    author_email='support@invisibleroads.com',
    url='http://october.mech.columbia.edu',
    install_requires=[
        "Pylons>=1.0",
        "recaptcha-client>=1.0.5",
        "SQLAlchemy>=0.6.3",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'np': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = np.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """)
