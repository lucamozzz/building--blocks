from setuptools import setup

package_name = 'ros_engine'
submodules = 'ros_engine/hardware'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, submodules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/no_control.launch.py']),
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
            'move = ros_engine.move:setup',
            'led = ros_engine.led_controller:setup',
            'ultrasonic = ros_engine.ultrasonic:setup',
            'battery = ros_engine.battery:setup',
            'odometry = ros_engine.odometry:setup',
            
        ],
    },
)
