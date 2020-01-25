from colorsys import hls_to_rgb


def generate_colors(nums):
    max_val, min_val = max(nums), min(nums)
    max_hue, min_hue = 240, 0
    colors = []
    for num in nums:
        normalized_num = (num - min_val) / (max_val - min_val)
        colors.append(normalized_num * (max_hue - min_hue) / 360)
    colors = [hls_to_rgb(hue, 0.53, 1) for hue in colors]
    hex_colors = ["#{:02x}{:02x}{:02x}".format(int(c[0]*255), int(c[1]*255), int(c[2]*255)) for c in colors]

    return hex_colors

if __name__ == '__main__':
    nums = [-3.1, -5, 3, 1, 7]
    colors = generate_colors(nums)
    print(colors)

