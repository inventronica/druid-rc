import cv2
import numpy as np
import depthai

def eagle_eye(camera):
    manip = camera.getImgManipConfig()
    manip.warp.meshPositionFirst = True
    manip.warp.positionFirstMeshSize = 0
    manip.warp.positionFirstMeshSizeHeight = camera.getResolutionHeight()
    manip.warp.positionFirstMeshSizeWidth = camera.getResolutionWidth()
    manip.warp.positionFirstMesh = []
    mesh_cols = camera.getResolutionWidth() // 10
    mesh_rows = camera.getResolutionHeight() // 10
    for i in range(mesh_rows):
        for j in range(mesh_cols):
            manip.warp.positionFirstMesh.extend([j * 10, i * 10])
    
    manip.warp.meshWidth = mesh_cols
    manip.warp.meshHeight = mesh_rows
    manip.warp.interpolation = 1
    manip.warp.borderPreset = 0

    manip.warp.enable = True
    manip.warp.passthrough = False

    camera.setImgManipConfig(manip)

    while True:
        # Get the camera frame
        camera_data = camera.getRgbFrame()
        frame = camera_data.getCvFrame()

        # Display the original frame
        cv2.imshow("Original", frame)

        # Apply the eagle eye effect
        camera.sendImageManipConfig()
        camera.sendPipelineConfig()
        camera.startPipeline()

        # Get the processed frame
        output_data = camera.getOutputQueue("previewout").get()
        output_frame = output_data.getCvFrame()

        # Display the processed frame
        cv2.imshow("Eagle Eye", output_frame)

        # Check for ESC key press to exit
        if cv2.waitKey(1) == 27:
            break

    # Cleanup
    cv2.destroyAllWindows()
    camera.stopPipeline()

# Create a DepthAI pipeline
pipeline = depthai.Pipeline()

# Create a node for the RGB camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)  # Set the preview size as desired

# Create an output stream for the preview
preview_out = pipeline.createXLinkOut()
preview_out.setStreamName("previewout")
cam_rgb.preview.link(preview_out.input)

# Connect the RGB camera to the preview output
cam_rgb.preview.link(preview_out.input)

# Start the pipeline
device = depthai.Device(pipeline)
camera = device.getOutputQueue("previewout", 1, True)

# Apply the eagle eye effect on the camera output
eagle_eye(camera)

# Release the resources
device.close()
