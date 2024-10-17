# Robotic-Hackathon

## Controlling Robot

### Steps to Implement:

1. Attach the **`RobotController`** script to a single GameObject in your scene (e.g., an empty GameObject named "RobotManager").
2. Attach the **`PlaneController`** script to each plane and set the `command` field appropriately in the Inspector.
3. Make sure the `RobotController` persists across scenes using `DontDestroyOnLoad()`.
