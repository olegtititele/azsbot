import barcode
from barcode.writer import ImageWriter
import random
from PIL import Image
import qrcode
import random
import os



class Stroke(object):

	def __init__(self, dirr, rand_name, pic_format):
		#rand.name <str>
		self.dirr = dirr
		self.rand_name = rand_name
		self.pic_format = pic_format #".<format>"
		self.img_dir = self.dirr + self.rand_name
		self.frm_img = self.img_dir + self.pic_format

	# png
	def create_rand_hatch(self):
		barCodeImage = barcode.get('ean13', self.rand_name, writer=ImageWriter())
		barCodeImage.save(self.img_dir)
		self.clear_metadata(self.frm_img)
		photo = open(self.frm_img, 'rb')
		return photo

	# jpg
	def create_rand_qr(self):
		qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
		)
		qr.add_data(self.rand_name)
		qr.make(fit=True)
		img = qr.make_image(fill_color="black", back_color="white")
		img.save(self.frm_img, "JPEG")
		self.clear_metadata(self.frm_img)
		photo = open(self.frm_img, 'rb')
		return photo

	def clear_metadata(self, photo):
		image = Image.open(photo)
		data = list(image.getdata())
		image_without_exif = Image.new(image.mode, image.size)
		image_without_exif.putdata(data)
		image_without_exif.save(photo)
		# photo = open(qrphoto, 'rb')
		

# if __name__ == "__main__":
# 	photo = Stroke('qrcode/', "4233423342342", '.png')
# 	dre = photo.create_rand_hatch()
	# dre = photo.create_rand_qr()
	# check = YooMoney("a1b2c3d445")
	# sosa = check.make_payment(2)