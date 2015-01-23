#-*- coding: utf-8 -*-
# imports - - - - - - -
import wx
import time
from agent import *
from specification import *
from optimization import *
from layout import *

WINDOW_SIZE = [1200,900]
MAIN_WINDOW_SIZE = (750,440)
MAIN_PADDING = (30,30)

g_main_frame = None
g_widgets = {}

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

def widget_factory(widget_class,parent,widget_id,*args,**kwargs):
    widget = widget_class(parent,widget_id,*args,**kwargs)
    g_widgets[widget_id] = widget
    return widget

def get_widget_by_id(widget_id):
    return g_widgets.get(widget_id, None)

def get_agent_list(box):
    if box.inner_layout:
        return [agent.identifier for agent in box.inner_layout.agents]
    else:
        return []

def get_map(box):
    if box.parent_layout:
        return get_map(box.parent_layout.base_box) + " > " + box.identifier
    else:
        return box.identifier


def get_right_position(basic_object, margin, y_adjustment=0):
    basic_x, basic_y = basic_object.Position
    basic_width, basic_height = basic_object.Size
    return [basic_x + basic_width + margin, basic_y + y_adjustment]

def get_bottom_position(basic_object, margin, x_adjustment=0):
    basic_x, basic_y = basic_object.Position
    basic_width, basic_height = basic_object.Size
    return [basic_x + x_adjustment, basic_y + basic_height + margin]

class MainFrame(wx.Frame):

    def __init__(self, current_box, parent=None, id=-1, title=None, *args, **kwargs):
        wx.Frame.__init__(self, parent, id, title, *args, **kwargs)

        self.base_panel = wx.Panel(self, wx.ID_ANY)
        self.set_current_box(current_box)
        self.set_base_box(current_box)
        self.refresh(self.current_box)

    def set_current_box(self, current_box):
        self.current_box = current_box

    def set_main_panel(self, main_panel):
        self.main_panel = main_panel

    def set_base_box(self, base_box):
        self.base_box = base_box

    def get_base_box(self):
        return self.base_box

    def render_box_options(self, target_box):
        ADJUST= 2
        main_panel = self.main_panel

        label_map = widget_factory(wx.StaticText, main_panel, 0, get_map(target_box), pos=get_right_position(get_widget_by_id(15), 20))

        label_name = widget_factory(wx.StaticText, main_panel, 6, "Name", pos=get_bottom_position(label_map, 10))
        text_name = widget_factory(wx.TextCtrl, main_panel, 1, target_box.identifier, pos=get_right_position(label_name, 5, -ADJUST), size=(240, 23))

        label_text = widget_factory(wx.StaticText, main_panel, 40, "Text", pos=get_bottom_position(label_name, 10))
        text_text = widget_factory(wx.TextCtrl, main_panel, 41, target_box.text, pos=get_right_position(label_text, 16, -ADJUST), size=(240, 23))

        STYLE_TEXT_SIZE = (50,23)
        label_x = widget_factory(wx.StaticText, main_panel, 7, "X", pos=get_bottom_position(label_text, 10))
        text_x = widget_factory(wx.TextCtrl, main_panel, 2, str(target_box.get_x()) , pos=get_right_position(label_x, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        text_x.SetMaxLength(4)

        label_y = widget_factory(wx.StaticText, main_panel, 8, "Y", pos=get_right_position(text_x, 20, ADJUST))
        text_y = widget_factory(wx.TextCtrl, main_panel, 3, str(target_box.get_y()), pos=get_right_position(label_y, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        text_y.SetMaxLength(4)

        label_width = widget_factory(wx.StaticText, main_panel, 9, "Width", pos=get_right_position(text_y, 20, ADJUST))
        text_width = widget_factory(wx.TextCtrl, main_panel, 4, str(target_box.get_width()), pos=get_right_position(label_width, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        text_width.SetMaxLength(4)

        label_height = widget_factory(wx.StaticText, main_panel, 10, "Height", pos=get_right_position(text_width, 20, ADJUST))
        text_height = widget_factory(wx.TextCtrl, main_panel, 5, str(target_box.get_height()), pos=get_right_position(label_height, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        text_height.SetMaxLength(4)

        if target_box.inner_layout:
            check_optimization = widget_factory( wx.CheckBox, main_panel, 15, "Optimize layout in this box.", pos=get_bottom_position(label_x, 15))
            check_optimization.SetValue(target_box.inner_layout.optimization_needed)

    def render_conditions(self, target_box):
        ADJUST= 2
        main_panel = self.main_panel

        def get_func_dict_value(box, name, key):
            function = None
            for condfun in box.condition.condfuns:
                if condfun.function.__name__ == name:
                    function = condfun.function
                    break

            if function:
                return function.func_dict[key]
            else:
                return ""

        STYLE_TEXT_SIZE = (50,23)
        label_x_from = widget_factory(wx.StaticText, main_panel, 18, "X Constraint", pos=get_bottom_position(get_widget_by_id(16), 20))
        text_x_from = widget_factory(wx.TextCtrl, main_panel, 19, str(get_func_dict_value(target_box, '_x_constraint', 'lower')) , pos=get_right_position(label_x_from, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        label_x_to = widget_factory(wx.StaticText, main_panel, 20, " - ", pos=get_right_position(text_x_from, 5, ADJUST))
        text_x_to = widget_factory(wx.TextCtrl, main_panel, 21, str(get_func_dict_value(target_box, '_x_constraint', 'upper')) , pos=get_right_position(label_x_to, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        check_x_constraint = widget_factory(wx.CheckBox, main_panel, 34, "Hard Constraint", pos=get_right_position(text_x_to, 20, 3))
        check_x_constraint.SetValue(bool(get_func_dict_value(target_box, '_x_constraint', 'soft_hard')))
        text_x_from.SetMaxLength(4)
        text_x_to.SetMaxLength(4)

        label_y_from = widget_factory(wx.StaticText, main_panel, 22, "Y Constraint", pos=get_bottom_position(label_x_from, 10))
        text_y_from = widget_factory(wx.TextCtrl, main_panel, 23, str(get_func_dict_value(target_box, '_y_constraint', 'lower')) , pos=get_right_position(label_y_from, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        label_y_to = widget_factory(wx.StaticText, main_panel, 24, " - ", pos=get_right_position(text_y_from, 5, ADJUST))
        text_y_to = widget_factory(wx.TextCtrl, main_panel, 25, str(get_func_dict_value(target_box, '_y_constraint', 'upper')) , pos=get_right_position(label_y_to, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        check_y_constraint = widget_factory(wx.CheckBox, main_panel, 35, "Hard Constraint", pos=get_right_position(text_y_to, 20, 3))
        check_y_constraint.SetValue(bool(get_func_dict_value(target_box, '_y_constraint', 'soft_hard')))
        text_y_from.SetMaxLength(4)
        text_y_to.SetMaxLength(4)

        label_width_from = widget_factory(wx.StaticText, main_panel, 26, "Width Constraint", pos=get_bottom_position(label_y_from, 10))
        text_width_from = widget_factory(wx.TextCtrl, main_panel, 27, str(get_func_dict_value(target_box, '_width_constraint', 'lower')) , pos=get_right_position(label_width_from, 9, -ADJUST), size=STYLE_TEXT_SIZE)
        label_width_to = widget_factory(wx.StaticText, main_panel, 28, " - ", pos=get_right_position(text_width_from, 5, ADJUST))
        text_width_to = widget_factory(wx.TextCtrl, main_panel, 29, str(get_func_dict_value(target_box, '_width_constraint', 'upper')) , pos=get_right_position(label_width_to, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        check_width_constraint = widget_factory(wx.CheckBox, main_panel, 36, "Hard Constraint", pos=get_right_position(text_width_to, 20, 3))
        check_width_constraint.SetValue(bool(get_func_dict_value(target_box, '_width_constraint', 'soft_hard')))
        text_width_from.SetMaxLength(4)
        text_width_to.SetMaxLength(4)

        label_height_from = widget_factory(wx.StaticText, main_panel, 30, "Height Constraint", pos=get_bottom_position(label_width_from, 10))
        text_height_from = widget_factory(wx.TextCtrl, main_panel, 31, str(get_func_dict_value(target_box, '_height_constraint', 'lower')) , pos=get_right_position(label_height_from, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        label_height_to = widget_factory(wx.StaticText, main_panel, 32, " - ", pos=get_right_position(text_height_from, 5, ADJUST))
        text_height_to = widget_factory(wx.TextCtrl, main_panel, 33, str(get_func_dict_value(target_box, '_height_constraint', 'upper')) , pos=get_right_position(label_height_to, 5, -ADJUST), size=STYLE_TEXT_SIZE)
        check_height_constraint = widget_factory(wx.CheckBox, main_panel, 37, "Hard Constraint", pos=get_right_position(text_height_to, 20, 3))
        check_height_constraint.SetValue(bool(get_func_dict_value(target_box, '_height_constraint', 'soft_hard')))
        text_height_from.SetMaxLength(4)
        text_height_to.SetMaxLength(4)


    def render_buttons(self):
        main_panel = self.main_panel

        make_button = widget_factory(wx.Button, main_panel, 11, "Make New Box", pos=get_bottom_position(get_widget_by_id(17), 10))
        make_button.Bind(wx.EVT_BUTTON, click_make_button)

        upper_button = widget_factory(wx.Button, main_panel, 12, "Upper Layer", pos=get_right_position(make_button, 10, -4))
        upper_button.Bind(wx.EVT_BUTTON, click_upper_button)

        update_button = widget_factory(wx.Button, main_panel, 13, "Update", pos=get_right_position(upper_button, 10, -4))
        update_button.Bind(wx.EVT_BUTTON, click_update_button)

        reset_button = widget_factory(wx.Button, main_panel, 42, "Reset", pos=get_bottom_position(make_button, 5, -6))
        reset_button.Bind(wx.EVT_BUTTON, click_reset_button)

        show_button = widget_factory(wx.Button, main_panel, 38, "Show", pos=get_right_position(reset_button, 10, -4))
        show_button.Bind(wx.EVT_BUTTON, click_show_button)

        start_button = widget_factory(wx.Button, main_panel, 14, "Start", pos=get_right_position(show_button, 10, -4))
        start_button.Bind(wx.EVT_BUTTON, click_start_button)

    def refresh(self, target_box):

        self.set_main_panel(wx.Panel(self.base_panel, wx.ID_ANY, pos=MAIN_PADDING, size=(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])))
        main_panel = self.main_panel

        check_render_value_before = False
        if get_widget_by_id(43): check_render_value_before = get_widget_by_id(43).GetValue()

        # reset all widgets on panel
        for child in g_widgets.values():
            child.Destroy()

        list_box = widget_factory(wx.ListBox, main_panel, 15, choices=get_agent_list(target_box), style=wx.LB_SINGLE, pos=(2,2), size=(150, 368))
        list_box.Bind(wx.EVT_LISTBOX, select_list_box)

        self.render_box_options(target_box)

        line1 = widget_factory(wx.StaticLine, main_panel, 16, pos=get_bottom_position(get_widget_by_id(7), 60), size=(525,2))

        self.render_conditions(target_box)

        line1 = widget_factory(wx.StaticLine, main_panel, 17, pos=get_bottom_position(get_widget_by_id(7), 205), size=(525,2))

        self.render_buttons()

        check_render = widget_factory( wx.CheckBox, main_panel, 43, "Render process of optimization.", pos=get_right_position(get_widget_by_id(14), 15))
        check_render.SetValue(check_render_value_before)

        self.Show()
        wx.Yield() 

def reset():
    global g_main_frame

    main_app = wx.App()
    base_layout = Layout.get_softplanner_layout()
    base_box =  base_layout.base_box
    #base_box =  BoxAgent(Style([0,0], WINDOW_SIZE, 0), "base")
    #Layout([], base_box)

    if g_main_frame: g_main_frame.Destroy()
    g_main_frame = MainFrame(base_box, None, -1, u'Layout Designator', pos=(100,100),size=MAIN_WINDOW_SIZE)

    main_app.MainLoop()

def main():
    reset()


def select_list_box(event):
    update()
    current_box = g_main_frame.current_box

    object = event.GetEventObject()
    nth = object.GetSelection()
    selected_box = current_box.inner_layout.agents[nth]

    g_main_frame.set_current_box(selected_box)
    g_main_frame.refresh(selected_box)

def click_reset_button(event):
    reset()

def click_make_button(event):
    update()
    new_box = BoxAgent(Style([0,0], [0,0], 1), "new box")
    Layout([], new_box) # create inner layout of new_box

    g_main_frame.current_box.inner_layout.add_box(new_box)

    g_main_frame.set_current_box(new_box)
    g_main_frame.refresh(new_box)

def click_upper_button(event):
    update()
    parent_layout = g_main_frame.current_box.parent_layout
    if parent_layout:
        g_main_frame.set_current_box(parent_layout.base_box)
        g_main_frame.refresh(parent_layout.base_box)


def click_update_button(event):
    update()

def myint(value):
    if value == "" or value == "None":
        return None
    else:
        return int(value)

def update():
    current_box = g_main_frame.current_box
    current_box.set_identifier(get_widget_by_id(1).GetValue())
    current_box.set_text(get_widget_by_id(41).GetValue())
    current_box.set_width(int(get_widget_by_id(4).GetValue()))
    current_box.set_height(int(get_widget_by_id(5).GetValue()))
    current_box.set_x(int(get_widget_by_id(2).GetValue()))
    current_box.set_y(int(get_widget_by_id(3).GetValue()))

    current_box.condition.remove_condfun_by_name("_x_constraint")
    if get_widget_by_id(19).GetValue() or get_widget_by_id(21).GetValue():
        new_condfun = BoxCondFun.x_constraint(myint(get_widget_by_id(19).GetValue()), myint(get_widget_by_id(21).GetValue()), int(get_widget_by_id(34).GetValue()))
        current_box.condition.add_condfun(new_condfun)

    current_box.condition.remove_condfun_by_name("_y_constraint")
    if get_widget_by_id(23).GetValue() or get_widget_by_id(25).GetValue():
        new_condfun = BoxCondFun.y_constraint(myint(get_widget_by_id(23).GetValue()), myint(get_widget_by_id(25).GetValue()), int(get_widget_by_id(35).GetValue()))
        current_box.condition.add_condfun(new_condfun)

    current_box.condition.remove_condfun_by_name("_width_constraint")
    if get_widget_by_id(27).GetValue() or get_widget_by_id(29).GetValue():
        new_condfun = BoxCondFun.width_constraint(myint(get_widget_by_id(27).GetValue()), myint(get_widget_by_id(29).GetValue()), int(get_widget_by_id(36).GetValue()))
        current_box.condition.add_condfun(new_condfun)

    current_box.condition.remove_condfun_by_name("_height_constraint")
    if get_widget_by_id(31).GetValue() or get_widget_by_id(33).GetValue():
        new_condfun = BoxCondFun.height_constraint(myint(get_widget_by_id(31).GetValue()), myint(get_widget_by_id(33).GetValue()), int(get_widget_by_id(37).GetValue()))
        current_box.condition.add_condfun(new_condfun)

    if current_box.inner_layout:
        current_box.inner_layout.set_optimization_needed(get_widget_by_id(15).GetValue())
 
    g_main_frame.refresh(current_box)

def click_show_button(event):

    optimization_app = wx.App()
    optimization_frame = OptimizationFrame(None, -1, u'optimization', pos=(400,100))

    base_layout = g_main_frame.get_base_box().inner_layout
    base_layout.render(optimization_frame.base_panel)

    optimization_frame.Show()
    optimization_app.MainLoop()

def click_start_button(event):

    def start_optimization():
        def render_closure():
            def _render_closure():
                base_layout.render(optimization_frame.base_panel)
                optimization_frame.Show()
                wx.Yield()
            return _render_closure

        def pass_closure():
            def _pass_closure():
                pass
            return _pass_closure

        def optimize_layout_inside(layout):
            if layout:
                if layout.optimization_needed == True:
                    optimization = OCSOptimization(layout) 
                    #optimization = RandomOptimization(layout) 

                    if get_widget_by_id(43).GetValue():
                        optimization.set_render_function(render_closure())
                    else:
                        optimization.set_render_function(pass_closure())
                        
                    optimization.optimize()

                for agent in layout.agents:
                    optimize_layout_inside(agent.inner_layout)
        base_layout = g_main_frame.get_base_box().inner_layout
        optimize_layout_inside(base_layout)
        base_layout.render(optimization_frame.base_panel)


    update()

    optimization_app = wx.App()
    optimization_frame = OptimizationFrame(None, -1, u'optimization', pos=(400,100))

    start_optimization()

    print "finish"

    optimization_frame.Show()

    optimization_app.MainLoop()

if __name__ == '__main__':
    main()


