# ***********************************************
# FileName:findModule.py
# AuthorZhaoPengTime2023-08-03 
# Discribe: Script to find module files all need
# ----------------BOSC NanhuV2---------
#************************************************

# ATTENTION!!!!!!
# there are 3 place user to do in this pyhon scripts 
# please find th ekey words as "USER TO DO"
# the fist is to define a folder for rtl code 
# the second is to define a name of verilog module rtl file list
# the third is to define a folder for put all the verilog module files 
# default: use the current time as the suffix of the name of verilog module rtl file list
# default: use the current time as the suffix of the folder for put all the verilog module files 

# import the pkg this script need
import os,sys,re,glob,shutil
from datetime import datetime
# =============================================================================================================================================
# USER TO DO, set the rtl code folder where is relative path to this pyhon script file
rtl_folder = 'tmp725'          # user shoul set the rtl verilog file path [no sep! no sep! no sep!]
# =============================================================================================================================================
verilog_code_pattern = r"(\w+)\s+\w+\s*\([\s\S]*?\)\;" # define the match patern, this will find the incorrect result but give a resolution 
cur_sep = os.path.sep           # the differrent sep in differrent os 
topModule = ''                  # the top module 
allFileList = []                # the all module and sub module file list
rtl_folder = rtl_folder+cur_sep # add cur_sep to the rtl_folder
subModule_rtl_folder = ''       # defailt is the name of topModule
# =============================================================================================================================================
# get a top verilog file and analysis what sub module we need and add it to the all file list
def getSubModule(in_file):
    subModuleList = []
    # print(in_file)
    with open(in_file,'r') as f:
        verilog_code = f.read()
    subModule_Matches = re.findall(verilog_code_pattern,verilog_code)
    for match in subModule_Matches:
        if(match == 'module'):                # skip the unreachable match 
            continue
        if(match == 'begin'):                 # skip the unreachable match 
            continue
        match_path = rtl_folder+match+'.v'
        # print("match path :",match_path)
        if not os.path.exists(match_path):    # skip the unreachable match 
            continue
        subModuleList.append(match)           # add the sub module name to the submodule list
        allFileList.append(match)             # add the sub module name to the allFileList list
    return subModuleList                      # retern the sub list for a new find progress

# =============================================================================================================================================
# redo the above step untill the subModulelist is null
def getAllSubModule(in_file):
    in_f = in_file                            # get the file name or path
    sub_list = getSubModule(in_f)             # use the method to get sub module 
    if (sub_list == []):                      # if no sub module , then interrupt
        return
    for f in sub_list:                        # if has sub module, do the recursion
        in_f = rtl_folder+f+'.v'
        if not os.path.exists(in_f):          # skip the unexisted file
            continue
        else:
            getAllSubModule(in_f)             # recurive find the sub module,just like two x tree

# =============================================================================================================================================
# copy all the file to the destfolder
def copySubModuleFile(destfolder,sub_list):
    if not os.path.exists(destfolder):        # make sure the destfolder is existed
        os.makedirs(destfolder)               # if no , make a dir 
        print("Folder",destfolder,"created sucessfully") 
    else:
        print("Folder",destfolder,"is already existed") # if yes, do nothing
    print('='*5," start copy file ",'='*5)      
    for f in sub_list:                        # to copy all the sub module file in sub_list
        tmp_f_path = rtl_folder+f+'.v'        # get the file path 
        if os.path.exists(tmp_f_path):        # make sure the file is existed in the rtl_folder
            shutil.copy(tmp_f_path,destfolder)# copy it to destfolder
        else:
            print("the file ",tmp_f_path,"is not extisted")
    print('='*5," copy submodule file ok ",'='*5) # give a success message

# =============================================================================================================================================
# define help_print
def help_print():
    print("-------------------------------------------")
    print("****v1.1 craft by bosc nanhu v2 project*****")
    print("+  python3 findModule.py rtl_module_name.v")  # this is the useage tips
    print("+  Args       :",len(sys.argv))               
    if (len(sys.argv) > 1):
       print("+  Module name:",sys.argv[1])
    print("-------------------------------------------")

# =============================================================================================================================================
# that is main function
def my_main():
    #========================================================================
    global allFileList
    global topModule
    global subModule_rtl_folder
    global verilog_code_pattern
    global rtl_folder
    #========================================================================
    if len(sys.argv) == 1 :
        help_print()
        return 
    help_print()
    curTime = datetime.now().strftime("_%Y_%m_%d_%H_%M")
    if not os.path.exists(rtl_folder):    # make sure the rtl_folder user defined
        print("pleas check the user define rtl_folder if is set right")
        return
    in_f = rtl_folder+sys.argv[1]         # get the module file path
    topModule = sys.argv[1].split('.')[0] # get the top module name
    allFileList.append(topModule)         # set the top module to the file list
    #========================================================================
    getAllSubModule(in_f)                 # start the find progress
    #========================================================================
    print(" all the file list :")
    inc_num = 0
    allFileList = list(set(allFileList))  # remove the repeat list unit
    allFileList.sort()                    # sort the list
    for i in allFileList:                 # print all the list
        inc_num = inc_num+1
        print(inc_num,"----",i)
    #=========================================================================
    print("-------------------------------------------")
    print("start genarate the rtl module code file list")
    cur_dir = os.getcwd()                           # get the current folder path
    # USER TO DO : set the defalt topModule_rtl_f
    # topModule_rtl_f = topModule+'_rtl_v1+'.f'     # this is old set
    topModule_rtl_f = topModule+'_rtl'+curTime+'.f' # get the current file name   
    with open(topModule_rtl_f,'w') as rtl_f:        # write to the f file 
        for i in allFileList:
            insert_file_path = cur_dir+cur_sep+rtl_folder+i+".v"
            rtl_f.write(insert_file_path+'\n')
    print("-------------------------------------------")
    # ======================================================================
    # USER TO DO : set the defalt subModule_rtl_folder
    # subModule_rtl_folder = topModule+"_v1"            # this is old set
    subModule_rtl_folder = topModule+curTime            # set the name of subModule_rtl_folder 
    copySubModuleFile(subModule_rtl_folder,allFileList) # copy the file to the subModule_rtl_folder
    print("******************end*********************")
# =============================================================================================================================================

if __name__ == "__main__":
    my_main()