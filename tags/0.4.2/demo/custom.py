### A custom item example

import sys
import gobject
import gtk
import goocanvas

class CustomItem(gobject.GObject, goocanvas.Item, goocanvas.ItemView):

    __gproperties__ = {
        'title': (str, None, None, '', gobject.PARAM_READWRITE),
        'description': (str, None, None, '', gobject.PARAM_READWRITE),
        'can-focus': (bool, None, None, False, gobject.PARAM_READWRITE),
        'visibility-threshold': (float, None, None, 0, 10e6, 0, gobject.PARAM_READWRITE),
        'visibility': (goocanvas.ItemVisibility, None, None, goocanvas.ITEM_VISIBLE, gobject.PARAM_READWRITE),
        'pointer-events': (goocanvas.PointerEvents, None, None, goocanvas.EVENTS_NONE, gobject.PARAM_READWRITE),
        'transform': (goocanvas.TYPE_CAIRO_MATRIX, None, None, gobject.PARAM_READWRITE),
        }


    def __init__(self, **kwargs):
        self.bounds = goocanvas.Bounds()
        self.view = None
        self.parent = None

        ## default values for properties
        #self.title = None
        #self.description = None
        #self.can_focus = False
        #self.visibility = goocanvas.ITEM_VISIBLE
        #self.visibility_threshold = 0.0
        #self.pointer_events = goocanvas.EVENTS_NONE
        #self.transform = None

        ## chain to parent constructor
        gobject.GObject.__init__(self, **kwargs)

    def do_create_view(self, canvas_view, parent_view):
        assert self.view is None
        self.view = self
        return self

    def do_set_parent(self, parent):
        assert self.parent is None
        self.parent = parent

    def do_set_property(self, pspec, value):
        if pspec.name == 'title':
            self.title = value
        elif pspec.name == 'description':
            self.description = value
        elif pspec.name == 'can-focus':
            self.can_focus = value
        elif pspec.name == 'visibility':
            self.visibility = value
        elif pspec.name == 'visibility-threshold':
            self.visibility_threshold = value
        elif pspec.name == 'pointer-events':
            self.pointer_events = value
        elif pspec.name == 'transform':
            self.transform = value
        else:
            raise AttributeError, 'unknown property %s' % pspec.name
        
    def do_get_property(self, pspec):
        if pspec.name == 'title':
            return self.title
        elif pspec.name == 'description':
            return self.description
        elif pspec.name == 'can-focus':
            return self.can_focus
        elif pspec.name == 'visibility':
            return self.visibility
        elif pspec.name == 'visibility-threshold':
            return self.visibility_threshold
        elif pspec.name == 'pointer-events':
            return self.pointer_events
        elif pspec.name == 'transform':
            return self.transform
        else:
            raise AttributeError, 'unknown property %s' % pspec.name

    ## optional methods
    def do_get_bounds(self):
        return self.bounds

    def do_get_item_view_at(self, x, y, cr, is_pointer_event, parent_is_visible):
        return None

    def do_set_parent_view(self, parent_view):
        pass

    ## mandatory methods
    def do_update(self, entire_tree, cr):
        raise NotImplementedError

    def do_paint(self, cr, bounds, scale):
        raise NotImplementedError



class CustomRectItem(CustomItem):

    def __init__(self, x, y, width, height, line_width, **kwargs):
        CustomItem.__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.line_width = line_width

    def do_update(self, entire_tree, cr):
        half_lw = self.line_width/2
        self.bounds.x1 = float(self.x - half_lw)
        self.bounds.y1 = float(self.y - half_lw)
        self.bounds.x2 = float(self.x + self.width + half_lw)
        self.bounds.y2 = float(self.y + self.height + half_lw)
        return self.bounds

    def do_paint(self, cr, bounds, scale):
        cr.rectangle(self.x, self.y, self.width, self.height)
        cr.set_line_width(self.line_width)
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()
        return self.bounds



def main(argv):
    window = gtk.Window()
    window.set_default_size(640, 600)
    window.show()
    window.connect("destroy", lambda w: gtk.main_quit())
    
    scrolled_win = gtk.ScrolledWindow()
    scrolled_win.set_shadow_type(gtk.SHADOW_IN)
    scrolled_win.show()
    window.add(scrolled_win)
    
    canvas = goocanvas.CanvasView()
    canvas.set_size_request(600, 450)
    canvas.set_bounds(0, 0, 1000, 1000)
    canvas.show()
    scrolled_win.add(canvas)
    
    ## Create the canvas model
    canvas_model = create_canvas_model()
    canvas.set_model(canvas_model)

    gtk.main()


def create_canvas_model():
    canvas_model = goocanvas.CanvasModelSimple()
    root = canvas_model.get_root_item()
    item = CustomRectItem(x=100, y=100, width=400, height=400, line_width=20)
    root.add_child(item)
    item = goocanvas.Text(text="Hello World",
                          x=300, y=300,
                          anchor=gtk.ANCHOR_CENTER,
                          font="Sans 24")
    root.add_child(item)
    item.rotate(45, 300, 300)

    return canvas_model


if __name__ == "__main__":
    main(sys.argv)
