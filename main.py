from PIL import Image, ImageEnhance

img = Image.open('Щеночек.jpg')

# Выводим информацию об изображении
print("Размер:", img.size)
print("Формат:", img.format)
print("Режим цвета:", img.mode)

# Изменяем контрастность (аналогично яркости)
contrast_enhancer = ImageEnhance.Contrast(img)
negative_image = contrast_enhancer.enhance(-1)

# Сохраняем изображение
negative_image.save('negative.jpg')
