
#include "template.h"
/*******************************************************************************
 * Definitions
 ******************************************************************************/



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

static uint32_t _device_get_index4(void)
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

