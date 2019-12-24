#include "mbed.h"

// Sensors drivers present in the BSP library
#include "stm32l475e_iot01_gyro.h"
#include "stm32l475e_iot01_accelero.h"

int main()
{
    int16_t pDataXYZ[3] = {0};
    float pGyroDataXYZ[3] = {0};

    printf("Start sensor init\n");


    BSP_GYRO_Init();
    BSP_ACCELERO_Init();

    while(1) {
        printf("\nNew loop, New sensor Read\n");

        BSP_GYRO_GetXYZ(pGyroDataXYZ);
        printf("\nGYRO_X = %.2f\n", pGyroDataXYZ[0]);
        printf("GYRO_Y = %.2f\n", pGyroDataXYZ[1]);
        printf("GYRO_Z = %.2f\n", pGyroDataXYZ[2]);

        BSP_ACCELERO_AccGetXYZ(pDataXYZ);
        printf("\nACCELERO_X = %d\n", pDataXYZ[0]);
        printf("ACCELERO_Y = %d\n", pDataXYZ[1]);
        printf("ACCELERO_Z = %d\n", pDataXYZ[2]);


        ThisThread::sleep_for(2000);

    }
}
