# simple state example for Memory
import random
import simplegui
     
# define event handlers
def new_game():
    global state, turns, numbers, exposed, guess_1, guess_2, matched, wrong, winner,card_colors,width,height
    state = 0
    turns=0
    numbers = [i%tot_numbers//2 for i in range(tot_numbers)]
    winner="    YOU WON!    "
    random.shuffle(numbers)
    exposed = [False for i in range(tot_numbers)]
    matched = [False for i in range(tot_numbers)]
    label.set_text("Turns = " +str(turns))
    card_colors=["blue","purple"]
    click_1=0
    click_2=0

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turns, numbers, exposed, guess_1, guess_2
    
    guess=int(pos[0]/(width/tot_numbers))

    if state == 0:
        state = 1
        guess_1=guess
        exposed[guess_1]=True
        
    elif state == 1:
        if not exposed[guess]:
            state = 2
            guess_2=guess
            exposed[guess_2]=True
            turns+=1
        
    elif state == 2:
        if matched.count(True)> tot_numbers-3:
            matched[guess_1] = True
            matched[guess_2] = True
            mouseclick
            
        else:
            if not exposed[guess]:
                if numbers[guess_1] == numbers[guess_2]:
                    matched[guess_1] = True
                    matched[guess_2] = True   
                    pass
                else:
                    exposed[guess_1] = False
                    exposed[guess_2] = False
                guess_1 = guess
                exposed[guess_1] = True
                state = 1      
            
    label.set_text("Turns = " + str(turns))

       
                         
def draw(canvas):
        for i in range(tot_numbers):

            if exposed[i]:
                canvas.draw_polygon([(cell_width*i, height/2),(cell_width*i+cell_width/2, height), (cell_width*i+cell_width, height/2),(cell_width*i + cell_width/2, 0)], 4, "White", card_colors[i%2])
                canvas.draw_text(str(numbers[i]), (cell_width*i+cell_width/4, height*.6), height/2.2, "White")

            else:
                canvas.draw_polygon([(cell_width*i, height/2),(cell_width*i+cell_width/2, height), (cell_width*i+cell_width, height/2),(cell_width*i + cell_width/2, 0)], 4, "White", "grey")

            if matched[i]:
                canvas.draw_polygon([(cell_width*i, height/2),(cell_width*i+cell_width/2, height), (cell_width*i+cell_width, height/2),(cell_width*i + cell_width/2, 0)], 4, "White", "green")
                canvas.draw_text(str(numbers[i]), (cell_width*i+cell_width/4, height*.6), height/2.2,  "White")
                if matched.count(True)==tot_numbers:
                    for i in range(tot_numbers):
                        canvas.draw_polygon([(cell_width*i, height/2),(cell_width*i+cell_width/2, height), (cell_width*i+cell_width, height/2),(cell_width*i + cell_width/2, 0)], 4, "Red", "pink")
                        canvas.draw_text(str(winner[i]), (cell_width*i+cell_width/4, height*.6), height/2.2, "White")
        pass
        
width=700
height=100
tot_numbers=14
cell_width=(width/tot_numbers)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory states", width, height)
frame.add_button("Restart", new_game, 150)
#frame.add_button("Simulate mouse click", buttonclick, 200)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
