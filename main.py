from PIL import Image, ImageDraw, ImageFont
import numpy as np
import unicodedata

count = 0 # 文字数
    
# 設定
font_size = 200
image_size = (font_size, font_size)
max_density=0
max_density_char=''
max_density_code=0x00
max_density_name=''

# フォントを指定（OSに応じて変更してください）
# Windowsなら： 'msgothic.ttc' や 'meiryo.ttc'
# Macなら：'/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
# ここではデフォルトを使用（文字化けするならパスを指定）
font = ImageFont.truetype("C:/Windows/Fonts/YuGothR.ttc", font_size)  # ←適切な CJK フォントを指定
    
for codepoint in range(0x110000):
    char = chr(codepoint)
   
    try:
        name = unicodedata.name(char)
        if "CJK" in name:
            # 画像を生成
            image = Image.new("L", image_size, "white")
            draw = ImageDraw.Draw(image)
            bbox = draw.textbbox((0, 0), char, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), char, fill="black", font=font)

            # モノクロ処理（二値化）
            bw = image.point(lambda x: 0 if x < 128 else 255, '1')

            # NumPy配列に変換し、黒ピクセルの割合を計算
            arr = np.array(bw)
            black_pixels = np.sum(arr == 0)
            total_pixels = arr.size
            density = black_pixels / total_pixels
            
            # ● 文字化け・空白などの除外条件（描画されてないと判断）
            if black_pixels < total_pixels * 0.001:
                continue
            
            print(f"U+{codepoint:04X} {char} {name} {count}")
            
            if density>max_density:
                max_density=density
                max_density_char=char
                max_density_code=codepoint
                max_density_name=name
                print(f"密度（黒の割合）：{density:.4f}")      
                
            count += 1

    except ValueError:
        continue  # 名前が無い（未定義）文字はスキップ

    # if count>22000:
    #     break
    

# 画像を生成
image = Image.new("L", image_size, "white")
draw = ImageDraw.Draw(image)
bbox = draw.textbbox((0, 0), max_density_char, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), max_density_char, fill="black", font=font)

image.save('./max_denity_char.png')

print(f"U+{max_density_code:04X} {max_density_char} {max_density_name}")
print(f"密度（黒の割合）：{max_density:.4f}")              

