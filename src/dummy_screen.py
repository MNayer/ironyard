from PIL.ImageFile import ImageFile

class DummyScreen:

    def update(self, image: ImageFile):
        image.show()


    def shutdown(self):
        pass

