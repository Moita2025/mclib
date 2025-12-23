import os
from pathlib import Path
from PIL import Image

def retry_failed_images(fail_txt_path):
    # 读取失败的图片路径列表，使用字典存储源文件和失败放大文件的对应关系
    failed_images = {}
    with open(fail_txt_path, 'r') as file:
        for line in file:
            failed_image = line.strip()  # 去除首尾空白字符
            if not failed_image:
                continue
            
            # 获取源图片路径（去除 -256px）
            original_image = failed_image.replace("-256px.png", ".png")
            failed_images[original_image] = failed_image
    
    # 第一遍遍历，删除失败的放大文件
    for original_image, failed_image in failed_images.items():
        failed_image_path = Path(failed_image)
        if failed_image_path.exists():
            os.remove(failed_image_path)
            print(f"已删除失败的放大文件: {failed_image_path}")
    
    # 等待用户输入确认是否生成放大版本
    user_input = input("是否重新为失败的图片生成放大版本? (Y/N): ").strip().lower()
    if user_input == "y":
        # 第二遍遍历，重新生成放大文件
        for original_image, failed_image in failed_images.items():
            original_image_path = Path(original_image)
            
            if not original_image_path.exists():
                print(f"  原始图片 {original_image} 不存在，跳过")
                continue
            
            try:
                with Image.open(original_image_path) as im:
                    width, height = im.size
                    
                    # 只处理小于 16x16 的图片
                    if width != 16 or height != 16:
                        print(f"  图片 {original_image} 不是 16x16，跳过")
                        continue
                    
                    # 放大至 256x256（重复 16x16 为 256x256）
                    resized_im = im.resize((256, 256), Image.Resampling.NEAREST)
                    target_file = original_image_path.with_name(original_image_path.stem + "-256px.png")
                    
                    # 保存放大后的图片
                    resized_im.save(target_file, "PNG")
                    print(f"  已生成: {target_file.name}")
            except Exception as e:
                print(f"  处理失败 {original_image}: {e}")

    # 删除失败记录文件
    os.remove(fail_txt_path)
    print(f"已删除失败记录文件: {fail_txt_path}")

if __name__ == "__main__":

    # 假设你的失败记录存储在 fail.txt 中
    fail_txt_path = "fail-1st.txt"
    
    # 如果失败记录文件存在，进行处理
    if Path(fail_txt_path).exists():
        retry_failed_images(fail_txt_path)
    else:
        print("没有找到失败记录文件！")