from PIL import Image, ImageOps
import os

def resize_image(input_image_path, size):
    original_image = Image.open(input_image_path)
    original_image = ImageOps.exif_transpose(original_image)  # handle rotation according to EXIF info
    original_image = original_image.convert("RGBA")  # ensure support for alpha channel
    
    width, height = original_image.size
    # consider image ratio when resizing to avoid distortions
    image_ratio = width / height

    desired_width, desired_height = size
    desired_ratio = desired_width / desired_height

    if image_ratio >= desired_ratio:
        # the original image is wider than the desired size
        new_width = desired_height * image_ratio
        new_height = desired_height
    else:
        # the original image is taller than the desired size
        new_width = desired_width
        new_height = desired_width / image_ratio

    resized_image = original_image.resize((int(new_width), int(new_height)))

    # create a new image with transparent background to paste the resized image
    final_image = Image.new("RGBA", size)
    final_image.paste(resized_image, ((int((size[0] - new_width) // 2), int((size[1] - new_height) // 2))))

    return final_image

def resize_to_formats(image_path, output_dir):
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    sizes = {"background": (1600, 900),
             "full-width": (1400, 700),  
             "half-width": (700, 350),  
             "small-icons": (100, 100)}

    for format, size in sizes.items():
        resized_image = resize_image(image_path, size)
        # save the image in both png and jpg format
        output_path_png = os.path.join(output_dir, f"{format}_image.png")
        output_path_jpg = os.path.join(output_dir, f"{format}_image.jpg")
        resized_image.save(output_path_png, "PNG")
        resized_image.convert("RGB").save(output_path_jpg, "JPEG")

# Usage
image_path = "#Your location of original image here"
output_directory = "Your output location for images here"
resize_to_formats(image_path, output_directory)