#Docker
<!-- GFM-TOC -->
* [Docker](#docker)
    * [1. Problem solved](#一solved problem)
    * [2. Comparison with virtual machines](#2. Comparison with virtual machines)
    *[三、Advantage](#三 Advantage)
    * [4. Usage Scenarios](#four Usage Scenarios)
    * [5. Mirrors and Containers](#五 Mirrors and Containers)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Problems solved

Since different machines have different operating systems, as well as different libraries and components, deploying an application to multiple machines requires a lot of environment configuration operations.

Docker mainly solves environment configuration problems. It is a virtualization technology that isolates processes. The isolated processes are independent of the host operating system and other isolated processes. Using Docker, existing applications can be deployed on other machines without modifying the application code and without requiring developers to learn the technology of a specific environment.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/011f3ef6-d824-4d43-8b2c-36dab8eaaa72-1.png" width="400px"/> </div><br>

## 2. Comparison with virtual machines

Virtual machine is also a virtualization technology. The biggest difference from Docker is that it simulates hardware and installs an operating system on the hardware.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/be608a77-7b7f-4f8e-87cc-f2237270bf69.png" width="500"/> </div><br>

### Startup speed

Starting a virtual machine requires first starting the virtual machine's operating system and then starting the application. This process is very slow;

Starting Docker is equivalent to starting a process on the host operating system.

### Occupying resources

A virtual machine is a complete operating system that requires a large amount of disk, memory, and CPU resources. One machine can only open dozens of virtual machines.

Docker is just a process. It only needs to package applications and related components. It takes up very few resources during runtime. One machine can open thousands of Dockers.

## 3. Advantages

In addition to fast startup and low resource usage, Docker has the following advantages:

### Easier to migrate

Provide a consistent operating environment. Packaged applications can be migrated to different machines without worrying about environment changes causing inability to run.

### Easier to maintain

Use layering techniques and mirroring to make it easier to reuse duplicate parts of your application. The higher the degree of reuse, the easier the maintenance work will be.

### Easier to expand

The basic image can be further expanded to obtain new images, and the official and open source communities provide a large number of images. By extending these images, it is very easy to get the image we want.

## 4. Usage scenarios

### Continuous integration

Continuous integration refers to frequently integr
ating code into the trunk so that errors can be discovered faster.

Docker is lightweight and isolated, and integrating code into one Docker will not affect other Dockers.

### Provide scalable cloud services

Docker can be easily added or removed based on application load.

### Build a microservice architecture

The lightweight nature of Docker makes it very suitable for deploying, maintaining, and combining microservices.

## 5. Mirrors and Containers

An image is a static structure that can be regarded as a class in object-oriented, and a container is an instance of an image.

The image contains the code and other components required for the container to run. It is a hierarchical structure, and each layer is read-only (read-only layers). When building an image, it is built layer by layer, with the previous layer being the basis for the next layer. This hierarchical storage structure of the image is very suitable for image reuse and customization.

When building a container, a writable layer is added to the image to save modifications during the running of the container.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/docker-filesystems-busyboxrw.png"/> </div><br>

## References

- [DOCKER 101: INTRODUCTION TO DOCKER WEBINAR RECAP](https://blog.docker.com/2017/08/docker-101-introduction-docker-webinar-recap/)
- [Docker Getting Started Tutorial](http://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)
- [Docker container vs Virtual machine](http://www.bogotobogo.com/DevOps/Docker/Docker_Container_vs_Virtual_Machine.php)
- [How to Create Docker Container using Dockerfile](https://linoxide.com/linux-how-to/dockerfile-create-docker-container/)
- [Understanding Docker (2): Docker image](http://www.cnblogs.com/sammyliu/p/5877964.html)
- [Why use Docker? ](https://yeasy.gitbooks.io/docker_practice/introduction/why.html)
- [What is Docker](https://www.docker.com/what-docker)
- [What is continuous integration? ](http://www.ruanyifeng.com/blog/2015/09/continuous-integration.html)
