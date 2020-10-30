# EdgeAV-Bot

The purpose of this project is to bring some of the expertise we learnt in the research doing pruning/quantization/compression to real-world examples, solving some of the most exciting machine learning optimization problems.

To evaluate the benefits, we are targeting a small scale AV here, which is scalable, inexpensive (<$300), and fun to play with! 🚗
For that, we need to:

- **Build a platform: - Robot:**
First, we need to build a robot car that takes commands from the edge device. We chose a regular RC car for this so that everyone can easily buy and transform their car of choice and provide the electrical details to do so. For the edge-AI device, we decided to go with the Jetson nano board based on its features, and also it is inexpensive. This board enables the execution of AI applications on the edge, but (happily for us) it has only a 128-core Maxwell GPU on it which gives us the opportunity to tackle the challenge of not having much compute power.
- **Profile to find the bottleneck:**
We will be running different machine learning applications and profile the performance (latency, throughput, memory) and the energy consumption targetting different goals.


- **Optimize the bottleneck:**
Finally, we will see what modules need to be optimized (and potentially accelerated) to make the models run smoothly on our device with the constrained resources.
These optimizations will be done with the goal of reducing latency, improving throughput, reducing memory footprint, and hopefully reducing the energy consumption of the system. As we don't know yet what parts need to be optimized, we can talk based on the previous experiences and hope that these optimizations can be done without sacrificing the test accuracy.

Some things to note:
- **Optimizing the Inference:** Our goal is to perform an inference task more efficiently. Training can technically happen on the Edge device as well, but due to its limited resource, we will rely on powerful servers to perform this task;
- **Optimizing the pre-trained models** Model optimizations such as pruning and quantization, usually needs a retraining/fine-tuning phase to recover the accuracy drop right after the optimization is done on a pre-trained model. There exist methods that can train a sparse/quantized model from scratch but we won't target that in this case.
- **Simplyifing vs computing:** Whenever possible, we will try to simplify or replace the computation and if not, optimize it. For example, if we can measure the depth with a simple sensor, our preference is to remove/reduce the load from the compute unit (to infer dept from the camera image) and just use sensor data. Similarly, if a task can be accomplished by a non-DNN solution with an acceptable accuracy loss, we might target that (e.g. e classic ELAS algorithm [1].) " In cases where sensing could replace computing, accelerating the computing algorithm has little value." [1]
