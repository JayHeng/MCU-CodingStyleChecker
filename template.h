/*
 * Copyright 20xx-20xx NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Revision History:
 * v0.1 - Initial Drop
 */

#ifndef _TEMPLATE_H_
#define _TEMPLATE_H_
/* 任何一个 .h 文件都需要包含上面格式的头文件保护宏，宏的命名与头文件名保持一致 */

/* 包含头文件代码 */
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
/*******************************************************************************
 * Definitions
 ******************************************************************************/

/* 公共(可被其他源文件使用)宏、枚举、结构体的定义 */

/* 枚举类型名使用下划线命名法，单词全小写，且以下划线开头。
   枚举元素名使用小骆驼峰法，但统一加 k 前缀 */
enum _device_mode
{
    kDeviceMode0    = 0x00U,
    kDeviceMode1    = 0x01U,
    kDeviceModeEnd  = 0x02U,
};

/* 结构体类型名使用下划线命名法，单词全小写，且以下划线开头。
   结构体成员名使用小骆驼峰法 */
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
/* #endif 后面需要加如上注释 */

#endif /* _TEMPLATE_H_ */
