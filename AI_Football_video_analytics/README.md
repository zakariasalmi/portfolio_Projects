# Soccer Video Analytics



![Image1](https://github.com/user-attachments/assets/f1dee448-a650-4269-ab7e-98e74ff308ad)
![Image2](https://github.com/user-attachments/assets/362cfb9f-dfc2-47dd-a82b-ab1b95996367)




## How to run


To run one of the applications (possession computation and passes counter) you need to use flags in the console.

These flags are defined in the following table:

| Argument | Description | Default value |
| ----------- | ----------- | ----------- |
| application | Set it to `possession` to run the possession counter or `passes` if you like to run the passes counter | None, but mandatory |
| path-to-the-model | Path to the soccer ball model weights (`pt` format) | `/models/ball.pt` |
| path-to-the-video | Path to the input video | `/videos/soccer_possession.mp4` |


