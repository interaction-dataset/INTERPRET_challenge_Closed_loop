# The "Closed-loop" track for the INTERPRET challenge for trajectory prediction in traffic #

This repo provides instructions for preparing your docker submission to participate the "Closed-loop" track the INTERPRET challenge for trajectory prediction of vehicles in traffic. The challenge is organized by the team of the [INTERACTION dataset](http://interaction-dataset.com). The INTERPRET challenge is the first "Closed-loop" challenge for evaluating the performance of predictors by considering their impacts in a "Prediction->Planning" pipeline that is commonly adopted in autonomous driving.

For more details about the [INTERACTION dataset](http://interaction-dataset.com) and the [INTERPRET challenge (a NeurIPS2020 competition)](http://challenge.interaction-dataset.com/prediction-challenge/intro), please refer the websites.

## Description
We provide a simulator built based on realistic scenarios selected from the INTERACTION dataset. In the simulator, one robot car is selected whose actions are driven by a default motion planner based on the submitted predictors. Other agents in the simulator are responsive agents driven by internal algorithms.

Hence, all participants need to prepare their predictors as docker files and submit to the server so that the closed-loop evaluation can be performed.

## Preparing your predictors to communicate with the simulator
The predictors communite with the simulator via grpc. We provide the following two APIs. Please read them while you are preparing your docker image.
1. Obtaining real-time information from the simulator: the predictors (clients) will use `on_env` to store the historical trajectory (10 frames) sent by the simulator (server);
2. Sending real-time predictions to the simulator: the predictor (clients) will use `fetch_my_state` to get the predicted results (30 frames in the future) from the predictors (clients).

In the `./predictor/*`,

- `predictor.py` is an abstract class, you need to implement all the abstract methods in your own predictor.
- `echo_predictor.py` is a simple echo predictor, namely returns back the last frame in the historical trajectory.
- `lstm_predictor.py` is a pytorch-based examplar predictor which is trained on the `interaction` dataset and has 0.3 MoN performance on the MA scenario. `lstm.pt` stores the model parameters. You can refer it to prepare your docker image.

## Prerequisites ##

 - python 3.7

 - docker

 - grpc && protobuf

    - please follow the instruction in the `simulator/readme.md`

    - ```bash
      pip install grpcio
      pip install protobuf
      ```

 - pytorch or tensorflow to support your predictor.

## Build and Run ##
**Prepare**

use `protoc` to generate python version protocols for communication.
each time the `simulator.proto` updated, you need generate them again.
```bash
protoc -I ../proto/ --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` ../proto/simulator.proto
protoc -I ../proto/ --python_out=. ../proto/simulator.proto
```

If this fails, you can try
```bash
python -m grpc_tools.protoc --proto_path=../proto/ --python_out=. --grpc_python_out=. ../proto/simulator.proto
```
You may get a warning when using `grpc_tools.protoc`, but it should still execute succesfully and generate the `simulator_pb2.py` and `simulator_pb2_grpc` files (provided that you have `grpc_tools` installed).

**Run locally**

```bash
# simulator should be launched before predictor, where
# -s sepcify the simulator service address
# -p specify the simulator service port
python3 main.py -s 127.0.0.1 -p 50051
```

**Docker**

- You need to put the dependencies (pytorch, numpy, ....) in the `requirement.text`, then

```bash
cd deploy
./make_image.sh my_predictor
```

## Metric
Please read the [Metrics_for_the_Closed_Loop_Track_of_the_INTERPRET_Challenge.pdf](./Metrics_for_the_Closed_Loop_Track_of_the_INTERPRET_Challenge.pdf) in the directory.



**Contact**
If you have any questions, please submit an issue in this repo. 
