using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class PlaneController : MonoBehaviour
{
    public string command; // Command to send

    private void Start()
    {
        // Optionally, you can add an XR Grab Interactable if you want to use the grab feature
        var interactable = gameObject.AddComponent<XRGrabInteractable>();
        interactable.onSelectEntered.AddListener(OnPlaneSelected);
    }

    private void OnPlaneSelected(XRBaseInteractor interactor)
    {
        RobotController.Instance.SendCommand(command);
        Debug.Log("Mouse clicked on " + gameObject.name + " - Sending command: " + command);
    }

    private void OnMouseDown()
    {
        RobotController.Instance.SendCommand(command);
        Debug.Log("Mouse clicked on " + gameObject.name + " - Sending command: " + command);
    }
}
