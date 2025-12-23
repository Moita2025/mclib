import os
from pathlib import Path
from PIL import Image

def process_img_directories(root_dir="."):
    root_path = Path(root_dir)
    
    # 递归查找所有名为 "img" 的目录
    for img_dir in root_path.rglob("img"):
        if not img_dir.is_dir():
            continue
        
        print(f"正在处理目录: {img_dir}")
        
        # 遍历该 img 目录下的所有 .png 文件（不递归子目录）
        for png_file in img_dir.glob("*.png"):
            # 跳过已经是 "-256px.png" 结尾的文件，防止重复处理
            if png_file.name.endswith("-256px.png"):
                continue
                
            # 构造目标文件名：例如 a.png -> a-256px.png
            target_name = png_file.stem + "-256px.png"
            target_file = png_file.with_name(target_name)
            
            # 如果目标文件已经存在，直接跳过
            if target_file.exists():
                print(f"  跳过（已存在）: {target_file.name}")
                continue
            
            # 打开图片获取尺寸信息
            try:
                with Image.open(png_file) as im:
                    width, height = im.size
                    
                    # 新增条件：只有宽高都 < 72px 才进行放大
                    if width >= 72 or height >= 72:
                        print(f"  跳过（尺寸不满足 <72px）: {png_file.name} ({width}x{height})")
                        continue
                    
                    # 计算等比例放大后的高度（目标宽度 256px）
                    width_percent = 256 / width
                    new_height = int(height * width_percent)
                    
                    # 放大图片，使用高质量滤镜
                    resized_im = im.resize((256, new_height), Image.Resampling.LANCZOS)
                    
                    # 保存新文件
                    resized_im.save(target_file, "PNG")
                    print(f"  已生成: {target_file.name} ({256}x{new_height}) ← 从 {png_file.name} ({width}x{height})")
            
            except Exception as e:
                print(f"  处理失败 {png_file.name}: {e}")

if __name__ == "__main__":
    # 需要安装 Pillow: pip install pillow
    process_img_directories(".")
    print("所有 img 目录处理完成！")