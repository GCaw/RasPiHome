import requests
import datetime
from time import sleep
import threading
from picamera import PiCamera
import logging
from ftplib import FTP_TLS

import i2ctemp
import config

#default period in seconds for how often to update each item
P_GET_INSIDE_TEMPERATURE = 50
P_TRANSMIT_TEMPS = 60
P_FETCH_REQUESTS = 30
P_FETCH_OUTSIDE_TEMP = 10*60

class HomeBase:
    def __init__(self, start=False):
        if (start):
            self.StartAll()
    
    def StartAll(self, inside_temp_period=P_GET_INSIDE_TEMPERATURE, outside_temp_period=P_FETCH_OUTSIDE_TEMP, transmit_period=P_TRANSMIT_TEMPS, requests_period=P_FETCH_REQUESTS):
        self.StartFetchOutsideTempThread(outside_temp_period)
        self.StartGetInsideTempThread(inside_temp_period)
        self.StartFetchRequestsThread(requests_period)
        sleep(20)
        self.StartTransmitTempsThread(transmit_period)
    
    def StopAll(self):
        self.StopGetInsideTempThread()
        self.StopFetchOutsideTempThread()
        self.StopFetchRequestsThread()
        self.StopTransmitTempsThread()
    
    def StartGetInsideTempThread(self, period):
        if (period):
            self.temp_sensor = i2ctemp.bmp180()
            self.get_inside_temp = True
            threading.Thread(target=self.GetInsideTempThread, args=(period,)).start()
        else:
            logging.error("inside_temp_period = 0, thread not started")
        
    def StopGetInsideTempThread(self):
        self.get_inside_temp = False
        
    def GetInsideTempThread(self, period):
        logging.info("Reading inside temperature every " + str(period) + " seconds")
        while(self.get_inside_temp):
            data = self.GetTempAndPress()
            self.inside_temp = data[0]
            self.inside_press = data[1]
            logging.info("Inside Temperature measured as : " + str(self.inside_temp))
            sleep (period)

        logging.info("No longer reading Inside Temp")
        return
        
    def StartTransmitTempsThread(self, period):
        if (period):
            self.transmit_temps = True
            threading.Thread(target=self.TransmitTempsThread, args=(period,)).start()
        else:
            logging.error("transmit_period = 0, thread not started")
    
    def StopTransmitTempsThread(self):
        self.transmit_temps = False
    
    def TransmitTempsThread(self, period):
        logging.info("Transmitting temperatures every " + str(period) + " seconds")
        while(self.transmit_temps):
            self.SendTempAndPress(self.inside_temp,self.inside_press,self.internet_temp)
            sleep(period)

        logging.info("No longer transmitting temp")
        return
        
    def StartFetchRequestsThread(self, period):
        if (period):
            self.fetch_requests = True
            threading.Thread(target=self.FetchRequestsThread, args=(period,)).start()
        else:
            logging.error("requests_period = 0, thread not started")
    
    def StopFetchRequestsThread(self):
        self.fetch_requests = False
        
    def FetchRequestsThread(self, period):
        logging.info("Fetching requests every " + str(period) + " seconds")
        while(self.fetch_requests):
            #
            sleep (period)

        logging.info("No longer reading Fetching requests")
        return
        
    def StartFetchOutsideTempThread(self, period):
        if (period):
            self.last_internet_temp_time = 0;
            self.internet_temp = 100.0;
            self.fetch_outside_temp = True
            threading.Thread(target=self.FetchOutsideTempThread, args=(period,)).start()
        else:
            logging.error("outside_temp_period = 0, thread not started")
        
    def StopFetchOutsideTempThread(self):
        self.fetch_outside_temp = False
        
    def FetchOutsideTempThread(self, period):
        logging.info("Fetching outside temperature every " + str(period) + " seconds")
        while(self.fetch_outside_temp):
            self.GetInternetWeather()
            sleep (period)

        logging.info("No longer reading fetching outside temp")
        return
        
    # Fetch a temperature from Open Weather API
    def GetInternetWeather(self):
        call = user_logins.WEATHER_API_ADDRESS + "/data/2.5/weather?zip="+ WEATHER_API_ZIPCODE + ",us&APPID=" + user_logins.WEATHER_API_KEY
        result = self.IssueRequest(call)
        
        if result is Null:
            temp = 100.0
            logging.error("Problem accessing outdoor weather")
        else:
            time_updated = result.json()['dt']
            if time_updated >  self.last_internet_temp_time:
                temp = self.ConvertKelvinToCelcius(result.json()['main']['temp'])
                self.last_internet_temp_time = time_updated
                logging.info("New outdoor temperature fetched: " + str(temp))
            else:
                logging.info("New outdoor temperature not available")
                temp = self.internet_temp
        
        self.internet_temp = temp
        
    def ConvertKelvinToCelcius():
        return temp - 273.15;
        
    def GetTempAndPress(self):
        return self.temp_sensor.GetTAndP()

    def IssueRequest(self, call):
        retry = 3
        while(retry):
            retry -=1
            try: 
                r = requests.get(call, timeout=10)
                
                if (r.status_code == 200):
                    retry = 0
                else:
                    logging.error("Request failed - status: " + r.status_code + " - " + r.text + " - " + call)
                    r = Null

            except (requests.ConnectionError, requests.ReadTimeout) as err:
                logging.error("Request failed: " + str(err)  + " - " + call)
                r = Null

        return r

    def SendTempAndPress(self, temp_in, press_in, temp_out):
        call = user_logins.SERVER_ADDRESS + "new_temp.php?temp="+ str(temp_in) + "&air=" + str(press_in) + "&temp_out=" + str(temp_out)
        result = self.IssueRequest(call)
        
        if result is Null:
            logging.error("Failed to send data to server")
        else:
            logging.info("Data sent to database server")
                
    def TakePhoto(self):
        camera = PiCamera()
        camera.resolution = (3280, 2464)
        camera.framerate = 15
        camera.start_preview(alpha = 150, resolution=(640, 480))
        sleep(2)
        
        timenow = datetime.datetime.utcnow().strftime("%y%m%d%H%M%S")
        camera.capture('/home/pi/Desktop/home/media/img' + timenow + '.jpg')

        camera.stop_preview
        camera.close()
    
    def TakeVideo(self, length):
        camera = PiCamera()
        camera.resolution = (1920, 1080)
        camera.framerate = 24
        camera.start_preview(alpha = 150, resolution=(640, 360))
        sleep(2)
        
        timenow = datetime.datetime.utcnow().strftime("%y%m%d%H%M%S")
        camera.start_recording('/home/pi/Desktop/home/media/mov' + timenow + '.h264')
        sleep(length)
        camera.stop_recording()
        
        camera.stop_preview
        camera.close()
        
    def UploadFileToServer(self, file_name, file_location, dest_location):
        try:
            ftp = FTP_TLS(FTP_SERVER_ADDRESS,port=FTP_SERVER_PORT,timeout=10)
            ftp.login(FTP_SERVER_USER, FTP_SERVER_PWD)
            ftps.prot_p() 
            ftp.cwd(dest_location)
            file = open(file_location,'rb')
            ftp.storbinary('STOR ' + file_name, file)
            file.close()
            ftp.quit()
        except ftplib.all_errors as err:
            logging.error("FTP upload failed - " + err)
    
    def ProcessMenu(self, option):
        if option == 0:
            print ("Help!")
        elif option == 1:
            self.StartGetInsideTempThread(P_GET_INSIDE_TEMPERATURE)
        elif option == 2:
            self.StartFetchOutsideTempThread(P_FETCH_OUTSIDE_TEMP)
        elif option == 3:
            self.StartTransmitTempsThread(P_TRANSMIT_TEMPS)
        elif option == 4:
            self.StartFetchRequestsThread(P_FETCH_REQUESTS)
        elif option == 5:
            self.StartAll()
        elif option == 11:
            self.StopGetInsideTempThread()
        elif option == 12:
            self.StopFetchRequestsThread()
        elif option == 13:
            self.StopTransmitTempsThread()
        elif option == 14:
            self.StopFetchRequestsThread()
        elif option == 15:
            self.StopAll()
        elif option == 50:
            self.GetInternetWeather()
        elif option == 51:
            self.TakePhoto()
        elif option == 52:
            self.TakeVideo(5)
        elif option == 99:
            return False
        else:
            print("Invalid Option")

        return True
            
def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(ascitime)s %(message)s')
    
    home = HomeBase(start=True)
   
    loop = True
    while (loop):
        loop = home.ProcessMenu(int(input("MENU: ")))
        
    home.StopAll()
    logging.info("Program Ended - threads may continue to run till next call")
            
if __name__=="__main__":
    main()