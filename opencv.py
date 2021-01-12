
import zipfile
from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv

# načtení face detection classifier (fdc)
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
# vybrané slovo, které musí být v textu, aby se ukázaly fotky z te stránky
word = "Mark"

# načtení souborů (novin)
zf =  zipfile.ZipFile("readonly/images.zip", "r")
zf.extractall()
pictures = zf.namelist()

# procházení souborů a hledání obličejů podle fdc
for picture in pictures:
   text = pytesseract.image_to_string((Image.open(picture).convert("L")))
   if word in text:
      print("Results found in file " + str(picture))
      img = cv.imread(picture)
      # převedení na černobílou
      gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
      # detekce obličejů
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=7)
      if len(faces) == 0:
         print("But there were no faces in that file!")
      else:
          # tvorba matice (velikost obrazu) podle počtu obličejů
         x = faces.tolist()
         faces.tolist()
         if len(x) > 0:
            if len(x) // 5 == 0:
               black = Image.new('RGB', (500, 100))
            elif (len(x) // 5) > 0 and (len(x) % 5) == 0:
                black = Image.new('RGB', (500, 100 * (len(x) // 5)))
            else:
                black = Image.new('RGB', (500, 100 * ((len(x) // 5) + 1)))
                i = 0
                images = []
                for face in faces.tolist():
                   im = Image.open(picture)
                   fc = faces.tolist()[i]
                   a = fc[0]
                   b = fc[1]
                   c = fc[0] + fc[2]
                   d = fc[1] + fc[3]
                   facepic = im.crop((a, b, c, d))
                   # zajištění že všechny fotky jsou 100x100 (vyplnění černou nebo změnšení)
                   if facepic.width < 100 or facepic.height < 100:
                      facepicblack = Image.new('RGB', (100, 100))
                      facepicblack.paste(facepic, (0, 0))
                      images.append(facepicblack)
                   else:
                      facepicresize = facepic.resize((100, 100))
                      images.append(facepicresize)
                   i += 1
                first_image = images[0]
                x = 0
                y = 0
                # vložení fotek do matice
                for img in images:
                   black.paste(img, (x, y) )
                   if x + first_image.width == black.width:
                      x = 0
                      y = y + first_image.height
                   else:
                      x = x + first_image.width
            display(black)
   else:
      pass
