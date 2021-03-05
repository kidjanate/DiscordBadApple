import time
import os
import discord
from discord.ext import commands
from PIL import Image
import cv2

ASCII_CHARS = ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "@"]


def resized_gray_image(image, new_width=70):
	new_height = 20
	resized_gray = image.resize((new_width, new_height)).convert('L')
	return resized_gray


def pix2chars(image):
	pixels = image.getdata()
	characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
	return characters


def generate_frame(image, new_width=70):
	new_image_data = pix2chars(resized_gray_image(image, new_width=new_width))

	total_pixels = len(new_image_data)
	print(total_pixels)

	ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, total_pixels, new_width)])
	"""
		sys.stdout.write(ascii_image)
		os.system('cls' if os.name == 'nt' else 'clear')
		"""
	return "`" + ascii_image + "`"


TOKEN = os.getenv("TOKEN")
PREFIX = 'b.'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)


@bot.event
async def on_ready():
	print(f'Logged in as: {bot.user.name}')
	print(f'With ID: {bot.user.id}')


@bot.command()
async def badapple(ctx):
	iscreated = False
	msg = None
	cap = cv2.VideoCapture('bad_apple.mp4')
	i = 0
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break
		if not i % 10:
			asciiframe = generate_frame(Image.fromarray(frame), 70)
			if not iscreated:
				msg = await ctx.send(asciiframe)
				# iscreated = True
				time.sleep(0.3)
			else:
				await msg.edit(content=asciiframe)
				time.sleep(1.2)
		i += 1
	await ctx.send("That's all")


bot.run(TOKEN)
