# RasPiHome
Project to use a Rasberry Pi as a home internet connected hub.

Curently the project consists of the following:
* Python code to run on a Raspberry Pi that does the following:
1. Reads temperature from connected i2c sensor
2. Fetches temperature data from Open Weather API
3. Takes photo and or video with connected RaspPi Camera
4. Monitors server for user requests
5. Updates server with temperature and media data as captured.

* php code to run on a server (in this case shared hosting) that:
1. Connects to a MySQL databse
2. Updates database in response to data from the Raspberry Pi
3. Updates databse in response to user requests
4. Allows access to database data as required by the Raspberry Pi or user
