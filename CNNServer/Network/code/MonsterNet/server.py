import requests
import gevent
import random
import string
import main
import os
import time
import re
from PIL import Image

from flask import Flask, request
app = Flask(__name__)

return_val = 'no'

@app.route('/submit', methods=['POST'])
def doEverything():
  print(request.files)
  for key, file  in request.files.items():
    file.save('./../../../Data/CharacterDraw/sketch/' + file.filename)
  main.main()  
  global return_val
  gevent.joinall([gevent.spawn(spawned)])
  return return_val
  
def spawned():
  global return_val
  print('yoting')
  payload = {'client_id': os.environ['FORGE_CLIENT_ID'], \
            'client_secret': os.environ['FORGE_CLIENT_SECRET'], \
            'grant_type': 'client_credentials', \
            'scope': 'data:write data:read'}
  resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', \
                headers={'Content-Type': 'application/x-www-form-urlencoded'}, \
                data=payload)
  access_token = resp.json()['access_token']
  
  print("token: " + access_token)

  jsonHeaders = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}

  name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
  payload2 = {'scenename': name, 'format': 'rcm'}
  resp2 = requests.post('https://developer.api.autodesk.com/photo-to-3d/v1/photoscene', \
                headers=jsonHeaders, \
                data=payload2)
  # print("error, if there was one otherwise None: " + resp2.json()['Error'])
  
  print(resp2.json())
  print(resp2.json()['Photoscene']['photosceneid'])
  sceneId = resp2.json()['Photoscene']['photosceneid']
  return_val = sceneId


  headers = {\
      'Content-Type': 'application/json',\
      'Authorization': 'Bearer ' + access_token,\
  }

  files = {\
      'photosceneid': (None, 'hcYJcrnHUsNSPII9glhVe8lRF6lFXs4NHzGqJ3zdWMU\n'),\
      'type': (None, 'image\n')\
      # 'file[0]': ('./../../../Data/CharacterDraw/sketch/sketch-F-0.png', open('./../../../Data/CharacterDraw/sketch/sketch-F-0.png', 'rb')),\
      # 'file[1]': ('./../../../Data/CharacterDraw/sketch/sketch-S-0.png', open('./../../../Data/CharacterDraw/sketch/sketch-S-0.png', 'rb')),\
  }

  i = 0
  for file in os.listdir('./../../../Data/CharacterDraw/output/results/m1/'):
    print(file)
    filePath = './../../../Data/CharacterDraw/output/results/m1/' + file
    im = Image.open(filePath)
    rgb_im = im.convert('RGB')
    filePath = re.sub('(\w+).png', '\\1.jpeg', filePath)
    rgb_im.save(filePath)
    # files['file[' + str(i) + ']'] = (filePath, open(filePath, 'rb'))
    files['file[' + str(i) + ']'] = filePath
    i+=1
  print(files)

  response = requests.post('https://developer.api.autodesk.com/photo-to-3d/v1/file',\
                          headers={'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + access_token}, data=files)
  print(response)

  startResponse = requests.post('https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/' + sceneId, headers=headers)
  print(startResponse.json())

  progressResponse = None
  while progressResponse is None or progressResponse.json()['Photoscene']['progressmsg'] != 'DONE':
    progressResponse = requests.get('https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/' + sceneId + '/progress', \
                headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token})
    # print(progressResponse)
    # print(progressResponse.json())
    print(progressResponse.json()['Photoscene']['progress'])
    time.sleep(7)
  
  fileResponse = requests.get('https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/' + sceneId + '?format=fbx', \
                headers=jsonHeaders)

  print(fileResponse.json()['Photoscene']['scenelink'])

  
if __name__ == '__main__':
    app.run()