import re
import os

# ==========================================
# 2. 主处理逻辑
# ==========================================
def process_material_list(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 '{input_file}'")
        print("请将您的材料清单内容保存为 input.txt 后再运行脚本。")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试使用 gb18030 编码读取 (有时 Windows 记事本默认编码)
        try:
            with open(input_file, 'r', encoding='gb18030') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败：{e}")
            return

    # 用于存储结果的列表
    results = []
    # 用于记录未识别的物品，方便用户补充字典
    unknown_items = set()

    # 正则表达式解释：
    # \|        匹配竖线 |
    # \s*       匹配可能的空格
    # ([^\|]+?) 捕获组 1：匹配非竖线字符 (物品名)，非贪婪
    # \s*       匹配可能的空格
    # \|        匹配竖线 |
    # \s*       匹配可能的空格
    # (\d+)     捕获组 2：匹配数字 (数量)
    # \s*       匹配可能的空格
    # \|        匹配竖线 |
    pattern = r"\|\s*([^\|]+?)\s*\|\s*(\d+)\s*\|"

    matches = re.findall(pattern, content)

    for name, count in matches:
        name = name.strip()
        
        # 过滤掉表头或无关行
        if name in ["Item", "原理图的材料清单", "文件名", "摘要", "文档名", "标题", "正文"]:
            continue
        if "区域" in name or "Missing" in name or "Available" in name:
            continue

        mc_id = name
        results.append(f"{mc_id} {count}")

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

    print(f"转换完成！结果已保存至 '{output_file}'")
    if unknown_items:
        print(f"\n发现 {len(unknown_items)} 个未识别的物品，请检查脚本中的映射字典：")
        for item in unknown_items:
            print(f"  - {item}")

if __name__ == "__main__":
    # 输入文件名 (请确保你的内容保存在这个文件里)
    input_filename = "input.txt"
    # 输出文件名 (固定为 1.txt)
    output_filename = "1.txt"
    
    process_material_list(input_filename, output_filename)
