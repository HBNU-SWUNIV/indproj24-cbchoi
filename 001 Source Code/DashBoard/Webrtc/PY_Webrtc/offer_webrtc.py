from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer, VideoStreamTrack, RTCRtpSender
import json
import asyncio
import requests
import cv2
import numpy as np
import base64
from config import *
import os

ID = "offerer01"

async def main():
    
    print("Starting")
    peer_connection = RTCPeerConnection()

    channel = peer_connection.createDataChannel("chat")
    
    async def send_data():
        while True:
            channel.send("rdddddddddddddddd")
            print("send finish")
            await asyncio.sleep(1)

    @channel.on("open")
    def on_open():
        print("channel opened")
        asyncio.ensure_future(send_data())
        

    await peer_connection.setLocalDescription(await peer_connection.createOffer())
    message = {"id": ID, "sdp" : peer_connection.localDescription.sdp, "type" : peer_connection.localDescription.type}
    r = requests.post(SIGNALING_SERVER_URL + '/offer', data = message)

    #데이터 전송
    while True:
        resp = requests.get(SIGNALING_SERVER_URL + "/get_answer")
        if resp.status_code == 503:
            print("Answer not Ready , trying again")
            await asyncio.sleep(1)
        elif resp.status_code == 200:
            data = resp.json()
            print(data)
            if data["type"] == "Answer":
                data["type"] = "answer"
                rd = RTCSessionDescription(sdp = data["sdp"], type=data["type"])
                await peer_connection.setRemoteDescription(rd)
                print(peer_connection.remoteDescription)
                while True:
                    await asyncio.sleep(1)
            else:
                print("Wrong type")
            break
    
asyncio.run(main())
