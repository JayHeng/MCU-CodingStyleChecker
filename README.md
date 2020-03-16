# MCUXpresso SDK Coding Style

### 1.代码风格

> * 风格细则：https://github.com/JayHeng/MCUX-SDK-Coding-Style/blob/master/coding_style.md

### 2.代码模板

> * 头文件模板：https://github.com/JayHeng/MCUX-SDK-Coding-Style/blob/master/template.h
> * 源文件模板：https://github.com/JayHeng/MCUX-SDK-Coding-Style/blob/master/template.c

### 3.检查工具

　　MCUXpresso SDK Coding Style Checker 是恩智浦 SDK 驱动 C 代码风格配套检查工具，其功能类似于 JAVA 代码下的 [CheckStyle](https://github.com/checkstyle/checkstyle) 工具（默认绑定 Google 风格以及 Sun 规范），也类似于 [Linux](https://github.com/torvalds/linux) 下的 scripts/checkpatch.pl 脚本，只不过提供的规范检查没有这两个工具丰富，是一个轻量级的工具。此外本工具基于 PyQt5 做了一个简洁的 GUI，更适合普通 MCU 开发者使用。  

　　MCUXpresso SDK Coding Style Checker 主要功能如下：  

> * 支持选择单文件或整个文件夹  
> * 自动识别 .c/.h 后缀文件，但要保证文件是 UTF-8 或 ASCII 编码（即不能包含非英文字符）  
> * 支持检测五种通用注释头（Defintions/Variables/Prototypes/Code/API）  
> * 支持检测全局变量的命名规范（在Variables注释头下）
> * 支持检查函数名的命名规范（在Code注释头下）  

![](http://henjay724.com/image/github/MCUXpresso-SDK-CodingStyleChecker_v0.1.PNG)

