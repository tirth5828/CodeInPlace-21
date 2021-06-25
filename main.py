from simpleimage import SimpleImage, clamp, Pixel


def darker(image, strength=2):
    if strength < 0:
        strength *= -1
    for pixel in image:
        pixel.red = pixel.red // strength
        pixel.green = pixel.green // strength
        pixel.blue = pixel.blue // strength


def brighter(image, strength=2):
    if strength < 0:
        strength *= -1
    for pixel in image:
        pixel.red = clamp(pixel.red * strength)
        pixel.green = clamp(pixel.green * strength)
        pixel.blue = clamp(pixel.blue * strength)


def red_channel(image):
    for pixel in image:
        pixel.green = 0
        pixel.blue = 0


def green_channel(image):
    for pixel in image:
        pixel.red = 0
        pixel.blue = 0


def blue_channel(image):
    for pixel in image:
        pixel.green = 0
        pixel.red = 0


def cal_lum(red, green, blue):
    return red * 0.299 + blue * 0.114 + green * 0.587


def grayscale(image):
    for pixel in image:
        lum = cal_lum(pixel.red, pixel.green, pixel.blue)
        pixel.blue = lum
        pixel.green = lum
        pixel.red = lum


def green_screen(front_image, back_image, threshold=1.6):
    for pixel in back_image:
        average = (pixel.red + pixel.blue + pixel.green) // 3
        if pixel.green >= average * threshold:
            x = pixel.x
            y = pixel.y
            back_image.set_pixel(x, y, front_image.get_pixel(x, y))


def combine_images(image1, image2, size):
    width1 = image1.width
    width2 = image2.width
    height1 = image1.height
    height2 = image2.height
    if size % 2 == 0:
        image2.make_as_big_as(image1)
        height = height1
        width = width1 * 2
    else:
        image1.make_as_big_as(image2)
        height = height2
        width = width2 * 2

    image = SimpleImage.blank(width, height)

    for x in range(image.width):
        for y in range(image.height):
            if x < image.width // 2:
                image.set_pixel(x, y, image1.get_pixel(x, y))
            else:
                image.set_pixel(x, y, image2.get_pixel(x - (image.width // 2), y))

    return image


def rotate_clockwise(image):
    output = SimpleImage.blank(image.height, image.width)
    for x in range(image.width):
        for y in range(image.height):
            output.set_pixel(output.width - y - 1, x, image.get_pixel(x, y))
    return output


def rotate(image, turns):
    ima = image
    for turn in range(turns):
        ima = rotate_clockwise(ima)
    return ima


def contrast(image, factor, mid=100):
    for pixel in image:
        pixel.green = (pixel.green - mid) * factor + mid
        pixel.red = (pixel.red - mid) * factor + mid
        pixel.blue = (pixel.blue - mid) * factor + mid


def blur(image, kernel_size):
    blur_range = kernel_size // 2
    output = SimpleImage.blank(image.width, image.height)
    for x in range(image.width):
        for y in range(image.height):
            total_red = 0
            total_green = 0
            total_blue = 0
            num = 0
            for xi in range(max(0, x - blur_range), min(image.width - 1, x + blur_range) + 1):
                for yi in range(max(0, y - blur_range), min(image.height - 1, y + blur_range) + 1):
                    total_red += image.get_pixel(xi, yi).red
                    total_green += image.get_pixel(xi, yi).green
                    total_blue += image.get_pixel(xi, yi).blue
                    num += 1
            Pixel(output, x, y).red = total_red / num
            Pixel(output, x, y).green = total_green / num
            Pixel(output, x, y).blue = total_blue / num
    return output


def apply_kernel(image, kernel):
    kernel_range = len(kernel) // 2
    output = SimpleImage.blank(image.width, image.height)
    for x in range(image.width):
        for y in range(image.height):
            total_red = 0
            total_green = 0
            total_blue = 0
            for xi in range(max(0, x - kernel_range), min(image.width - 1, x + kernel_range) + 1):
                for yi in range(max(0, y - kernel_range), min(image.height - 1, y + kernel_range) + 1):
                    xk = xi + kernel_range - x
                    yk = yi + kernel_range - y
                    kernel_value = kernel[xk][yk]
                    total_red += (image.get_pixel(xi, yi).red * kernel_value)
                    total_green += (image.get_pixel(xi, yi).green * kernel_value)
                    total_blue += (image.get_pixel(xi, yi).blue * kernel_value)
            Pixel(output, x, y).red = total_red
            Pixel(output, x, y).green = total_green
            Pixel(output, x, y).blue = total_blue
    return output


def combine_image_in_one(image1, image2):
    image = SimpleImage.blank(image1.width, image1.height)
    for x in range(image1.width):
        for y in range(image1.height):
            Pixel(image, x, y).red = (image1.get_pixel(x, y).red ** 2 + image2.get_pixel(x, y).red ** 2) ** 0.5
            Pixel(image, x, y).green = (image1.get_pixel(x, y).green ** 2 + image2.get_pixel(x, y).green ** 2) ** 0.5
            Pixel(image, x, y).blue = (image1.get_pixel(x, y).blue ** 2 + image2.get_pixel(x, y).blue ** 2) ** 0.5
    return image


def main():
    print("HI")
    image1 = SimpleImage("1234.jpg")
    image1.show()
    kernel_x = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    kernel_y = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    kernel = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    apply_kernel(image1, kernel_x).show()
    apply_kernel(image1, kernel_y).show()
    combine_image_in_one(apply_kernel(image1, kernel_x), apply_kernel(image1, kernel_y)).show()


if __name__ == '__main__':
    main()
