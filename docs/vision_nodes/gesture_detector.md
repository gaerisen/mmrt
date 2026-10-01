# Gesture Detector

A server that accepts a filepath to an image and responds with a string
containing its best guess at the hand gesture depicted in the image.

Requires a model to be available at `/home/mmrt/assets/models/dima806'. This is
subject to change, but if you'd like to run it as-is and don't have the model,
you can find it at: [hf.co/dima806/hand_gestures_images_detection]. The dima806
folder must contain `model.safetensors`, `config.json`, and
`preprocesser_config.json`.
