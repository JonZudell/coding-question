# coding-question
Hello thanks for taking a moment to look over what I've written up.

I've included two seperate examples one in lua and one in python with different approaches.
If I have enough free time I may include a minimalist command line java implementation and add some unit tests / additional functionality.

# LUA
For the LUA version I decided to use the https://love2d.org/ framework. 
I've been getting more into lua lately so I figured I'd take a crack at it and approach the problem from a desktop GUI point of view.
So you dont have to run it yourself I'll include images and explain how things behave.

The inital state.
![](https://i.imgur.com/YbTAukt.png)

When a cell is clicked it is highlighted
![](https://i.imgur.com/57P2S72.png )

Afterwards it gradually fades this is implemented as a glsl shader not because I needed to but because i thought it was cool
![](https://i.imgur.com/Vdscc5F.png)

Multiple cells selected gradually fade
![](https://i.imgur.com/MNlCaXe.png)


# Python
For the python version I decided to use my favorite web development framework Flask. 
I've temporarily hosted it at [jonscherwellinterview.com](http://www.jonscherwellinterview.com)

# TODOs
Unit test for flask
Select match type based on input
Add javascript and hit the json endpoints for progressive enhancement

