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
    # ShellSessionGenerator
        # ini
            使用ini文件指定路径相关配置
        # 优化README
            ini
        # commands
            export HISTSIZE=1000
        # 生成的配置中删掉
            "nodeType": "session",
            支持v2版本格式

    # 优化README
        chmod 755 /Users/yutianqi/Code/Github/SessionManager/ssmgr.py
        chmod 755 /Users/yutianqi/Code/Github/SessionManager/jump.exp
    # sso
        未指定节点ID提示
        如果存在找不到节点，则直接提示是否要继续
        如果只打开一个节点，要考虑是否要新开tab
            # 单个tab
                默认     在当前tab打开
                -t      在新tab打开
                -w      在新窗口打开
            # 多个tab
                默认/-t  在当前窗口，新开多个tab打开
                -w      在新窗口，新开多个tab打开

    # ssm
        整合ShellSessionGenerator
        ShellSessionGenerator增加独立的nodeId生成逻辑函数
        相同ProjectName要有覆盖提示

    # 高亮显示关键字
        https://blog.csdn.net/qq_38882327/article/details/111034039
        \033[***开头，\033[0m
        print('默认颜色')
        print('\033[1;30;41m')     #下一目标输出背景为红色，颜色为黑色高亮显示
        print('*' * 50)
        print('\033[7;31;37m错误次数超限，用户已被永久锁定，请联系管理员！\033[1;30;41m')  #字体颜色红色反白处理，下一目标输出背景为红色，颜色为黑色高亮显示
        print('*' * 50)
        print('\033[0m')           #下一目标输出恢复为默认设置
        print('已恢复')

        显示方式：0（默认）、1（高亮）、22（非粗体）、4（下划线）、24（非下划线）、 5（闪烁）、25（非闪烁）、7（反显）、27（非反显）
        前景色：30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋 红）、36（青色）、37（白色）
        背景色：40（黑色）、41（红色）、42（绿色）、 43（黄色）、44（蓝色）、45（洋 红）、46（青色）、47（白色）

        "abc\033[0;37;mdef\033[0mhig"


# 技术点
    iTerm2 python api
        https://iterm2.com/python-api/tutorial/index.html
    argparse
        https://cloud.tencent.com/developer/article/1509763

# Projects
    https://github.com/search?q=iterm2+session
    https://github.com/Peter-Nhan/Iterm2_Automate_sessions
    https://github.com/ktont/iterm2-session
    https://github.com/lilongen/xshell-to-iterm2
    https://blog.csdn.net/weixin_46380571/article/details/108095237


# TestCase
    ssl
    ssl -v
    ssl -n 5
    ssl -n 50

    sso

    ssm