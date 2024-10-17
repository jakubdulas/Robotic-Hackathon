using System.Net.Sockets;
using UnityEngine;

public class RobotController : MonoBehaviour
{
    public static RobotController Instance; // Singleton instance

    private TcpClient client;
    private NetworkStream stream;
    private string espIp = "192.168.0.116"; // Replace with your ESP8266's IP
    private int port = 80;

    private void Awake()
    {
        // Implement Singleton pattern
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject); // Keep the connection alive between scenes
            ConnectToRobot();
        }
        else
        {
            Destroy(gameObject); // Destroy duplicate RobotController instances
        }
    }

    private void ConnectToRobot()
    {
        try
        {
            client = new TcpClient(espIp, port);
            stream = client.GetStream();
            Debug.Log("Connected to Arduino.");
        }
        catch (SocketException e)
        {
            Debug.LogError("Connection error: " + e.Message);
        }
    }

    public void SendCommand(string command)
    {
        if (client != null && stream != null && client.Connected)
        {
            byte[] data = System.Text.Encoding.ASCII.GetBytes(command);
            stream.Write(data, 0, data.Length);
            Debug.Log("Sent command: " + command);
        }
        else
        {
            Debug.LogError("Failed to send command. No connection established.");
        }
    }

    private void OnApplicationQuit()
    {
        // Close the connection when the application quits
        if (client != null)
        {
            stream.Close();
            client.Close();
        }
    }
}
