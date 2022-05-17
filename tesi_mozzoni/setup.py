from setuptools import setup

package_name = 'tesi_mozzoni'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'car_controller = tesi_mozzoni.CarController:setup',
            'DetectObstacle = tesi_mozzoni.DetectObstacle:setup',
            'GoTo = tesi_mozzoni.GoTo:setup',
            'CheckBattery = tesi_mozzoni.CheckBattery:setup',
                        
            ],
    },
)
