from ..libs import *
from .base import Widget
from toga.constants import *


class ImageView(Widget):
    def __init__(self, image=None, style=None):
        super(ImageView, self).__init__(style=style)

        self.startup()

        self.image = image

    def startup(self):
        self._impl = NSImageView.alloc().init()
        self._impl.__dict__['interface'] = self

        # self._impl.setImageFrameStyle_(NSImageFrameGrayBezel)
        self._impl.setImageFrameStyle_(NSImageFrameNone)
        self._impl.setImageAlignment_(NSImageAlignCenter)
        self._impl.setImageScaling_(NSImageScaleProportionallyUpOrDown)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # self._impl.setWantsLayer_(True)
        # self._impl.setBackgroundColor_(NSColor.blueColor())

        # if self.width is None:
        #     self.width = self._impl.fittingSize().width
        # if self.height is None:
        #     self.height = self._impl.fittingSize().height

    # @property
    # def alignment(self):
    #     return self._alignment

    # @alignment.setter
    # def alignment(self, value):
    #     self._alignment = value
    #     self._impl.setAlignment_(NSTextAlignment(self._alignment))

    # @property
    # def scaling(self):
    #     return self._scaling

    # @scaling.setter
    # def scaling(self, value):
    #     self._scaling = value
    #     self._impl.setAlignment_(NSTextAlignment(self._scaling))

    @property
    def image(self):
        return self._impl.image

    @image.setter
    def image(self, image):
        if image:
            self._impl.image = image._impl
        else:
            self._impl.image = NSImage.alloc().initWithSize_(NSSize(self.width, self.height))
