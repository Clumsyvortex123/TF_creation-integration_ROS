import rospy
import tf
from shutil import move
import sys
import copy 
import rospy
import moveit_commander
from geometry_msgs.msg import Pose
import moveit_msgs.msg
import geometry_msgs.msg

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

            # Extract translation and rotation components and store them in variables
            x, y, z = trans
            qx, qy, qz, qw = rot  # Quaternion components

            # Print the translation and rotation
            print("Translation (x, y, z):", x, y, z)
            print("Rotation (x, y, z, w):", qx, qy, qz, qw)
            
            

            moveit_commander.roscpp_initialize(sys.argv)

            #setup scene for robot
            robot = moveit_commander.RobotCommander()
            scene = moveit_commander.PlanningSceneInterface()
            group = moveit_commander.MoveGroupCommander('manipulator')
            
            #configuration setup
            group.set_goal_position_tolerance(0.05)

            #self.group.set_planner_id('RRTConnectkConfigDefault')

            group.set_planning_time(5)
            group.set_num_planning_attempts(5)

            #applying ready status
            status = 0

            waypoints = []

            wpose = group.get_current_pose().pose
            # wpose.position.y -= scale * 0.3  # First move up (z)
            # waypoints.append(copy.deepcopy(wpose))
            # Define the orientation of the end-effector (you may need to adjust this)
            orientation = geometry_msgs.msg.Quaternion()
            orientation.x = qx
            orientation.y = qy
            orientation.z = qz
            orientation.w = qw
            wpose.orientation = orientation
            waypoints.append(copy.deepcopy(wpose))
            
            #a
            wpose.position.x = x
            wpose.position.y = y
            wpose.position.z = z

            waypoints.append(copy.deepcopy(wpose))
            print(waypoints)
        

            (plan, fraction) = group.compute_cartesian_path(
                waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
                
            )  
            print(fraction)
        
            group.execute(plan, wait=True)









            
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
