# Web-UI-test
一个网页自动化测试项目案例
从上到下依次为 测试用例文件夹， 配置文件夹， 数据文件夹， 存放结果文件夹， 封装关键字文件夹
实现了 老东家平台页面部分功能测试，部分功能因数据加密暂无法实现，在unittest运行框架下最终23个测试断言错误1个，跳过3个，成功19个
其中log数据可实时输出控制台也可写入result文件夹下log文件中保存
因ddt数据加载时导致测试用例名称改变，进而导致非unittest框架下找不到测试用例，所以想进行HTTPTestRunner报告生成需要进一步努力，或者下一步改用pytest框架结合其他报告生成模块来实现
![image](https://user-images.githubusercontent.com/64000814/169347768-2aa349ac-700d-440e-a82e-eef8a6f326d6.png)
![image](https://user-images.githubusercontent.com/64000814/169347507-f386d02c-73a1-4fd0-9b5b-e57852d83232.png)
![image](https://user-images.githubusercontent.com/64000814/169347618-9086a547-17e5-4e5c-8c76-41cc3d45b45a.png)
