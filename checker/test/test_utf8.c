
#include "template.h"
/*******************************************************************************
 * Definitions
 ******************************************************************************/

#define MAX_devices0   (128U)
#define MAX_devices1(a, b)  (a+b)
#define _MAX_DEVICES2  (128U)

enum device_mode0
{
    kDeviceMode0    = 0x00U,
};

enum _DEVICE_mode1
{
    kDeviceMode0    = 0x00U,
};

typedef enum _device_mode2
{
    kDeviceMode0    = 0x00U,
} _device_mode2_t;

typedef enum _device_mode3
{
    kDeviceMode0    = 0x00U,
} DEVICE_mode3_t;

typedef enum _device_mode4
{
    kDeviceMode0    = 0x00U,
} DEVICE_mode4;

typedef enum _device_mode5
{
    deviceMode0     = 0x00U,
} device_mode5_t;

typedef enum _device_mode6
{
    kDeviceMode0    = 0x00U,
    kDeviceMode1,
    kdeviceMode2    = 0x02U,
} device_mode6_t;

struct device_config0
{
    uint32_t index;
};

struct _DEVICE_config1
{
    uint32_t index;
};

typedef struct _device_config2
{
    uint32_t index;
} _device_config2_t;

typedef struct _device_config3
{
    uint32_t index;
} DEVICE_config3_t;

typedef struct _device_config4
{
    uint32_t index;
} DEVICE_config4;

typedef struct _device_config5
{
    uint32_t Index;
} device_config5_t;

typedef struct _device_config6
{
    uint32_t index;
    uint32_t mo_de;
} device_config6_t;

/*******************************************************************************
 * Variables
 ******************************************************************************/

uint32_t g_deviceIndex0, g_deviceIndex1;   /* fake comment. */
uint32_t *deviceIndex2       = 0;
uint32_t *deviceIndex3 \
        = 0;
uint32_t **deviceIndex4;
static uint32_t deviceIndex5 = 0;
uint32_t deviceIndex6[100];
uint32_t g_DeviceIndex7;
uint32_t g_device_index8;
uint32_t g__deviceIndex9;
  uint32_t g_2deviceIndex10;

static device_config_t deviceConfig = {    /* fake comment. */
#if defined(MAX_DEVICES)
    .index = MAX_DEVICES,
#else
    .index = 1,
#endif
    .mode = 2,
    };

/*******************************************************************************
 * Prototypes
 ******************************************************************************/

/*******************************************************************************
 * Code
 ******************************************************************************/

static uint32_t getDeviceIndex0(uint8_t arg0,
                                uint8_t arg1)
{
    return s_deviceConfig.index;
}

static uint32_t Get_DeviceIndex1(void)
{
    return s_deviceConfig.index;
}

static uint32_t DEVICE_getIndex2(void) {
    return s_deviceConfig.index;
}

static uint32_t DEVICE_Get_Index3(void)
{
    return s_deviceConfig.index;
}

static uint32_t _DEVICE_GetIndex4(void)
{
    return s_deviceConfig.index;
}

static uint32_t _device_get_index5(void)
{
    return s_deviceConfig.index;
}

int main(void)
{
    uint8_t i = 0;
    uint8_t j = 0;

    for (; i + j < 5;)
    {
        i++;
        j++;
    }

    while (1)
    {
    }
}

