import cv2
import pygame as pg
from numba import njit





class AsciiConverter:
    def __init__(self, path, font_size):
        pg.init()
        self.path = path
        self.capture = cv2.VideoCapture(path)
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()


        self.ASCII_CHARS = '.",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Roboto',font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

        self.rec_fps = 10
        self.record = False
        self.recorder = cv2.VideoWriter('video/convert.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.rec_fps,self.RES)

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.transpose(frame)

    def rec_frame(self):
        if self.record:
            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record  = not self.record
                cv2.destroyAllWindows()
    def convert(self):
        self.image = self.get_image()
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))


    def get_image(self):
        ret,self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image,cv2.COLOR_BGR2GRAY)
        return gray_image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image,(640,360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img',resized_cv2_image)

    def draw(self):
        self.surface.fill('black')

        self.convert()

    def save(self):
        pygame_img = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_img)
        cv2.imwrite('img/convert3.png', cv2_img)

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save()

            self.record = not self.record
            self.rec_frame()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    app = AsciiConverter(path='video/video.gif', font_size=12)

    app.run()