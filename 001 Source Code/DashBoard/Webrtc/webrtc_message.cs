using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.WebRTC;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Threading.Tasks;
using System;

public class WebRTC3 : MonoBehaviour
{

    [System.Serializable]
    private class SignalingMessage
    {
        public string id;
        public RTCSdpType type;
        public string sdp;

    }

    [System.Serializable]
    private class TostringMessage
    {
        public string id;
        public string type;
        public string sdp;
    }

    private string ID = "answerer01";
    private string SIGNALING_SERVER_URL = "http://192.168.50.244:8000";

    private string[] STUNSERVER = { "stun:stun.l.google.com:19302" };
    public UnityWebRequest webRequest;
    public UnityWebRequest postRequest;
    public RTCDataChannel channel;
    public RTCDataChannel receiveChannel;

    public RTCSessionDescription a_desc;

    private RTCPeerConnection peerConnection;
    private RTCConfiguration config;

    // Start is called before the first frame update
    void Start()
    {

        WebRTC.Initialize();
        config = new RTCConfiguration();
        RTCIceServer[] iceServers = { new RTCIceServer { urls = STUNSERVER } };
        config.iceServers = iceServers;

        peerConnection = new RTCPeerConnection(ref config);

        RTCDataChannelInit channelConfig = new RTCDataChannelInit();

        channel = peerConnection.CreateDataChannel("video",channelConfig);
        channel.OnOpen += () =>
        {
            Debug.Log("Data channel Open!");
        };
        channel.OnClose += () =>
        {
            Debug.Log("Data channel closed!");
        };

        channel.OnMessage += (data) =>
        {
            Debug.Log("Data channel received message: " + data);
        };
        
        StartCoroutine(GetResquest(SIGNALING_SERVER_URL));

    }

    private void Update() 
    {
       
        peerConnection.OnDataChannel = (channel_1) =>
        {
            Debug.Log("Data channel created by remote party!");

            // Assign the channel object to the dataChannel variable
            channel = channel_1;

            // Set up the data channel event handlers
            channel.OnOpen += () =>
            {
                Debug.Log("Data channel open!");
            };

            channel.OnClose += () =>
            {
                Debug.Log("Data channel closed!");
            };

            channel.OnMessage += (byte[] bytes) =>
            {
                //data 수신
                var message = System.Text.Encoding.UTF8.GetString(bytes);
                Debug.Log(message);
            };
        };

    }
  
    IEnumerator Createanswer()
    {
        var op = peerConnection.CreateAnswer();
        yield return op;
        peer_local_connection_access(op.Desc);
        
    }

    IEnumerator PostResquest(RTCSessionDescription desc)
    {
        var message = new TostringMessage();
        message.id = ID;
        message.type = desc.type.ToString();
        message.sdp = desc.sdp;
        
        string json = JsonUtility.ToJson(message);

        using (UnityWebRequest www = UnityWebRequest.Post(SIGNALING_SERVER_URL + "/answer", json))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log("Form upload complete!");
            }
        }

    }

    IEnumerator GetResquest(string uri)
    {
        webRequest = UnityWebRequest.Get(uri + "/get_offer");
        {
            // Request and wait for the desired page.
            yield return webRequest.SendWebRequest();


            string[] pages = uri.Split('/');
            int page = pages.Length - 1;

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                    Debug.LogError(pages[page] + ": Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.ProtocolError:
                    Debug.LogError(pages[page] + ": HTTP Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.Success:
                    Debug.Log(pages[page] + ":\nReceived: " + webRequest.downloadHandler.text);
                    get_next_level();
                    break;
            }
        }
    }
    
    public void get_next_level()
    {
        var data = JsonUtility.FromJson<SignalingMessage>(webRequest.downloadHandler.text);
        if (data.type == RTCSdpType.Offer)
        {
            RTCSessionDescription desc = new RTCSessionDescription();
            desc.sdp = data.sdp;
            desc.type = data.type;

            peer_connection_remote_acces(desc);

            StartCoroutine(Createanswer());

        }
        else
        {
            Debug.Log("74error");

        }
    }

    async void peer_connection_remote_acces(RTCSessionDescription desc)
    {
        peerConnection.SetRemoteDescription(ref desc);
        await Task.Delay(1000); 

    }

    async void  peer_local_connection_access(RTCSessionDescription desc)
    {
        peerConnection.SetLocalDescription(ref desc);
        await Task.Delay(1000); 
        StartCoroutine(PostResquest(desc));
    }

}
