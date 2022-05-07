# 功能设计
1. ssm 
   ssm -a <nodeName> <ip> <port> <username> <password>：交互式新增配置项
   ssm -a -f <filename> ：从csv文件生成登录配置到sessions.json
   ssm -d <nodeId>：删除配置项
   
2. ssl
   ssl：读取Session层级配置json，列出Session分组列表，默认全量展开
     └── 21> Other1_21
   ssl | grep
   ssl -n 6        显示指定节点下的节点列表
   ssl -l <n>      展开到第n层
   ssl -a          平铺展示
   ssl -v          包含节点IP信息

3. sso
   sso 6            如果节点为文件夹，递归打开指定节点下的所有Session
   sso 7            打开指定Session
   sso 7,8,9        打开多个Session
   sso 7-9          打开多个连续Session

   sso -t           新标签打开Session
   sso -w           新窗口打开Session，默认选项

# TODO
    # ini
        使用ini文件指定路径相关配置
    # 优化README
        ini
        chmod 755 /Users/yutianqi/Code/Github/SessionManager/ssmgr.py
        chmod 755 /Users/yutianqi/Code/Github/SessionManager/jump.exp
    # commands
        export HISTSIZE=1000
    # sso
        未指定节点ID提示
    # ssm
        整合ShellSessionGenerator
        ShellSessionGenerator增加独立的nodeId生成逻辑函数
        相同ProjectName要有覆盖提示

        



# 技术点
    iTerm2 python api


# Projects
    https://github.com/search?q=iterm2+session
    https://iterm2.com/python-api/tutorial/index.html
    https://github.com/Peter-Nhan/Iterm2_Automate_sessions
    https://github.com/ktont/iterm2-session
    https://github.com/lilongen/xshell-to-iterm2
    https://blog.csdn.net/weixin_46380571/article/details/108095237


