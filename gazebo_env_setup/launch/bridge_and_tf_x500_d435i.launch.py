from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    bridge_args = [
        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',

        '/d435i/rgb/image@sensor_msgs/msg/Image@gz.msgs.Image',
        '/d435i/rgb/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',

        '/d435i/depth/image@sensor_msgs/msg/Image@gz.msgs.Image',
        '/d435i/depth/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',

        '/d435i/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
    ]

    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_ros_bridge_x500_d435i',
        output='screen',
        arguments=bridge_args,
        remappings=[
            # RGB
            ('/d435i/rgb/image', '/rgb_camera'),
            ('/d435i/rgb/camera_info', '/camera_info'),

            # Depth
            ('/d435i/depth/image', '/depth_camera'),
            ('/d435i/depth/camera_info', '/depth_camera/camera_info'),

            # IMU
            ('/d435i/imu', '/imu'),
        ],
        parameters=[
            {'use_sim_time': True},
        ],
    )

    # map → odom (static)
    tf_map_to_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_map_to_odom',
        output='screen',
        arguments=[
            '0', '0', '0',
            '0', '0', '0',
            'map',
            'odom',
        ],
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        gz_bridge,
        tf_map_to_odom,
    ])
