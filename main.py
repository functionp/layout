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
    optimization_app = wx.App()
    optimization_frame = OptimizationFrame(None, -1, u'optimization', pos=(400,100))

    specification = Specification.load_specification("sample.dat")

    #layout = specification.get_default_layout()

    optimization = OCSOptimization(specification, specification.default_layout)

    objective_value_before = optimization.get_objective_value()
    print "Optimization Value Before:"
    print objective_value_before

    #optimization.optimize()
    optimized_layout = optimization.agent_set
    optimized_layout.render(optimization_frame.base_panel)

    objective_value = optimization.get_objective_value()
    print "Optimization Value After:"
    print objective_value

    optimization_frame.Show()

    optimization_app.MainLoop()

if __name__ == '__main__':
    main()


