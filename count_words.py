#!/usr/bin/env python3
import os
import re

def count_chinese_words(text):
    # 移除YAML前言（通常在Markdown文件开头的---之间）
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)
    
    # 移除Markdown图片链接
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # 移除Markdown链接
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    # 移除HTML标签
    text = re.sub(r'<.*?>', '', text)
    
    # 移除代码块
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', '', text)
    
    # 移除#号（标题）
    text = re.sub(r'#+ ', '', text)
    
    # 移除空行和空格
    text = re.sub(r'\s+', '', text)
    
    # 计算字符数（中英文都算一个字）
    return len(text)

def main():
    posts_dir = '/Volumes/pjhubs_t7/app/windstormeye.github.io/source/_posts'
    total_words = 0
    file_count = 0
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md') and not filename.startswith('.'):
            file_path = os.path.join(posts_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = count_chinese_words(content)
                    total_words += words
                    file_count += 1
                    print(f"{filename}: {words} 字")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
    
    print("\n统计结果:")
    print(f"总文件数: {file_count} 个")
    print(f"总字数: {total_words} 字")
    print(f"平均每篇: {total_words // file_count if file_count else 0} 字")

if __name__ == "__main__":
    main()