#-*- coding: utf-8 -*-
# imports - - - - - - -
import wx
import time
from agent import *
from specification import *
from optimization import *
from layout import *

WINDOW_SIZE = (1200,900)
MAIN_WINDOW_SIZE = (900,550)
MAIN_PADDING = (30,30)

g_current_box = None
g_main_frame = None

class OptimizationFrame(wx.Frame):

    def __init__(self, parent=None, id=-1, title=None, *args, **kwargs):
        wx.Frame.__init__(self, parent, id, title,*args, **kwargs)

        self.SetBackgroundColour("#ffffff")
        self.SetSize(WINDOW_SIZE)

        self.base_panel = wx.Panel(self, wx.ID_ANY)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(50)

    # the method which runs at regular interval
    def on_timer(self, event):
        pass
        #self.move()

    def move(self):
        present_x, present_y = self.child_panel1.GetPosition()

        self.child_panel1.SetPosition((present_x + 1, present_y + 1))
        self.child_panel1.Update()

class MainFrame(wx.Frame):

    def __init__(self, parent=None, id=-1, title=None, *args, **kwargs):
        wx.Frame.__init__(self, parent, id, title, *args, **kwargs)

        self.base_panel = wx.Panel(self, wx.ID_ANY)

def get_agent_list(box):
    if box.inner_layout:
        return [agent.identifier for agent in box.inner_layout.agents]
    else:
        return []

def reflesh_main(target_box):
    def get_right_position(basic_object, margin):
        basic_x, basic_y = basic_object.Position
        basic_width, basic_height = basic_object.Size
        return [basic_x + basic_width + margin, basic_y]
        
    def get_bottom_position(basic_object, margin):
        basic_x, basic_y = basic_object.Position
        basic_width, basic_height = basic_object.Size
        return [basic_x, basic_y + basic_height + margin]

    main_panel = wx.Panel(g_main_frame.base_panel, wx.ID_ANY, pos=MAIN_PADDING, size=(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1]))

    list_box = wx.ListBox(main_panel, wx.ID_ANY, choices=get_agent_list(target_box), style=wx.LB_SINGLE, pos=(2,2), size=(150, 300))

    label_map = wx.StaticText(main_panel, wx.ID_ANY, target_box.identifier, pos=get_right_position(list_box, 10))

    label_name = wx.StaticText(main_panel, wx.ID_ANY, "Name", pos=get_bottom_position(label_map, 10))
    text_name = wx.TextCtrl(main_panel,wx.ID_ANY, target_box.identifier, pos=get_right_position(label_name, 5))

    STYLE_TEXT_SIZE = (60,23)
    label_x = wx.StaticText(main_panel, wx.ID_ANY, "X", pos=get_bottom_position(label_name, 10))
    text_x = wx.TextCtrl(main_panel,wx.ID_ANY, str(target_box.get_x()) , pos=get_right_position(label_x, 5), size=STYLE_TEXT_SIZE)
    text_x.SetMaxLength(4)

    label_y = wx.StaticText(main_panel, wx.ID_ANY, "Y", pos=get_right_position(text_x, 20))
    text_y = wx.TextCtrl(main_panel,wx.ID_ANY, str(target_box.get_y()), pos=get_right_position(label_y, 5), size=STYLE_TEXT_SIZE)
    text_y.SetMaxLength(4)

    label_width = wx.StaticText(main_panel, wx.ID_ANY, "Width", pos=get_right_position(text_y, 20))
    text_width = wx.TextCtrl(main_panel,wx.ID_ANY, str(target_box.get_width()), pos=get_right_position(label_width, 5), size=STYLE_TEXT_SIZE)
    text_width.SetMaxLength(4)

    label_height = wx.StaticText(main_panel, wx.ID_ANY, "Height", pos=get_right_position(text_width, 20))
    text_height = wx.TextCtrl(main_panel,wx.ID_ANY, str(target_box.get_height()), pos=get_right_position(label_height, 5), size=STYLE_TEXT_SIZE)
    text_height.SetMaxLength(4)

    make_button = wx.Button(main_panel, wx.ID_ANY, "Make New Box", pos=get_bottom_position(label_x, 30))
    make_button.Bind(wx.EVT_BUTTON, click_make_button)

    start_button = wx.Button(main_panel, wx.ID_ANY, "Start", pos=get_right_position(make_button, 10))
    start_button.Bind(wx.EVT_BUTTON, click_start_button)

    g_main_frame.Show()
    wx.Yield() 


def main():
    global g_current_box
    global g_main_frame

    main_app = wx.App()
    g_main_frame = MainFrame(None, -1, u'controller', pos=(100,100),size=MAIN_WINDOW_SIZE)

    g_current_box =  BoxAgent(Style([0,0], WINDOW_SIZE, 0), "base")

    reflesh_main(g_current_box)
    main_app.MainLoop()

def click_make_button(event):
    global g_current_box
    new_box = BoxAgent(Style([0,0], [0,0], 1), "new box")
    Layout([new_box], g_current_box)

    g_current_box = new_box
    reflesh_main(new_box)

def click_start_button(event):
    def render_closure(layout):
        def _render_closure():
            layout.render(optimization_frame.base_panel)
            optimization_frame.Show()
            wx.Yield()
        return _render_closure

    def softplanner():
        #specification = SoftplannerSpecification()
        constraint1 = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned()], 1)

        base_layout = SoftplannerLayout()
        #base_optimization = OCSOptimization(specification, base_layout)

        header_menu_layout = base_layout.get_agent_with_identifier("header_inner_menu").inner_layout
        header_menu_specification = Specification(header_menu_layout, constraint1)
        header_menu_optimization = OCSOptimization(header_menu_specification, header_menu_layout)
        #header_menu_optimization.optimize()

        #global_menu_layout = base_layout.get_agent_with_identifier("global_inner_menu").inner_layout
        #global_menu_optimization = OCSOptimization(specification, global_menu_layout)
        #global_menu_optimization.optimize()

        #制約候補にエージェント制約追加してみた　中身どんなんか観察
        image_area_layout = base_layout.get_agent_with_identifier("image_area_inner").inner_layout
        image_area_specification = Specification(image_area_layout, constraint1)
        image_area_optimization = OCSOptimization(image_area_specification, image_area_layout)
        image_area_optimization.set_render_function(render_closure(base_layout))
        image_area_optimization.optimize()

        main_layout = base_layout.get_agent_with_identifier("main").inner_layout
        main_specification = Specification(main_layout, constraint1)
        main_optimization = OCSOptimization(main_specification, main_layout)
        #main_optimization.optimize()

        base_layout.render(optimization_frame.base_panel)

    optimization_app = wx.App()
    optimization_frame = OptimizationFrame(None, -1, u'optimization', pos=(400,100))

    softplanner()


    optimization_frame.Show()

    optimization_app.MainLoop()

if __name__ == '__main__':
    main()


