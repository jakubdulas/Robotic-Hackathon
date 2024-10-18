using System.Collections;
using UnityEngine;
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

        // Open the WebSocket connection
        await websocket.Connect();

        // Start capturing frames
        StartCoroutine(CaptureFramesCoroutine());
    }

    private IEnumerator CaptureFramesCoroutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(0.1f); // Adjust the frame capture interval

            // Capture the frame
            RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
            playerCamera.targetTexture = renderTexture;
            Texture2D screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
            playerCamera.Render();
            RenderTexture.active = renderTexture;
            screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
            playerCamera.targetTexture = null;
            RenderTexture.active = null;

            // Encode to PNG
            byte[] imageBytes = screenShot.EncodeToPNG();

            // Send the frame (call async method without awaiting)
            _ = SendFrameAsync(imageBytes); // Fire and forget

            Destroy(screenShot);
            Destroy(renderTexture);
        }
    }

    // Async method to send the frame over WebSocket
    private async System.Threading.Tasks.Task SendFrameAsync(byte[] imageBytes)
    {
        if (websocket.State == WebSocketState.Open)
        {
            try
            {
                await websocket.Send(imageBytes);
            }
            catch (System.Exception e)
            {
                Debug.LogError("Error sending frame: " + e.Message);
            }
        }
    }

    async void OnApplicationQuit()
    {
        await websocket.Close();
    }
}
