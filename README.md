# 简介使
邮箱代理是一个期末大作业项目。邮箱代理能够实现QQ、网易邮箱的发送和接收，并且能够支持下载邮件到本地。同时拥有相对完善的用户交互界面。
# 如何使用
直接下载python代码，将所有的库全部导入，即可运行。
进入主窗口选择自己的邮箱类型，填写邮箱号，填写授权码即可进行邮件的发送和下载。
关于授权码的获取[点击这里](https://blog.csdn.net/weixin_43760266/article/details/122679171?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522171730841516800188552953%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=171730841516800188552953&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-122679171-null-null.142^v100^pc_search_result_base1&utm_term=qq%E9%82%AE%E7%AE%B1%E6%8E%88%E6%9D%83%E7%A0%81%E5%A6%82%E4%BD%95%E8%8E%B7%E5%8F%96&spm=1018.2226.3001.4187)
## 安装依赖
为了确保所有导入的包都能正常使用，你需要安装以下Python库。可以使用`pip`命令来安装这些库。以下是安装这些库的命令：

```
pip install PyQt5
pip install smtplib
pip install imaplib
pip install email
pip install imbox
pip install itertools
pip install multiprocessing
pip install traceback
```
  
请注意，部分库（如`smtplib`、`imaplib`、`email`、`itertools`、`multiprocessing`和`traceback`）是Python标准库的一部分，不需要额外安装，它们会随Python安装一起提供。
因此，你只需要安装第三方库：

```
pip install PyQt5 imbox
```

最终的安装命令如下：


```
pip install PyQt5 imbox
```

  

这将确保你所需要的所有库都已安装并可用于导入。
