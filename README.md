# mcux_sdk_coding_style

### 1.命名

#### 1.1 变量

变量命名使用 CamelCase (小骆驼峰法)，即第一个单词以小写字母开始，第二个单词以及后面的每一个单词的首字母大写，例如 myVariableName

> * 作用域可在文件外的全局变量加 g\_ 前缀，如 g\_myVariableName
> * 使用 static 修饰的全局变量加 s\_ 前缀，如 s\_myVariableName
> * 局部变量不加任何前缀，如 myVariableName
> * 其他如 volatile, const 修饰或指针型变量，无需任何特殊表示
> * 命名中的大部分单词都不要缩写，除非是相当流行的缩写，如 init 或 config

#### 1.2 宏

宏命名使用下划线命名法，单词全大写，例如 MY_MACRO_NAME

#### 1.3 枚举

枚举类型的命名混合了多种命名法，且加了一些特殊前后缀

> * 枚举类型名使用下划线命名法，单词全小写，且以下划线开头
> * 枚举元素名使用小骆驼峰法，但统一加 k 前缀
> * 可用 typedef 重命名枚举类型名，使用下划线命名法，但需加 \_t 后缀
> * 枚举变量名使用小骆驼峰法

```C
typedef enum _my_enumeration_name
{
    kMyEnumerator0     = 0x00U,
    kMyEnumerator1     = 0x01U,

    kMyEnumeratorEnd   = 0x02U,
} my_enumeration_name_t;

static my_enumeration_name_t s_myEnumVariableName;
```

#### 1.4 结构体

结构体类型的命名混合了多种命名法，且加了一些特殊前后缀

> * 结构体类型名使用下划线命名法，单词全小写，且以下划线开头
> * 结构体成员名使用小骆驼峰法
> * 可用 typedef 重命名结构体类型名，使用下划线命名法，但需加 \_t 后缀
> * 结构体变量名使用小骆驼峰法

```C
typedef struct _my_struct_name
{
    uint32_t myStructMember0;
    uint32_t myStructMember1;
} my_struct_name_t;

static my_struct_name_t s_myStructVariableName;
```

#### 1.5 函数

函数命名使用 Pascal (大骆驼峰法)，即把变量名称的第一个字母也大写，例如 MyFunctionName

> * 函数命名可由 [Action][Feature] 组成，动作在前，特性在后。如 InitClock()、EnableInterrupts()
> * 一系列同类函数，可加 MODULE\_ 前缀，前缀单词全大写。如 SD 卡操作的系列函数，可为 SD_PowerOnCard()、SD_PowerOffCard()

### 2.代码体

#### 2.1 排版

> * 永远不要使用 Tab 键（使用 4 个空格代替 Tab），需要以 4 个空格为单位的缩进
> * 换行符应使用 "unix"(LF)，而不是windows(CR + LF)
> * 文件结尾需空一行

#### 2.2 花括号

不使用 K&R 风格花括号，左右括号都需要独占一行

#### 2.3 局部变量定义

局部变量定义应总是放在所在最小作用域(即最近的 {} 内)里的最前面，并且一行代码仅定义一个变量

```C
void MyFunctionName(void)
{
    uint8_t myVariableName0;
    uint8_t myVariableName1;

    /* 代码体 */

    for (;;)
    {
        uint8_t myVariableName2;

        /* 代码体 */
    }
}
```

#### 2.4 数字

代码中所有无符号整型数字，均应加 "U" 后缀

```text
Hex: 0x1234ABCDU
Dec: 1234U
```

#### 2.5 注释

仅使用 /\* \*/ 来注释

```C
/* 注释风格1，单独占一行 */
uint8_t i = 0;

for (; i < 5;)
{
    i++; /* 注释风格2，与代码共享一行 */
}
```

#### 2.6 条件编译

\#endif 后面需要加如下注释

```C
#if MY_MACRO_NAME

/* 代码体 */

#endif /* MY_MACRO_NAME */
```

#### 2.7 头文件保护宏

任何一个 .h 文件都需要包含下面格式的头文件保护宏代码，宏的命名与头文件名保持一致。如文件名为 hello\_world.h，则宏名为 \_HELLO\_WORLD\_H\_

```C
#ifndef _HEADER_FILENAME_
#define _HEADER_FILENAME_

/* 头文件内容 */

#endif /* _HEADER_FILENAME_ */
```

### 3.整体模板
#### 3.1 源文件(.c)
```C

/* 包含头文件代码 */

#include "hello_world.h"

/*******************************************************************************
 * Definitions
 ******************************************************************************/

/* 私有(仅本源文件内使用)宏、枚举、结构体的定义 */

enum _device_mode
{
    kDeviceMode0    = 0x00U,
    kDeviceMode1    = 0x01U,

    kDeviceModeEnd  = 0x02U,
};

/*******************************************************************************
 * Variables
 ******************************************************************************/

/* 所有全局变量(外部，静态，常量，指针)的定义 */

uint32_t g_deviceIndex = 0;

static device_config_t s_deviceConfig;

const uint32_t g_maxDevices = MAX_DEVICES;

static uint8_t *g_deviceData;

/*******************************************************************************
 * Prototypes
 ******************************************************************************/

/* 内部函数(即 static 修饰)的声明 */

static uint32_t GetDeviceIndex(void);

/*******************************************************************************
 * Code
 ******************************************************************************/

/* 所有函数(外部，内部)的定义 */

void InitDevice(void)
{
    s_deviceConfig.index = 1;
    s_deviceConfig.mode = kDeviceMode1;
    memset(s_deviceConfig.data, 5, sizeof(s_deviceConfig.data));
    s_deviceConfig.isEnabled = true;
}

static uint32_t GetDeviceIndex(void)
{
    return s_deviceConfig.index;
}

int main(void)
{
    InitDevice();
    g_deviceIndex = GetDeviceIndex();

    PRINTF("hello world.\r\n");

    while (1)
    {
    }
}

```

#### 3.2 头文件(.h)

```C
#ifndef _HELLO_WORLD_H_
#define _HELLO_WORLD_H_

/* 包含头文件代码 */

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

/*******************************************************************************
 * Definitions
 ******************************************************************************/

/* 公共(可被其他源文件使用)宏、枚举、结构体的定义 */

#define MAX_DEVICES  (128U)

typedef struct _device_config
{
    uint32_t index;
    uint32_t mode;
    uint8_t data[16];
    bool isEnabled;
} device_config_t;

/* 外部全局变量的声明 */

extern uint32_t g_deviceIndex;

extern const uint32_t g_maxDevices;

/*******************************************************************************
 * API
 ******************************************************************************/

#if defined(__cplusplus)
extern "C" {
#endif /*_cplusplus*/

/* 外部函数(可加 extern 修饰)的声明 */

void InitDevice(void);

#if defined(__cplusplus)
}
#endif /*_cplusplus*/

#endif /* _HELLO_WORLD_H_ */

```

