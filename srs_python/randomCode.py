# encoding: utf-8
from PIL import Image,ImageFilter,ImageDraw,ImageFont
import random
from srs_admin import settings

class randomCode():
    def __init__(self):
        # 随机生成4位文件名
        name = ''
        for t in range(4):
            rt = self.randomChar()
            name += rt
        self.name=name+'.png'
        self.key=''

    def randomChar(self):
        if random.randint(1,2)==1:
            return chr(random.randint(65,90))
        else:
            return chr(random.randint(48,57))

    #背景色
    def randomColor(self):
        return (255,255,255)
        # return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
    #验证码颜色
    def randomColor2(self):
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255))


    #设置干扰线，红色
    def gene_line(self,draw,width,height):
        # 随机生成begin坐标
         begin = (random.randint(0, width), random.randint(0, height))
        # 随机生成end坐标
         end = (random.randint(0, width), random.randint(0, height))
         #用红色画线，一条从begin到end的直线
         draw.line([begin, end], fill = (255,0,0))

    def main(self):
        w = 240
        h = 60
        im = Image.new('RGB', (w, h), (255, 255, 255))
        font = ImageFont.truetype(settings.STATICFILES_DIRS[0]+'/fonts/Arial.ttf', 36)
        draw = ImageDraw.Draw(im)

        for x in range(w):
            for y in range(h):
                draw.point((x, y), fill=self.randomColor())
        #随机生成4位验证码并填入图中
        key = ''
        for t in range(4):
            rt = self.randomChar()
            draw.text((60 * t + 10, 10), rt, font=font, fill=self.randomColor2())
            key+=rt
        self.key=key


        self.gene_line(draw,w,h)
        #图像模糊
        image = im.filter(ImageFilter.BLUR)
        image.save(settings.STATICFILES_DIRS[0]+'/image/'+self.name)

if __name__ == '__main__':
    r = randomCode()
    r.main()
