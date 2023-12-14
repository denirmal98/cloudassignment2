# Installing Apache Spark on macOS using Homebrew

## Docker Image
You can access the Docker image for this project [here](https://hub.docker.com/repository/docker/nd439/cloudassignment2/general).

## Install Homebrew
If Homebrew is not installed on your machine, you can install it by executing the following command in your terminal:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

# Install Apache Spark and Hadoop
Once Homebrew is installed, use it to install Apache Spark and Hadoop by running the following commands:

```bash
brew install apache-spark
brew install hadoop
```

# Set Environment Variables
Configure the environment variables `SPARK_HOME` and `HADOOP_HOME` in your shell configuration file (e.g., `.bash_profile`, `.zshrc, etc.). Open the file in a text editor and add the following lines:

```bash
export SPARK_HOME=/usr/local/opt/apache-spark/libexec
export HADOOP_HOME=/usr/local/opt/hadoop
```

Save the file and either restart your terminal or run `source ~/.bash_profile` (or the corresponding command for your shell) to apply the changes.

# Verify Installation
To confirm the installation, run Spark's built-in example:

```bash
spark-shell
```

If the setup is correct, you should see the Spark shell prompt.

# Installing AWS-CLI on Mac

## For Sudo Users
If you have sudo permissions, you can install the AWS CLI for all users on the computer using the following commands:

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

# Verify AWS-CLI Installation
To verify the AWS CLI installation, check the version:

```bash
which aws
/usr/local/bin/aws
aws --version
```

This ensures that the `aws` command is in your `$PATH` and provides information about the installed AWS CLI version.


# Setup Cluster on AWS
# Setting Up Amazon EMR on AWS

1. **Navigate to EC2 -> Create Cluster:**
   Access the Amazon EMR service in the AWS Management Console and choose to create a new cluster.

2. **Provide Cluster Name:**
   Assign a name to your cluster.

3. **Select Amazon EMR Release -> emr-6.15.0:**
   Choose the desired Amazon EMR release version for your cluster.

4. **Configure Cluster: Add Instance Group:**
   Click on "Cluster Configuration" and add an instance group to create a 4-node cluster group.

5. **Security Configuration and EC2 Key Pair:**
   Configure the security settings and EC2 key pair for SSH access to the cluster.

6. **Select Roles:**
   Choose the necessary roles:
   - Amazon EMR service role: EMR_DefaultRole
   - EC2 instance profile for Amazon EMR: EMR_DefaultRole

7. **Create Cluster:**
   Finalize the configuration and create the cluster.

   After creating the cluster, open port 22 and specify the custom IP address in the security settings of the EC2 instances.

# Connect to EMR Instance

1. **Connect to SSH Server:**
   Use the following SSH command to connect to the EMR instance:

```bash
ssh -i "CS643-Cloud.pem" hadoop@ec2-3-92-224-244.compute-1.amazonaws.com
```

2. **Copy File from Local to EMR Instance:**
   Exit the EMR instance and use the following command to copy a file from your local machine to the EMR instance:

```bash
scp -i CS643-Cloud.pem ~/Desktop/ProgrammingAssignment2-main/training.py ubuntu@ec2-34-207-132-95.compute-1.amazonaws.com:~/trainingModel
```

Reconnect to the server using the SSH command.

3. **Create a Virtual Environment:**
   Navigate to your project folder and create a virtual environment (replace "venv" with your preferred name):

```bash
python -m venv venv
```

4. **Activate the Virtual Environment:**

```bash
source venv/bin/activate
```

5. **Install Project Dependencies:**

```bash
pip install -r requirements.txt
```

6. **Execute the Command:**

```bash
python training.py
```


# Setup Prediction on EC2 Instance

1. **Navigate to EC2:**
   Go to the AWS Management Console and access the EC2 service.

2. **Launch an Instance:**
   Click on "Launch Instance" to initiate the instance creation process.

Once the instance is created, connect using the SSH command:

```bash
ssh command
```

**Install Java:**
Both Apache Spark and Apache Hadoop require Java. Install OpenJDK with the following commands:

```bash
sudo apt update
sudo apt install openjdk-8-jdk
```

Add the following lines to the end of the file:

```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64   # Replace this path with the correct Java installation path
export PATH=$PATH:$JAVA_HOME/bin
```

**Install AWS-CLI:**
Using the package manager (e.g., apt on Ubuntu):

```bash
sudo apt update
sudo apt install awscli
```

Configure AWS CLI:

```bash
aws configure
```

**Install Hadoop:**

1. **Download and Extract Hadoop:**

```bash
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzvf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /opt/hadoop
```

2. **Configure Hadoop:**
   Edit ~/.bashrc or ~/.bash_profile and add:

```bash
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
```

Refresh your shell:

```bash
source ~/.bashrc   # or source ~/.bash_profile
```

3. **Test Hadoop Installation:**

```bash
hadoop version
```

**Install Spark:**

1. **Download and Extract Spark:**

```bash
wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xzvf spark-3.5.0-bin-hadoop3.tgz
sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
```

2. **Configure Spark:**
   Edit ~/.bashrc or ~/.bash_profile and add:

```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
```

Refresh your shell:

```bash
source ~/.bashrc   # or source ~/.bash_profile
```

3. **Test Spark Installation:**

```bash
spark-shell
```

**Setup Python in AWS EC2:**

## Python Environment Setup

1. **Install Python:**
   Download and install the latest Python version from [python.org](https://www.python.org/downloads/).

2. **Install `virtualenv`:**

```bash
pip install virtualenv
```

3. **Create a `Virtual Environment`:**

```bash
python -m venv venv
```

4. **Activate the `Virtual Environment`:**

```bash
source venv/bin/activate
```

5. **Install Project Dependencies:**

```bash
pip install -r requirements.txt
```

6. **Execute the Command:**

```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2 file_name.py
```

Replace `file_name.py` with your filename.

This sequence of steps guides you through setting up an EC2 instance, installing necessary software, and configuring Python for your project.

# Docker Image for Cloud Assignment 2

This Dockerfile is designed to set up an environment for Cloud Assignment 2, incorporating Python, Java, Spark, and Hadoop.

## Build Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and execute the following command:

```bash
docker build -t cloud-assignment-2 .
```

## Run Docker Container

After building the image, you can run a Docker container using the following command:

```bash
docker run -it cloud-assignment-2
```

## Deploy Docker Image to Docker Hub

### Build Docker Image

To build the Docker image for deployment, use the following command in the directory containing your Dockerfile:

```bash
docker build -t your-dockerhub-username/cloud-assignment-2:latest .
```

### Login to Docker Hub

Login to your Docker Hub account using the following command:

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

### Tag the Image

Tag the Docker image with your Docker Hub username and repository name, specifying the desired version or tag:

```bash
docker tag your-dockerhub-username/cloud-assignment-2:latest your-dockerhub-username/cloud-assignment-2:version-tag
```

Replace `version-tag` with the desired version for your Docker image.

### Push the Image

Push the tagged image to Docker Hub:

```bash
docker push your-dockerhub-username/cloud-assignment-2:version-tag
```

This step uploads the Docker image to your Docker Hub repository.

Now, your Docker image is available on Docker Hub and can be pulled and used by others. Users can run the image with:

```bash
docker run -it your-dockerhub-username/cloud-assignment-2:version-tag
```

Replace `version-tag` with the specific version or tag you want to run.

