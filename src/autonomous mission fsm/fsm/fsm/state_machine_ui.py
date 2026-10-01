from ursina import *

app = Ursina()
def do_something_slider1():
    print("Slider1 value: ", slider1.value)
    
def do_something_slider2():
    print("Slider2 value: ", slider2.value)
    
def do_something_slider3():
    print("Slider3 value: ", slider3.value)
    
controls_box = Entity(parent=camera.ui, position = (0,-.3,0),model='quad', scale=(.7, .24), color=color.gray)
slider_scale = (1 / .7, 1 / .24, 1)
slider1 = Slider(parent=controls_box, position=(-.4, .28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=do_something_slider1, dynamic=True)
slider2 = Slider(parent=controls_box, position=(-.4, 0, -.01), scale=slider_scale, min=0, max=100, on_value_changed=do_something_slider2, dynamic=True)
slider3 = Slider(parent=controls_box, position=(-.4, -.28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=do_something_slider3, dynamic=True)

app.run()
