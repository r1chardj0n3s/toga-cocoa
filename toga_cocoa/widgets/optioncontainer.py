from ..libs import *
from .base import Widget


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        pass
        # print ("Select tab view item")


class OptionContainer(Widget):
    def __init__(self, style=None):
        super(OptionContainer, self).__init__(style=None)
        self.is_container = True
        self._content = []

        self.startup()

    def startup(self):
        self._impl = NSTabView.alloc().init()

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        self._delegate = TogaTabViewDelegate.alloc().init()
        self._delegate.__dict__['interface'] = self

        self._impl.setDelegate_(self._delegate)

    def add(self, label, container):
        self._content.append((label, container))
        container.window = self.window

        item = NSTabViewItem.alloc().initWithIdentifier_('%s-Tab-%s' % (id(self), id(container)))
        item.setLabel_(label)
        container.app = self.app

        item.setView_(container._impl)

        self._impl.addTabViewItem_(item)

        # Make the content autoresize to the option container item frame
        container._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

    def _update_child_layout(self, **style):
        """Force a layout update on the children of this widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for label, content in self._content:
            frame = self._impl.contentRect
            content._update_layout(
                left=frame.origin.x,
                top=frame.origin.y,
                width=frame.size.width,
                height=frame.size.height
            )
