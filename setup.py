# -*- coding: utf-8 -*-

"""
利用Python脚本从svn获取最新版本信息，然后利用py2exe进行打包，最新进行相应的清理操作
"""

import os
import time
import glob
import shutil
import subprocess
import sys
import stat
import zipfile
import json
from distribution import Distribution
from Cheetah.Template import Template


def change_package_fromLib(package_name):
    '''
        根据包名从python Lib中获取到包，替换library.zip中名字相同的包
    '''
    library_zippath = os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip'])
    library_path = os.getcwd() + os.sep + os.sep.join(['dist', 'library'])
    with zipfile.ZipFile(library_zippath, 'r') as zip_file:
        zip_file.extractall(path=library_path)
    shutil.rmtree(library_path + os.sep + package_name)
    for item in [package_name]:
        package = __import__(item)
        package_path = os.path.dirname(package.__file__)
        shutil.copytree(package_path, library_path + os.sep + package_name)

    os.remove(os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip']))
    addFolderToZip(library_path, 'dist\library.zip')
    shutil.rmtree(library_path)


def change_package_fromLocal(package_name):
    '''
        根据包名从当前项目中获取到包，替换library.zip中名字相同的包
    '''
    library_zippath = os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip'])
    library_path = os.getcwd() + os.sep + os.sep.join(['dist', 'library'])
    with zipfile.ZipFile(library_zippath, 'r') as zip_file:
        zip_file.extractall(path=library_path)
    shutil.rmtree(library_path + os.sep + package_name)
    for item in [package_name]:
        package_path = os.getcwd() + os.sep + item
        shutil.copytree(package_path, library_path + os.sep + package_name)

    os.remove(os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip']))
    addFolderToZip(library_path, 'dist\library.zip')
    shutil.rmtree(library_path)


def addFolderToZip(folder, zip_filename):
    '''
        将文件夹foldler添加到名字为zip_filename的zip中去
    '''
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        def addhandle(folder, zip_file):
            for f in os.listdir(folder):
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path):
                    print 'Add file: %s' % full_path
                    zip_file.write(full_path, full_path.split('library\\')[1])
                elif os.path.isdir(full_path):
                    print 'add folder: %s' % full_path
                    addhandle(full_path, zip_file)
        addhandle(folder, zip_file)


def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


def get_py2exe_datafiles(datapath, relativehead):
    head, tail = os.path.split(datapath)
    d = {}
    for root, dirs, files in os.walk(datapath):
        files = [os.path.join(root, filename) for filename in files]
        root = root.replace(tail, relativehead)
        root = root[root.index(relativehead):]
        d[root] = files
    return d.items()


def write_file(filename, content):
    '''
        将相应的content写入filename中去
    '''
    fd = open(filename, "w")
    fd.write(content)
    fd.close()


def get_sw_distributedname(sw_name, sw_version, project_svnpath):
    '''
    输入：
        sw_name : 软件名称
        sw_version: 软件版本号
        project_svnpath: 项目在svn中的路径
    输出：
        project_localpath： 项目在本地的路径
        distributedname：软件发行版本号
    作用：
        从svn仓库将项目checkout到本地，获取svn版本号，构建软件发行版本号distributedname
    '''
    project_localpath = os.sep.join([os.getcwd(), sw_name])
    subprocess.call('svn co %s %s' % (project_svnpath, project_localpath))
    svn_info = subprocess.check_output(['svn', 'info'])
    svn_infolines = svn_info.split(os.linesep)
    svn_version = svn_infolines[6][6:]
    buildtime = time.strftime("%Y%m%d", time.localtime(int(time.time()))).decode('UTF8')
    distributedname = '%s-v%s-r%s-b%s' % (sw_name, sw_version, svn_version, buildtime)
    info = [svn_version, buildtime]
    return project_localpath, distributedname, info


def clearsvn(sw_path):
    '''
    输入：
        sw_path: 项目软件路径
    输出：
        空
    作用：
        调用shutil.rmtree进行整个文件夹删除
    '''
    for (p, d, f) in os.walk(sw_path):
        if p.find('.svn') > 0:
            shutil.rmtree(p)


def getfiles(path):
    '''
        获取指定path下的所有文件列表
    '''
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.sep.join([dirpath, filename]))
    return files


def getjsfiles(path):
    '''
        获取指定path下的所有后缀为.js的文件列表
    '''
    jsfiles = []
    files = getfiles(path)
    for filename in files:
        if filename[-3:] == '.js':
            jsfiles.append(filename)
    return jsfiles


def jsminhandle(jsfiles):
    '''
        压缩所有js文件
    '''
    yuicompressor_path = os.sep.join([os.getcwd(), 'yuicompressor-2.4.6.jar'])
    for jsfile in jsfiles:
        if jsfile[-3:] == '.js':
            print 'js min : %s' % jsfile
            os.system('java -jar %s --type js -o  %s %s' % (yuicompressor_path, jsfile, jsfile))


def getpyfiles(path):
    '''
        获取指定path下的所有后缀为.py的文件列表
    '''
    pyfiles = []
    files = getfiles(path)
    for filename in files:
        if filename[-3:] == '.py':
            pyfiles.append(filename)
    return pyfiles


def py2pyohandle(pyfiles):
    '''
        将指定的py文件编译为pyo文件
    '''
    for filename in pyfiles:
        if os.path.basename(filename) not in ['ifpms.py', 'userifpms.py', 'mark.py']:
            print 'py 2 pyo: %s' % filename
            os.system("C:\Python25\python.exe -m py_compile %s" % filename)
            os.remove(filename)


def generate_markpy(sw_path, product='default'):
    content = '''
    #!/usr/bin/env python
    # -*- coding: UTF8 -*-
    logo = '%s'
    ''' % product
    import codecs
    filepath = os.sep.join([sw_path, 'extensions', 'ifpms@ov-orange.com', 'pylib'])
    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(content)


def generate_license(sw_path, product='default'):
    src = os.sep.join([sw_path, 'license.%s.txt' % product])
    dst = os.sep.join([sw_path, 'chrome', 'license.txt'])
    os.rename(src, dst)


def generate_chromemanifest(sw_path, product='default'):

    content = '''
    content ifpms jar:ifpms.jar!/content/
    content etc etc/
    content wav wavs/
    content sample sample/
    content mapImg mapImg/
    skin ifpms default jar:ifpms.jar!/skin/%s/
    locale ifpms zh-CN jar:ifpms.jar!/locale/zh-CN/
    locale ifpms en-US jar:ifpms.jar!/locale/en-US/
    ''' % product
    import codecs
    filepath = os.sep.join([sw_path, 'chrome', 'chrome.manifest'])
    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(content)


def generate_nsi(sw_name, build, datatime):
    content = '''
    '''
    import codecs
    filepath = os.sep.join([path, '%s-setup.nsi' % sw_name])
    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(content)


def auto_iss(template, nameSpace):
    t = Template(template, searchList=[nameSpace])
    code = unicode(t)
    return code


templateDef_iss ='''
; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "$MyAppName"
#define MyAppVersion "$MyAppVersion"
#define MyAppPublisher "$MyAppPublisher"
#define MyAppURL "$MyAppURL"
#define MyAppExeName "$MyAppExeName"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8136D515-0A08-46A2-85CD-5BA9EC33D909}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=$distributedname
SetupIconFile=$SetupIconFile
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "$source_exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "$source_folder"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
'''


if __name__ == '__main__':
    # 从config中获取软件的基本信息
    import config
    sw_name = config.__softwarename__
    sw_version = config.__version__
    sw_publisher = config.__author__
    sw_url = config.__url__
    sw_description = config.__description__
    sw_logoico = config.__logoico__

    #生成软件版本号
    svn_version = '100'
    t = time.gmtime()
    buildtime = ''.join([str(i) for i in [t.tm_year, t.tm_mon, t.tm_mday]])
    info = [svn_version, buildtime]
    distributedname = distributedname = '%s-v%s-r%s-b%s' % (sw_name, sw_version, svn_version, buildtime)

    # 在options中生成软件版本信息文件
    sw_info = json.dumps({
        "sw_name": sw_name, 
        "sw_version": 'v%s' % sw_version, 
        "svn_version": 'r%s' % info[0], 
        "buildtime": 'b%s' % info[1]},
        indent=3)
    write_file(os.sep.join([os.getcwd(), 'options', 'ver.json']), sw_info)

    # 利用模板自动生成setup.iss打包脚本
    setup_iss_file = '%s-setup.iss' % sw_name
    nameSpace = {
        'MyAppName': sw_name,
        'MyAppVersion': sw_version,
        'MyAppPublisher': sw_publisher,
        'MyAppURL': sw_url,
        'MyAppExeName': '%s.exe' % sw_name,
        'distributedname': distributedname,
        'SetupIconFile': sw_logoico,
        'source_exe':  os.sep.join([os.getcwd(), 'dist', '%s.exe' % sw_name]),
        'source_folder': os.sep.join([os.getcwd(), 'dist', '*'])
    }
    setup_iss_content = auto_iss(templateDef_iss, nameSpace)
    with open(setup_iss_file, 'w') as f:
        f.write(setup_iss_content)

    # 利用py2exe将项目打包成可执行文件
    if os.name == "nt":
        dist = Distribution()
        dist.vs2008 = None
        dist.setup(
                name=sw_name,
                version=sw_version,
                description=u"Application based on PyQt4",
                script=os.sep.join([os.getcwd(), 'QMain.py']),
                target_name='QMarkdowner',
                icon=sw_logoico)

        dist.add_modules('PyQt4')
        dist.bin_excludes += ["libzmq.dll"]
        dist.includes += []
        # dist.data_files += matplotlibdata_files
        dist.data_files += get_py2exe_datafiles(os.sep.join([os.getcwd(), 'utildialog', 'utildialogskin']), 'utildialogskin')
        dist.data_files += [('phonon_backend', [
                'C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
                ]),
            ('imageplugins', [
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qgif4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qjpeg4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qsvg4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qico4.dll',
            ])]

        dist.excludes += [
                  '_gtkagg',
                  '_tkagg',
                  '_agg2',
                  '_cairo',
                  '_cocoaagg',
                  '_fltkagg',
                  '_gtk',
                  '_gtkcairo', ]

        dist.build('py2exe')

    '''
        拷贝响应的图片皮肤和与项目有关的资源文件到打包目录
    '''

    for item in ['skin', 'Bootstrap Metro UI CSS', 'options', 'themecss', 'doc', 'MaDeEditor']:
        shutil.copytree(os.getcwd() + os.sep + item, os.getcwd() + os.sep + os.sep.join(['dist', item]))

    for item in ['log']:
        os.mkdir(os.getcwd() + os.sep + os.sep.join(['dist', item]))

    change_package_fromLocal('Cheetah')

    # 调用外面iscc 运行setup.iss, 生成安装版本exe
    os.system("iscc %s" % setup_iss_file)

    for key in ['build', 'dist', sw_name, 'QMarkdowner-setup.iss']:
        path = os.getcwd() + os.sep + key
        delete_file_folder(path)
