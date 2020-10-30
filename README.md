# EdgeAV-Bot

The purpose of this project is to bring some of the expertise research on pruning/quantization/compression to real-world examples, solving some of the most exciting machine learning optimization problems.
To evaluate the benefits, we are targeting a small scale AV here which is inexpensive, and fun to play with! 🚗
For that, we need to:

- **Build a platform: - Robot:**
First, we need to build a robot car that takes commands from the edge device. We chose a regular RC car for this so that everyone can easily buy and transform their car of choice and provide the electrical details to do so. For the edge-AI device, we decided to go with the Jetson nano board based on its features, and also it is inexpensive. This board enables the execution of AI applications on the edge, but (happily for us) it has only a 128-core Maxwell GPU on it which gives us the opportunity to tackle the challenge of not having much compute power.

- **Profile to find the bottleneck:**
We will be running different machine learning applications and profile the performance (latency, throughput, memory) and the energy consumption targetting different goals.

- **Optimize the bottleneck:**
Finally, we will see what modules need to be optimized (and potentially accelerated) to make the models run smoothly on our device with the constrained resources.
These optimizations will be done with the goal of reducing latency, improving throughput, reducing memory footprint, and hopefully reducing the energy consumption of the system. As we don't know yet what parts need to be optimized, we can talk based on the previous experiences and hope that these optimizations can be done without sacrificing the test accuracy.

## Design Constraints

**Cost**: The lower the better. The total cost consists of sensors (ultrasound, camera, ...), interfaces (motor driver, voltage level converter), the brain (Jetson Nano), power source (batteries), and the mechanical part (the car body) which is around $300.
We should mention that the cost of an autonomous vehicle is a complex function influenced by not only the cost of the vehicle itself, but also other costs including maintaining the cloud services.


**Latency** The end-to-end time between when a new event happened/sensed and when the robot reacted must be short enough to avoid hitting objects. This is not very critical in our case is the speed of the car is very low but is a big factor in larger vehicles.

**Throughput** This indicates how often we can feed the robot with new commands and control it. [1] says a 10Hz throughput is well above what humans drivers manipulate the vehicle. The classical way of dealing with this is pipelining if possible.

**Energy** Energy translates to the range of the robot. It cannot easily be extended with more battery as more battery means more weights and putting more pressure on motors. We estimated the average power consumption of modules under the load to be 15Wh (or 3A-5V the board + peripheral) and the motors at max speed to be 25Wh. We chose a 20,000mah battery to power the compute logic for 6 hours and keep the original battery to drive the motors which should give us up to 1h under mid load.

**Quality** For the purpose of this project, course-grained information such as depth, or slightly reduced model accuracy can be acceptable. Therefore, when we see huge savings in terms of the energy/latency, we might trade off the accuracy, otherwise, the goal is to maintain the accuracies as much as possible.

**Security & Safety** Again, this is not that of a concern here as the data is collected from public areas and are not sensitive in the nature; this means that we can send it to the cloud to process. 
Similarly, the car is running at low speeds and don't carry/can not harm anything, so having a sophisticated is not justifiable.
Having said there, we design a mechanism to override the robot movements when sensors detect something that is in contrast with perception modules. So, as long as the latency of the system is acceptable and the models produce the correct results, we meet our goal here.
 

## Considerations

Some things to note:
- **Optimizing the Inference:** Our goal is to perform an inference task more efficiently. Training can technically happen on the Edge device as well, but due to its limited resource, we will rely on powerful servers to perform this task;
- **Optimizing the pre-trained models** Model optimizations such as pruning and quantization, usually needs a retraining/fine-tuning phase to recover the accuracy drop right after the optimization is done on a pre-trained model. There exist methods that can train a sparse/quantized model from scratch but we won't target that in this case.
- **Simplyifing vs computing:** Whenever possible, we will try to simplify or replace the computation and if not, optimize it. For example, if we can measure the depth with a simple sensor, our preference is to remove/reduce the load from the compute unit (to infer dept from the camera image) and just use sensor data. Similarly, if a task can be accomplished by a non-DNN solution with an acceptable accuracy loss, we might target that (e.g. e classic ELAS algorithm [1].) " In cases where sensing could replace computing, accelerating the computing algorithm has little value." [1]
- **HW acceleration** FPGA acceleration with its unique capabilites such as partial reconfiguration, is a suitable (and cool) candidate for offloading ML workloads and if we identify a good use case and have time to do so, we will go that way, but we will majorly rely on accelerating things on the GPU using CUDA when possible.

[1] [Building the Computing System for Autonomous Micromobility Vehicles: Design Constraints and Architectural Optimizations](https://www.microarch.org/micro53/papers/738300b067.pdf)
