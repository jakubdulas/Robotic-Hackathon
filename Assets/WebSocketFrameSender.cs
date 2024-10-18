using System.Collections;
using UnityEngine;
using System.IO;
using NativeWebSocket;

public class WebSocketFrameSender : MonoBehaviour
{
    public Camera playerCamera;
    private WebSocket websocket;

    async void Start()
    {
        websocket = new WebSocket("ws://192.168.0.171:8765");

        websocket.OnOpen += () => Debug.Log("Connection open!");
        websocket.OnError += (e) => Debug.Log("Error: " + e);
        websocket.OnClose += (e) => Debug.Log("Connection closed!");

        // Open connection
        await websocket.Connect();
        
        // Start sending frames
        StartCoroutine(SendFrameCoroutine());
    }

    private IEnumerator SendFrameCoroutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(0.1f);  // Adjust as necessary

            // Capture frame
            RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
            playerCamera.targetTexture = renderTexture;
            Texture2D screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
            playerCamera.Render();
            RenderTexture.active = renderTexture;
            screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
            playerCamera.targetTexture = null;
            RenderTexture.active = null;

            // Convert to byte array
            byte[] imageBytes = screenShot.EncodeToPNG();

            // Send the image over WebSocket
            if (websocket.State == WebSocketState.Open)
            {
                await websocket.Send(imageBytes);
            }

            Destroy(screenShot);
            Destroy(renderTexture);
        }
    }

    async void OnApplicationQuit()
    {
        await websocket.Close();
    }
}
