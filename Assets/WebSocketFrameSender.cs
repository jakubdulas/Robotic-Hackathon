using System.Collections;
using System.Threading.Tasks;
using UnityEngine;
using NativeWebSocket;

public class WebSocketFrameSender : MonoBehaviour
{
    public Camera playerCamera;
    private WebSocket websocket;

    // Cached RenderTexture and Texture2D
    private RenderTexture renderTexture;
    private Texture2D screenShot;

    // Frame capture interval (in seconds)
    public float frameCaptureInterval = 0.1f;

    async void Start()
    {
        websocket = new WebSocket("ws://192.168.0.171:8765");

        websocket.OnOpen += () => Debug.Log("Connection open!");
        websocket.OnError += (e) => Debug.Log("Error: " + e);
        websocket.OnClose += (e) => Debug.Log("Connection closed!");

        // Open the WebSocket connection
        await websocket.Connect();

        // Initialize RenderTexture and Texture2D once
        renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);

        // Start capturing frames
        StartCoroutine(CaptureFramesCoroutine());
    }

    private IEnumerator CaptureFramesCoroutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(frameCaptureInterval); // Adjust the frame capture interval

            // Capture the frame
            playerCamera.targetTexture = renderTexture;
            playerCamera.Render();
            RenderTexture.active = renderTexture;
            screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
            playerCamera.targetTexture = null;
            RenderTexture.active = null;

            // Encode to PNG
            byte[] imageBytes = screenShot.EncodeToPNG();

            // Send the frame using the async method
            _ = SendFrameAsync(imageBytes); // Fire and forget
        }
    }

    // Async method to send the frame over WebSocket
    private async Task SendFrameAsync(byte[] imageBytes)
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
        // Clean up resources
        if (renderTexture != null) RenderTexture.ReleaseTemporary(renderTexture);
        if (screenShot != null) Destroy(screenShot);
    }
}
