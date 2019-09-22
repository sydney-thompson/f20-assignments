#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
# add any other python modules that you need here ...

# define joint positions per pose
poses_list = [
   {'joint_1': 0, 'joint_2': 0, 'joint_3': 0, 'joint_4': 0},
   {'joint_1': 0, 'joint_2': -0.95, 'joint_3': 0.41, 'joint_4': -1},
   {'joint_1': 0, 'joint_2': -1.45, 'joint_3': 1.45, 'joint_4': -1.53}
]

def pose_switcher():
    # Define publishers and init your node here.
    joints = poses_list[0].keys()
    pubs = {}
    for k in joints:
        pubs[k] = rospy.Publisher('/{}/command'.format(k), Float64, queue_size=5)

    rospy.init_node('switch_poses', anonymous=True)

    # Add a loop to request the robot to move its joints according to the 
    # desired poses and at a constant rate.
    rate = rospy.Rate(1.0/5)
    current_pose = 0
    while not rospy.is_shutdown():
        for k in joints:
            pubs[k].publish(poses_list[current_pose][k])
            rospy.loginfo("Published pose {} - {}".format(current_pose, k))
        current_pose = (current_pose + 1)%len(poses_list)
        rate.sleep()

if __name__ == '__main__':
   try: 
       pose_switcher()
   except rospy.ROSInterruptException:
       pass
