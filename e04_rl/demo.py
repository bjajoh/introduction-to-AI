from vpython import *

scene.width = 1600
scene.height = 900

#    Cliffworld environment
#
#    states:
#        +--+--+--+--+--+--+--+--+--+--+--+--+
#        | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|
#        +--+--+--+--+--+--+--+--+--+--+--+--+
#        |12|13|14|15|16|17|18|19|20|21|22|23|
#        +--+--+--+--+--+--+--+--+--+--+--+--+
#        |24|25|26|27|28|29|30|31|32|33|34|35|
#        +--+--+--+--+--+--+--+--+--+--+--+--+
#        |36|37|38|39|40|41|42|43|44|45|46|47|
#        +--+--+--+--+--+--+--+--+--+--+--+--+
#    
#    actions:
#        a = 0 -> top
#        a = 1 -> down
#        a = 2 -> left
#        a = 3 -> right

width  = 3
length = 12

state = 47
action = 2
episode = 3

state_y = int(state/length)
state_x = state-length*state_y

print(state_x, state_y)

episode_text = text(text=f"Episode: {episode}", pos=vec(0,5,0), align='center', height=.7, color=color.white, billboard=True, emissive=True)


field       = box(pos=vec(0,0,0), length=length, height=2, width=width, color=color.green)
goal        = box(pos=vec((length/2)-0.5,0,((width/2)+0.5)), length=1, height=2, width=1, color=color.green)
goal_text   = text(text='Goal', pos=vec((length/2)-1,1,((width/2)+1.5)), align='center', height=0.5, color=color.yellow, billboard=True, emissive=True)
start       = box(pos=vec(-((length/2)-0.5),0,((width/2)+0.5)), length=1, height=2, width=1, color=color.green)
start_text  = text(text='Start', pos=vec(-((length/2)-1),1,((width/2)+1.5)), align='center', height=0.5, color=color.yellow, billboard=True, emissive=True)
ground      = box(pos=vec(0,-.9,((width/2)+0.5)), length=length-2, height=.2, width=1, color=color.red)
wall_back   = box(pos=vec(0,1,-((width/2)+0.5)), length=length, height=4, width=1, color=color.white)
wall_start  = box(pos=vec(-((length/2)+0.5),1,0), length=1, height=4, width=width+2, color=color.white)
wall_goal   = box(pos=vec(((length/2)+0.5),1,0), length=1, height=4, width=width+2, color=color.white)
agent       = cylinder(pos=vec(state_x-5.5,1,-1+state_y), radius=0.3, axis=vec(0,1.5,0), color=color.blue)

#agent.pos=vec(state_x,1,-1+state_y)

if action == 0:
  pointer = arrow(pos=vec(state_x-5.5,1.7,-1+state_y), axis=vector(0,0,-1), shaftwidth=0.2, color=color.blue)
elif action == 1:
  pointer = arrow(pos=vec(state_x-5.5,1.7,-1+state_y), axis=vector(0,0,1), shaftwidth=0.2, color=color.blue)
elif action == 2:
  pointer = arrow(pos=vec(state_x-5.5,1.7,-1+state_y), axis=vector(-1,0,0), shaftwidth=0.2, color=color.blue)
elif action == 3:
  pointer = arrow(pos=vec(state_x-5.5,1.7,-1+state_y), axis=vector(1,0,0), shaftwidth=0.2, color=color.blue)