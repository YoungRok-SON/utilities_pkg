from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    bridge_args = [
        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',

        '/d435i/rgb/image@sensor_msgs/msg/Image@gz.msgs.Image',
        '/d435i/rgb/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',

        '/d435i/depth/image@sensor_msgs/msg/Image@gz.msgs.Image',
        '/d435i/depth/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',

        # Point cloud emitted directly by the gz depth_camera sensor
        # (published at <depth topic>/points = /d435i/depth/image/points).
        '/d435i/depth/image/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked',

        # IR stereo pair for stereo-inertial VINS (mimics real D435i infra1/infra2)
        '/d435i/infra1/image@sensor_msgs/msg/Image@gz.msgs.Image',
        '/d435i/infra2/image@sensor_msgs/msg/Image@gz.msgs.Image',

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

            # Depth point cloud -> topic ego-planner grid_map subscribes to
            # (grid_map/cloud is remapped to drone_0_pcl_render_node/depth/points)
            ('/d435i/depth/image/points', '/drone_0_pcl_render_node/depth/points'),

            # IR stereo pair
            ('/d435i/infra1/image', '/infra1/image'),
            ('/d435i/infra2/image', '/infra2/image'),

            # IMU
            ('/d435i/imu', '/imu'),
        ],
        parameters=[
            {'use_sim_time': True},
        ],
    )

    # NOTE: map->odom static TF intentionally REMOVED.
    # The SLAM/odometry source (VINS-Fusion or RTAB-Map) now owns map->odom;
    # publishing a second static map->odom here corrupts the TF tree.
    # Re-enable a static identity map->odom ONLY for bridge-only / sensor-test
    # runs where no SLAM node is providing it.

    return LaunchDescription([
        gz_bridge,
    ])
