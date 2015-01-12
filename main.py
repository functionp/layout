#-*- coding: utf-8 -*-
# imports - - - - - - -
import wx
import time
from agent import *
from specification import *
from optimization import *
from layout import *

WINDOW_SIZE = (1200,900)

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

def main():
    main_app = wx.App()
    main_frame = MainFrame(None, -1, u'controller', pos=(100,100),size=(260,300))

    child_panel = wx.Panel(main_frame.base_panel, wx.ID_ANY, pos=(30,30), size=(200,200))

    start_button = wx.Button(child_panel, wx.ID_ANY, "Start")
    start_button.Bind(wx.EVT_BUTTON, click_start_button)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(start_button)
    child_panel.SetSizer(sizer)

    main_frame.Show()

    main_app.MainLoop()

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


