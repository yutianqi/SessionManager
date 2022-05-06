

## TODO
1. ssm 
   ssm -a <nodeName> <ip> <port> <username> <password>
   ssm -a -f <filename>
   ssm -d <nodeId>
   
2. 
从csv文件生成：
a. profile配置
b. 登录配置
c. Session层级配置json
    ```json
    [
        {
            "nodeName": "L1-PT",
            "nodeType": "directory",
            "nodeId": "1",
            "childNodes": [
                {
                    "nodeName": "L2-region1",
                    "nodeType": "directory",
                    "nodeId": "2",
                    "childNodes": [
                        {
                            "nodeName": "L3-Master",
                            "nodeType": "directory",
                            "nodeId": "2",
                            "childNodes": [
                                {
                                    "nodeName": "L4-Master1_240",
                                    "nodeType": "session",
                                    "nodeId": "2",
                                    "ip": "192.168.0.240",
                                    "port": "22",
                                    "username": "ossuser",
                                    "password": "Fusionsolar@h00356474",
                                    "profileName": "PT_region1_master_Master1"
                                },
                                {
                                    "nodeName": "L4-Master2_207",
                                    "nodeType": "session",
                                    "nodeId": "2",
                                    "ip": "192.168.0.207",
                                    "port": "22",
                                    "username": "ossuser",
                                    "password": "Fusionsolar@h00356474",
                                    "profileName": "PT_region1_master_Master2"
                                }
                            ]
                        },
                        {
                            "nodeName": "L3-Disb",
                            "nodeType": "directory",
                            "nodeId": "3",
                            "childNodes": [
                                {
                                    "nodeName": "L4-Disb1_10",
                                    "nodeType": "session",
                                    "nodeId": "2",
                                    "ip": "192.168.0.10",
                                    "port": "22",
                                    "username": "ossuser",
                                    "password": "Fusionsolar@h00356474",
                                    "profileName": "PT_region1_disb_Disb1"
                                },
                                {
                                    "nodeName": "L4-Disb2_11",
                                    "nodeType": "session",
                                    "nodeId": "2",
                                    "ip": "192.168.0.11",
                                    "port": "22",
                                    "username": "ossuser",
                                    "password": "Fusionsolar@h00356474",
                                    "profileName": "PT_region1_disb_Disb2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    ```

1. ssls：读取Session层级配置json，列出Session分组列表，默认全量展开
    ```
    └── 1> PT1 
        └── 2> region1
            ├── 3> Master           
            │   ├── 4> Master1_240    
            │   └── 5> Master2_207
            ├── 6> Disb
            │   ├── 7> Disb1_10
            │   ├── 8> Disb1_10
            │   └── 9> Disb2_11
            └── 20> Other
                └── 21> Other1_21
    ```
   ssls | grep
   ssls -n 6        显示指定节点下的节点列表

   ssls -l <n>      展开到第n层
   ssls -a          平铺展示
   ssls -v          包含节点IP信息

2. 
   ssopen 6         如果节点为文件夹，递归打开指定节点下的所有Session
   ssopen 7         打开指定Session
   ssopen 7,8,9     打开多个Session
   ssopen 7-9       打开多个连续Session

   ssopen -t        新标签打开Session
   ssopen -w        新窗口打开Session，默认选项

3. 






# 技术点
iTerm2 python api



# Projects


https://github.com/search?q=iterm2+session


https://iterm2.com/python-api/tutorial/index.html


https://github.com/Peter-Nhan/Iterm2_Automate_sessions


https://github.com/ktont/iterm2-session


https://github.com/lilongen/xshell-to-iterm2


https://blog.csdn.net/weixin_46380571/article/details/108095237


