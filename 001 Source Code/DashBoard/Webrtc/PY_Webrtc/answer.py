import requests
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
import asyncio
import base64
import cv2
import numpy as np
import socket
import json
from config import *


ID="answerer01"

stun_server = RTCIceServer(urls=['stun:stun.l.google.com:19302'])
CONFIG = RTCConfiguration(iceServers=[stun_server])

async def main():
    
    print("Starting")
    peer_connection = RTCPeerConnection(configuration=CONFIG)

    channel = peer_connection.createDataChannel("chat")
    
    @peer_connection.on("datachannel")
    def on_datachannel(channel):
        print(channel, "-", "created by remote party")
    
        @channel.on("message")
        async def on_message(message):
            print(message)
            # You can add your image decoding and display code here
        
    resp = requests.get(SIGNALING_SERVER_URL + "/get_offer")
    while True:
        if resp.status_code == 200:
            data = resp.json()
            if data["type"] == "offer":
                rd = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await peer_connection.setRemoteDescription(rd)
                print("remote L ",peer_connection.remoteDescription)
                await peer_connection.setLocalDescription(await peer_connection.createAnswer())
                print("local l ",peer_connection.localDescription)
                
                message = {"id": ID, "sdp" : peer_connection.localDescription.sdp, "type" : peer_connection.localDescription.type}
                r = requests.post(SIGNALING_SERVER_URL + '/answer', data=message)
    
                while True:
                    await asyncio.sleep(1)

asyncio.run(main())