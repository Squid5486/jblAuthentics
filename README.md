A python client to control JBL Authentics speakers. Tested on a JBL Authentics L16, but this probably works on the L8 model as well. 

JBL previously had an app called "JBL Music" on the App Store and Google play store that made it possible to control these speakers from your phone, but i guess JBL dropped support for this app so you cant download it anymore. 

This python program mimics the JBL Music app. The JBL Music app sends some kind of modified http packages, so it was easier to send raw tcp packets using socket instead of using the requests python library. 