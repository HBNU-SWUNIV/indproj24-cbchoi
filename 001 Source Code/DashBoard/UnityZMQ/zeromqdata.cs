using NetMQ;
using UnityEngine;
using System;
using System.Text;
using NetMQ.Sockets;
using System.Collections;

public class zeromqdata : MonoBehaviour
{
    void Start()
    {
        using (var client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");
            client.SendFrame("Hello");

            string message = null;
            bool gotMessage = false;

            while (!gotMessage)
            {
                if (client.TryReceiveFrameString(out message))
                {
                    gotMessage = true;
                    Debug.Log("Received: " + message);
                }
            }
        }
    }
}