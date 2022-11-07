# multibot-paramater-startup
## Reason
I was working on a project and had issues with starting up several subscriptions and publishers for various robots in one context. 
I came up with a solution to this issue that I had not encountered on forums or other multi-robot setups before.  

This method puts the subscriber and publisher into a single class. This makes it so that each class can subscribe and publish within its namespaces for each robot. This allows for accessing the robot positions and other functions from an array context. 

## Test
This can be tested by running this node as a python file while there is an active roscore running. 
After that, in another terminal you can run the list command to see what nodes are active. 
```bash 
rostopic list
```

You should see multiple sets of topics in the list. With an empty node the topic should look like: 
```bash
/robot_0/cmd_vel
/robot_0/move_base/result
/robot_0/move_base_simple/goal
/robot_0/odom
/robot_1/cmd_vel
/robot_1/move_base/result
/robot_1/move_base_simple/goal
/robot_1/odom
/robot_2/cmd_vel
/robot_2/move_base/result
/robot_2/move_base_simple/goal
/robot_2/odom
/robot_3/cmd_vel
/robot_3/move_base/result
/robot_3/move_base_simple/goal
/robot_3/odom
/robot_4/cmd_vel
/robot_4/move_base/result
/robot_4/move_base_simple/goal
/robot_4/odom
/rosout
/rosout_agg
```
