using System;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using NativeWebSocket;


public class NewBehaviourScript : MonoBehaviour
{
    public GameObject panel;
    Texture2D texture;
    bool isTextureUpdated = false;
    WebSocket ws;


    // Start is called before the first frame update
    async void Start()
    {
        texture = new Texture2D(2, 2);

        ws = new WebSocket("ws://192.168.0.171:8000/ws");

        ws.OnMessage += (bytes) =>
        {
            texture.LoadImage(bytes);
            isTextureUpdated = true;
        };

        ws.OnOpen += () => Debug.Log("Connection opened!");
        ws.OnError += (e) => Debug.Log($"Error: {e}");
        ws.OnClose += (e) => Debug.Log("Connection closed!");

        await ws.Connect();
    }


    // Update is called once per frame
    void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        ws?.DispatchMessageQueue();
#endif

        if (isTextureUpdated)
        {
            panel.GetComponent<Renderer>().material.mainTexture = texture;
            isTextureUpdated = false;
        }

    }

    async void OnApplicationQuit()
    {
        if (ws != null)
        {
            await ws.Close();
        }
    }
}
