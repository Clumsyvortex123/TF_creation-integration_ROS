import rospy
import tf

def get_frame_coordinates():
    # Initialize the ROS node
    rospy.init_node('get_frame_coordinates', anonymous=True)

    # Create a TF listener
    tf_listener = tf.TransformListener()

    while not rospy.is_shutdown():
        try:
            # Prompt the user for the frame name
            frame_name = input("Enter the name of the frame to retrieve coordinates (Ctrl+C to exit): ")

            # Get the transform from the base frame (e.g., "base_link") to the specified frame
            tf_listener.waitForTransform("base_link", frame_name, rospy.Time(), rospy.Duration(4.0))
            (trans, rot) = tf_listener.lookupTransform("base_link", frame_name, rospy.Time())

            # Print the translation and rotation
            print("Translation (x, y, z):", trans)
            print("Rotation (x, y, z, w):", rot)
        
        except tf.LookupException as e:
            print("TF Lookup Exception:", e)
        except tf.ConnectivityException as e:
            print("TF Connectivity Exception:", e)
        except tf.ExtrapolationException as e:
            print("TF Extrapolation Exception:", e)
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    try:
        get_frame_coordinates()
    except rospy.ROSInterruptException:
        pass
