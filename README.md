1) TSID folder
 : This is some modified version of TSID for using Qpoases
 
2) KIMM_qpoases folder
 : This is just wrapper of qpoases (if you already use other qpoases, you dont need to build and install it)
 
 3) tsid_api
 : This is our previous tsid_ggory (I changed the name from tsid_ggory to tsid_api)
 
 
 # Install Precedure
 1) Kimm_qpoases
 ```
 cd kimm_qpoases && mkdir build && cd build
 cmake ..
 ccmake .. (plz change install directory usr/local to opt/openrobots)
 make -j16
 sudo make install 
 ```
 2) TSID
 If you already installed tsid binary file 
 ```
 sudo apt purge robotpkg-tsid robotpkg-py36-tsid
 ```
 after that
 ```
 cd tsid && mkdir build && cd build
 cmake ..
 ccmake .. (plz change install directory usr/local to opt/openrobots)
 make -j16
 sudo make install 
 ```
 3) tsid_api
 ```
 cd tsid_api && mkdir build && cd build
 cmake ..
 ccmake .. (plz change install directory usr/local to opt/openrobots)
 make -j16
 sudo make install 
 ```
