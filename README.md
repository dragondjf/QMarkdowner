关于QMarkdowner的那些事
===================================================
###1. markdown 是什么？
 
+   大家都知道，markdown是一种适于网络编写的纯文本格式的标记语言，由一系列的符号标记和文本组成，在很多软件项目中常常采用markdown去撰写说明文档readme.md，传递项目的更新或特性，例如GitHub中每个开源项目都有一个readme.md。    
+   markdown的优势：
    + 简洁明了，易读易写    
    + 兼容html，独立于平台      
+   在计算机的世界很多人用他去编写Blog,读写发布快速方便，简单易用，如果你想快速记录你所想，如果你想在blog中快速发布你所想，markdown是值得学习使用的一个工具。
+  详情参见[markdown中文语法说明](http://wowubuntu.com/markdown/#philosophy)。

###2.QMarkdowner是什么？
 
+   既然markdown文档具备这些优势，在什么编辑器上撰写markdown格式文档？
+   开源中国[markdown编辑器](http://www.oschina.net/search?scope=project&q=markdown)集锦；
+   QMarkdowner是一个开源项目，目的就是使本已简单明了的markdown文本更加简洁明了，易读易写，成为markdown书写发布的利刃；
+   QMarkdowner特性：
    +   所见所得，书写与预览同步；
    +   支持导入外部markdown格式文档；
    +   全屏预览，五种主题切换，简洁美观；
    +   支持markdwon、html、pdf格式导出；

###3. QMarkdowner风格预览
所见所得，书写与预览同步

![编辑窗口][edit]

black主题预览     

![black][black]

white主题预览

![white][white]

github主题预览

![github][github]

evernote主题预览

![evernote][evernote]

jeklly主题预览

![jeklly][jeklyy]

###4. QMarkdowner涉猎的技术   
+ Python2.7    
+ qframer.qt    
    + QMainwidow  ----  **核心窗口部件**
    + QStackWidget  ---- **堆控件**
    + QtWebkit  ----  **嵌入浏览器控件**
    + qss ---  **控制程序的外观**
+ Web   
    + Made  ----  **chrome markdown插件技术**
    + bootstrap metro css  ----  **Metro风格**
    + markdown css  ----  **风格预览**
    + highlight.js  ----  **代码语法高亮**
+ markdown  ----  **python markdown转换成html的库**    
+ cheetah  ---- **html模板，与python协调动态生成html**
+ wkhtmltopdf  ---- **html转pdf第三方库**
+ py2exe ----  **将py程序转换成exe**
+ inno setup ----  **打包发布工具**
+ 待续。。。。。。
+ 附上一张软件架构图
![QFramer][QFramer]

###5. 致敬
+ 感谢：   
  + Chrome插件MaDe，highlight.js, wkhtmltopdf等开源项目；
  + Good朋友jack_zh；
  + ulipad和uliweb作者limodou；
  + PyQt and PySide群里的樱桃大丸子等大神.   
+    联系邮箱：dragondjf@gmail.com, ding465398889@163.com
+    联系QQ：465398889
+    GitHub地址：https://github.com/dragondjf/
+    软件发布地址：http://yunpan.cn/cHv5RfPyzEMdY （提取码：fef6）
+    刻骨铭心：感谢开源精神，分享成就自我！

###6.反馈改进     
+ 欢迎大家拍砖，一起营造markdown撰写**利刃QMarkdowner**
+ 下一步功能增强：
    + 加入**markdown文件管理功能**，打造成利用markdown写作的利器，帮助有志利用markdown写作的朋友快速撰写书稿；
    + 加入**一键分享发布功能**，能快速集成到evernote、blog、github等第三方平台中去；
+ 欢迎各位大神品足，暂时意见反馈请通过一下方式反馈：
    + 邮箱：dragondjf@gmail.com
    + QQ: 465398889
    + 电话：13986218913

[QFramer]: http://img0.ph.126.net/TyGYLcYRAvRsa0DMrCORzw==/6597693189751234389.jpg
[edit]:  http://img2.ph.126.net/w9buqTFZpcSCwBMJ5oEZhA==/2232096565415514338.png
[black]: http://img1.ph.126.net/z8wFRtEpJReRE4dL0oiFdg==/2265592087644079252.png
[white]: http://img1.ph.126.net/XpfGKX6kfhdC3oPgDjq-Ow==/1689694285294341322.png
[github]: http://img1.ph.126.net/oiAEpMBTbSzfmVpDu0sgAA==/2759299196712461656.png
[evernote]: http://img0.ph.126.net/fEI3NyFyJP_guV04NSWzqQ==/1474647403087135956.png
[jeklyy]: http://img0.ph.126.net/9nN6mdFW90m_VNglRaU8mw==/1991716935304705011.jpg
