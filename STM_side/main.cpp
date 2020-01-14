/* WiFi & Sensor
 * Copyright (c) 2016 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "mbed.h"
#include "TCPSocket.h"
#include "TCPServer.h"

#include "stm32l475e_iot01_gyro.h"
#include "stm32l475e_iot01_accelero.h"
#define SCALE_MULTIPLIER    0.004
DigitalOut led(LED1);
DigitalOut errled(LED3);

DigitalOut intled(LED4);
WiFiInterface *wifi;

InterruptIn button(USER_BUTTON);
EventQueue queue;
const char *sec2str(nsapi_security_t sec)
{
    switch (sec) {
        case NSAPI_SECURITY_NONE:
            return "None";
        case NSAPI_SECURITY_WEP:
            return "WEP";
        case NSAPI_SECURITY_WPA:
            return "WPA";
        case NSAPI_SECURITY_WPA2:
            return "WPA2";
        case NSAPI_SECURITY_WPA_WPA2:
            return "WPA/WPA2";
        case NSAPI_SECURITY_UNKNOWN:
        default:
            return "Unknown";
    }
}
float fixnumber(float num){
    if(num>=0){
        num+=10000;
    }
    else{
        
        num=-num;
         num+=10000;
    }
   return num;
}

int fixSymbol(float num){
    if(num>=0){
        return 0;}
    else{
        return 1;
    
    }
}
int scan_demo(WiFiInterface *wifi)//this function is to scan all hotspots nearby(up to 15),sometimes it will fail.
{
    
    WiFiAccessPoint *ap;

    printf("Scan:\n");

    int count = wifi->scan(NULL,0);

    if (count <= 0) {
        printf("scan() failed with return value: %d\n", count);
        return 0;
    }

    /* Limit number of network arbitrary to 15 */
    count = count < 15 ? count : 15;

    ap = new WiFiAccessPoint[count];
    count = wifi->scan(ap, count);

    if (count <= 0) {
        printf("scan() failed with return value: %d\n", count);
        return 0;
    }

    for (int i = 0; i < count; i++) {
        printf("Network: %s secured: %s BSSID: %hhX:%hhX:%hhX:%hhx:%hhx:%hhx RSSI: %hhd Ch: %hhd\n", ap[i].get_ssid(),
               sec2str(ap[i].get_security()), ap[i].get_bssid()[0], ap[i].get_bssid()[1], ap[i].get_bssid()[2],
               ap[i].get_bssid()[3], ap[i].get_bssid()[4], ap[i].get_bssid()[5], ap[i].get_rssi(), ap[i].get_channel());
    }
    printf("%d networks available.\n", count);

    delete[] ap;
    return count;
    


}
void acc_server(NetworkInterface *net)//collect data and send via socket
{
    while(true){
    
    /* 
    TCPServer socket;
    TCPSocket* client;*/
    TCPSocket socket;
    //SocketAddress addr("192.168.1.238",65431);
    SocketAddress addr("192.168.137.1",65431);
    nsapi_error_t response;

    int16_t pDataXYZ[3] = {0};
    float pGyroDataXYZ[3] = {0};
    char recv_buffer[9];
    char acc_json[64];
    int sample_num = 0;//counter

    

    // Open a socket on the network interface, and create a TCP connection to addr
    response = socket.open(net);
    if (0 != response){
        printf("Error opening: %d\n", response);
        errled=1;
    }
    response = socket.connect(addr);
    
    if (0 != response){
        printf("Error connecting: %d\n", response);
        errled=1;

    }


    socket.set_blocking(1);
    printf("sending data...");
    intled=0;
    while (1){
        led=1;
        //++sample_num; cancle the counter
        BSP_ACCELERO_AccGetXYZ(pDataXYZ);
        BSP_GYRO_GetXYZ(pGyroDataXYZ);
 

        float x = pDataXYZ[0]*SCALE_MULTIPLIER, y = pDataXYZ[1]*SCALE_MULTIPLIER, z = pDataXYZ[2]*SCALE_MULTIPLIER;
        float gx= pGyroDataXYZ[0]*SCALE_MULTIPLIER, gy = pGyroDataXYZ[1]*SCALE_MULTIPLIER, gz = pGyroDataXYZ[2]*SCALE_MULTIPLIER;
        
        int sx=0,sy=0,sz=0,sgx=0,sgy=0,sgz=0;
        sgx=fixSymbol(gx);
        gx=fixnumber(gx);
        sgy=fixSymbol(gy);
         gy=fixnumber(gy);
        sgz=fixSymbol(gz);
         gz=fixnumber(gz);
        /*sgx=fixSymbol(gx);
        sgy=fixSymbol(gy);
        sgz=fixSymbol(gz);*

        
       
       
        gx=fixnumber(gx);
        gy=fixnumber(gy);
        gz=fixnumber(gz);
        printf("here");
        printf("Print:%d%d%d%d%d%d",sx,sy,sz,sgx,sgy,sgz);
        //break;*/


 int len = sprintf(acc_json,"{\"gx\":%f,\"gy\":%f,\"gz\":%f,\"sx\":%d,\"sy\":%d,\"sz\":%d}",
                                         (float)((int)(gx*10000))/10000,(float)((int)(gy*10000))/10000,(float)((int)(gz*10000))/10000,
                                         sgx,sgy,sgz);//,(int)sy,(int)sz,(int)sgx,(int)sgy,(int)sgz);
       /* int len = sprintf(acc_json,"{\"x\":%f,\"y\":%f,\"z\":%f,\"gx\":%f,\"gy\":%f,\"gz\":%f,\"sx\":%d,\"sy\":%d,\"sz\":%d}",(float)((int)(x*10000))/10000,
                                        (float)((int)(y*10000))/10000, (float)((int)(gx*10000))/10000,(float)((int)(z*10000))/10000,(float)((int)(gy*10000))/10000,(float)((int)(gz*10000))/10000,
                                         sx,sy,sz);//,(int)sy,(int)sz,(int)sgx,(int)sgy,(int)sgz);
* 
       /* int len = sprintf(acc_json,"{%f,%f,%f,%f,%f,%f}",(float)((int)(x*10000))/10000,
                                        (float)((int)(y*10000))/10000, (float)((int)(gx*10000))/10000,(float)((int)(z*10000))/10000,(float)((int)(gy*10000))/10000,(float)((int)(gz*10000))/10000);
*/
        
        response = socket.send(acc_json,len);
        printf("sent %s\n",acc_json);
       
        if (0 >= response){
            printf("Error seding: %d\n", response);
        }
        wait(0.025);
        if(button.read()==1){
            intled=1;
            continue;
        }
        
    
    led=0;
    }

 
    socket.close();
}

}

void test(){
    printf("test");
}



int main()
{
    int a;
   /* while(true){
        a = button.read();
        printf("%d\n",a);
    }*/
    intled=0;
    led=0;
    errled=0;
    float sensor_value = 0;
    int16_t pDataXYZ[3] = {0};
    float pGyroDataXYZ[3] = {0};

    BSP_GYRO_Init();
    BSP_ACCELERO_Init();
    printf("init completed\n");

#ifdef MBED_MAJOR_VERSION
    printf("Mbed OS version %d.%d.%d\n\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
#endif

    wifi = WiFiInterface::get_default_instance();
    if (!wifi) {
        printf("ERROR: No WiFiInterface found.\n");
        errled=1;//connect error
        return -1;
    }
/* 
    int count = scan_demo(wifi);
    if (count == 0) {
        printf("No WIFI APs found - can't continue further.\n");
        return -1;
    }*/

    printf("\nConnecting to %s...\n", MBED_CONF_APP_WIFI_SSID);
    int ret = wifi->connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
    if (ret != 0) {
        printf("\nConnection error: %d\n", ret);
        errled=1;//connect error
        return -1;
    }



    printf("Success\n\n");
    printf("MAC: %s\n", wifi->get_mac_address());
    printf("IP: %s\n", wifi->get_ip_address());
    printf("Netmask: %s\n", wifi->get_netmask());
    printf("Gateway: %s\n", wifi->get_gateway());
    printf("RSSI: %d\n\n", wifi->get_rssi());


    Thread eventThread;
    
    eventThread.start(callback(&queue, &EventQueue::dispatch_forever));
    //acc_server(wifi);
    button.fall(queue.event(&acc_server,wifi));
    //button.fall(queue.event(&test));



    //button.fall(&acc_server,wifi);
    //button.fall(&acc_server,wifi);
    //acc_server(wifi);
    wait(osWaitForever);
    //wifi->disconnect();
}
