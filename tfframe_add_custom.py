import rospy
import tf2_ros
import geometry_msgs.msg

# Initialize the ROS node
rospy.init_node('add_tf_frames_to_simulation')

# Create a tf2_ros.TransformBroadcaster instance
tf_broadcaster = tf2_ros.TransformBroadcaster()

while not rospy.is_shutdown():
    # Prompt the user for frame details
    new_frame_name = input("Enter the name of the new TF frame (or 'exit' to quit): ")
    
    if new_frame_name.lower() == 'exit':
        break

    reference_frame_name = input("Enter the name of the reference frame (e.g., base_link): ")
    
    x = float(input("Enter X-coordinate: "))
    y = float(input("Enter Y-coordinate: "))
    z = float(input("Enter Z-coordinate: "))
    
    qx = float(input("Enter X quaternion value: "))
    qy = float(input("Enter Y quaternion value: "))
    qz = float(input("Enter Z quaternion value: "))
    qw = float(input("Enter W quaternion value: "))

    # Create a TransformStamped message
    transform_msg = geometry_msgs.msg.TransformStamped()
    transform_msg.header.stamp = rospy.Time.now()
    transform_msg.header.frame_id = reference_frame_name
    transform_msg.child_frame_id = new_frame_name
    transform_msg.transform.translation.x = x
    transform_msg.transform.translation.y = y
    transform_msg.transform.translation.z = z
    transform_msg.transform.rotation.x = qx
    transform_msg.transform.rotation.y = qy
    transform_msg.transform.rotation.z = qz
    transform_msg.transform.rotation.w = qw

    # Broadcast the transformation
    tf_broadcaster.sendTransform(transform_msg)

rospy.spin()  # This keeps the program running until ROS is shutdown
