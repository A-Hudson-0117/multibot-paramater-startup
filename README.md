# multibot-paramater-startup

I was working on a project and had issues with starting up several subscriptions and publishers for various robots in one context. 
I came up with a solution to this issue that I had not seen before. 

It puts the subscriber and publisher into a class. This makes it so that each class can subscribe and publish within its namespaces for each robot.  
