from PIL import Image
import asyncio
ASCII_CHARS = ["-", "#", "S", "%", "?", "*", "+", ";", ":", ",", "@"]

def resized_gray_image(image ,new_width=70):
	width,height = image.size
	aspect_ratio = height/width
	new_height = 20
	resized_gray_image = image.resize((new_width,new_height)).convert('L')
	return resized_gray_image

def pix2chars(image):
	pixels = image.getdata()
	characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
	return characters

def generate_frame(image,new_width=70):
	new_image_data = pix2chars(resized_gray_image(image,new_width=new_width))

	total_pixels = len(new_image_data)
	print(total_pixels)

	ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, total_pixels, new_width)])

	return "`"+ascii_image+"`"
	"""
	sys.stdout.write(ascii_image)
	os.system('cls' if os.name == 'nt' else 'clear')
	"""


import discord
from discord.ext import commands
TOKEN = 'ODA3MTU1NTQxNDkwMjcwMjE4.YBz4LQ.j8Nh4mB1qWMLkIglJd3F0bo7dWQ'
PREFIX = 'b.'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)


@bot.event
async def on_ready():
	print(f'Logged in as: {bot.user.name}')
	print(f'With ID: {bot.user.id}')


@bot.command()
async def badapple(ctx):
	if(ctx.channel.id == 807155469071155200):
		i = 0
		isCreated = False
		msg = None
		while i < 7000:
			i = i + 10
			img = Image.open(f"frames/frame{i}.jpg")
			frame = generate_frame(img,60)
			if frame != None:
				if isCreated == False:
					msg = await ctx.send(frame)
					isCreated = True
				else:
					await msg.edit(content=frame)
					asyncio.sleep(1.2)
					
		await ctx.send("That's all")
				


bot.run(TOKEN)




	
