import sys
import os
import re

# module xxxxx(
# )
# endmodule

#默认的tmp文件夹
output_dir = 'tmp725' 
source_file = 'SimTop.v'
 
def run(file_dir):
    # 如果文件夹不存在，则创建它
    file_dir = file_dir +'/'
    sourcefile = source_file
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 读入原始的 Verilog 文件此处应该是可以改变的
    with open(sourcefile, 'r') as f:
        content = f.read()

    # 定义模块匹配的正则表达式
    # pattern = r'module\s+(\w+)\s*\('
    pattern = r'module\s+\w+\s*\([\s\S]*?\)\s*;[\s\S]*?endmodule'
    module_name_pattern = r'module\s+(\w+)\s*\('
    # 使用正则表达式匹配所有的模块名称
    matches = re.findall(pattern, content)
    
    index = 0
    # 遍历所有匹配到的模块，分别保存到独立的文件中
    for match in matches:
        # 计数器加1
        index = index +1
        # 定义新文件名
        module_name = re.search(module_name_pattern,match).group(1)
        # print(module_name)
        new_file_name = module_name+'.v'
        # 提取该模块的代码
        module_code = match
        # 将提取到的代码保存到新文件中
        outfile = file_dir +new_file_name
        with open(outfile, 'w') as f:
            f.write(module_code)
        print( str(index)+' '+new_file_name +' '+'OK')
        
    print('===========RUN SUCCESS===========')
    
def clean(file_dir):
     #定义要删除的文件夹
    file_dir = file_dir +'/'
    for filename in os.listdir(file_dir):
        file_path = os.path.join(file_dir, filename)
        try:
            if os.path.isfile(file_path):  # 如果是文件则删除
                os.remove(file_path)
                print(f"{file_path} has been deleted")
        except Exception as e:
            print(e)
    os.rmdir(file_dir)
    print("============Clean Down===============")


if __name__ == "__main__":
    #求命令行参数个数
    num_args = len(sys.argv)-1
    #如果命令行参数不够
    if(num_args == 0):
        print("=============请重新输入参数=============")
        print('第一个是命令类型，第二个是文件夹名')
        print('python3 verilogSplit.py xx.v run/clean tmp')
        
    #采用默认参数
    elif(num_args == 1):
        if(sys.argv[1]=="clean"):
            if not os.path.exists(output_dir):
                print('不存在文件该文件夹')
            else:
                clean(output_dir)
        elif(sys.argv[1]=="run"):
            run(output_dir)
            
        else:
            print("命令不对:请输入run或者是clean")
    #采用自定义参数
    elif(num_args == 2):
        if(sys.argv[1]=="clean"):
            if not os.path.exists(sys.argv[2]):
                print('不存在文件该文件夹')
            else:
                clean(sys.argv[2])
        elif(sys.argv[1]=="run"):
            run(sys.argv[2])
        else:
            print("命令不对:请输入run或者是clean")
    elif(num_args == 3):
        source_file = sys.argv[1]
        if not os.path.isfile(source_file):
            print('文件不存在')
        else:
            if(sys.argv[2]=="clean"):
                if not os.path.exists(sys.argv[3]):
                    print('不存在文件该文件夹')
                else:
                    clean(sys.argv[3])
            elif(sys.argv[2]=="run"):
                run(sys.argv[3])
            else:
                print("命令不对:请输入run或者是clean")
    #参数太多的情况
    else:
        print('=============参数太多==================')
        print("=============请重新输入参数=============")
        print('第一个是命令类型，第二个是文件夹名')
        print('python3 verilogSplit.py xx.v run/clean tmp')
        print("=====================================")