# Connection to IFB cluster

There are two ways for connecting to IFB cluster: SSH and Open on demand.

- SSH

  1. First you need to upload your public key to <https://my.cluster.france-bioinformatique.fr/manager2/login>
  2. Then execute the following command line (replace `mylogin` by your IFB cluster login that is available on your IFB account):

```bash
ssh -X -o ServerAliveInterval=60 -l mylogin core.cluster.france-bioinformatique.fr
```

  - Command line explanation:
    - `-X`: enable X11 forwarding (for GUI applications)
    - `-o ServerAliveInterval=60`: Avoid timeout by sending every 60 seconds a message to SSH server
    - `-l mylogin`: define the account to use


You can find more information on IFB website: <https://my.cluster.france-bioinformatique.fr/manager2/login>



- Open on demand


  - Use the following link to connect to the IFB On Demand service: <https://ondemand.cluster.france-bioinformatique.fr/>
  - You can find more information on IFB website: <https://ifb-elixirfr.gitlab.io/cluster/doc/software/openondemand/>

[comment]: # TODO Check the version of Nextflow to use

::: boxed
**Exercise 1:**

Connect to the IFB cluster using SSH or Open on demand.
:::


# Connection to compute node and downloading example data

1. Open a session on a compute node:
```bash
srun --account=2557_anf_workflow --pty bash
```

2. Create and go to your working directory
```bash
mkdir -p /shared/projects/2557_anf_workflow/participants/$USER
cd /shared/projects/2557_anf_workflow/participants/$USER
```

3. Download example data
```bash
git clone https://gitlab.com/anf-workflow-et-reproductibilite/conteneurs.git
mv conteneurs/data .
rm -rf conteneurs
```

4. Display the version of Apptainer
```bash
apptainer version
```

→ Now you are ready to start


# Interacting with images

In this first part of the practical session, we want to execute the [cowsay](https://en.wikipedia.org/wiki/Cowsay) program using Apptainer. 
The `cowsay` is just a software that generates ASCII art pictures of a cow with a message. As an example, the following command line:
```bash
cowsay "ANF Workflow et reproductibilité 2025"
```
will produce as output:
```
 __
< ANF Workflow et reproductibilité 2025  >
 --
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
::: boxed
**Exercise 2:**

Try to execute the `cowsay` program. Check that is not installed on the IFB cluster.
:::


Now, we download an Apptainer image that contains the `cowsay` program:
```bash
apptainer pull docker://ghcr.io/apptainer/lolcow
```
::: boxed
💡 **Note 1:** We use here a Docker repository as source for the image.
Apptainer convert the Docker/OCI image in Apptainer/Singularity image format (*.sif* file).
:::

::: boxed
**Exercise 3:**

Download/pull the cowsay Apptainer. Check that a *lolcow_latest.sif* file has been created in your current directory.
:::


To execute a single command inside an Apptainer container, we use the following command:
```bash
apptainer exec myimage.sif command
```
::: boxed
**Exercise 4:**

Execute cowsay in an Apptainer contain that display "ANF Workflow et reproductibilité 2025"
:::

<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Command line to execute:
```bash
apptainer exec lolcow_latest.sif cowsay "ANF Workflow et reproductibilité 2025"
```
:::
</details>


::: boxed
**Exercise 5:**

Compare the output the `id`, `whoami`, `ls -l` and `ls -l /` commands inside and outside a container created using the *lolcow_latest.sif* image.
What are the differences? Why there are these differences?
:::


You can also execute the default command within a container:
```bash
apptainer run myimage.sif
```
::: boxed
**Exercise 6:**

Execute the default command for the cowsay Apptainer image.
Try to add additional parameters to the command line.
:::
<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Command line to execute:
```bash
apptainer run lolcow_latest.sif
```
:::
</details>

At last, you can use an Apptainer image in interactive mode.
To do this use the following command:
```bash
appatainer shell myimage.sif
```
::: boxed
**Exercise 7:**

Create a container from the *lolcow_latest.sif* image in interactive mode.
Execute the `cowsay` command, explore the tree directory of the container and try to execute other command in the container.
:::


# Creating Apptainer images

To create an Apptainer image, you need to write a definition file.
Definitions files have the same role as Dockerfile, but the syntax is very different.
Here, in the following example, we define a *lolcow.def* file that will produce an Apptainer image that works like the image that we used in the previous section of the practical session.

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt --yes update
    apt --yes install cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    date | cowsay | lolcat
```

We can see one header and 3 sections in this file.


The header (here the first two lines), define which base image we will use.
There is many type of [bootstrap agents](https://apptainer.org/docs/user/1.0/appendix.html#buildmodules), but the most used are "docker" and "localimage" (for existing images saved on your machine).
In this example, we will use the Docker image for Ubuntu 24.04 as the base for the image you want to create.


The first section `%post`, contains command are the executed for downloading and installing software in the image.
The next section `%environment`, define the environment variables that will be set when running the container.
And the last section, define the default command that will be executed when the container is executed with `apptainer run` command.


You can add many more sections in a definition file, they are described in [Apptainer documentation](https://apptainer.org/docs/user/main/definition_files.html).


Once, your definition file is ready, you can create your image with the following command line:
```bash
apptainer build lolcow.sif lolcow.def
```

::: boxed
**Exercise 8:**

Create an Apptainer image *lolcow.sif* from the *lolcow.def* file.
Execute the created image with the `apptainer run` command.
:::




<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Writing the *lolcow.def* file:
```bash
cat > lolcow.def << EOF
Bootstrap: docker
From: ubuntu:24.04

%post
    apt --yes update
    apt --yes install cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    date | cowsay | lolcat
EOF
```
- Creation of the *lolcow.sif* image:
```bash
apptainer build lolcow.sif lolcow.def
```
- Executing a command inside a container created from the *lolcow.sif* image:
```bash
apptainer run lolcow.sif
```
:::
</details>




# Creating an Apptainer image with the `classify.py` script

The following Bash script allows the installation of the *classify.py* script on an Ubuntu machine.

```bash
#!/bin/bash

# With environment variable no question will be prompt when installing Debian/Ubuntu packages
export DEBIAN_FRONTEND=noninteractive

# Install Python 3 and pip
apt update
apt install --yes python3 python3-pip wget git

# Install required dependencies of classify.py using pip
pip3 install --break-system-packages torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
pip3 install --break-system-packages ftfy==6.3.1 regex==2025.11.3 tqdm==4.67.1
pip3 install --break-system-packages git+https://github.com/openai/CLIP.git

# Download and install the classify.py in /usr/local/bin
cd /tmp
wget https://gitlab.com/anf-workflow-et-reproductibilite/classify/-/raw/main/classify.py
mv classify.py /usr/local/bin/
chmod +x /usr/local/bin/classify.py

# Cleaning
apt remove --purge --yes wget git
apt clean
```

::: boxed
**Exercise 9:**

Create a definition file named *classify.def* that contains the Bash command for creating a working Apptainer image with the *classify.py* script.
Create the *classify.sif* Apptainer image from the *classify.def* file.
:::

<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Writing the *classify.def* file:
```bash
cat > classify.def << EOF
Bootstrap: docker
From: ubuntu:24.04

%post
    # With environment variable no question will be prompt when installing Debian/Ubuntu packages
    export DEBIAN_FRONTEND=noninteractive

    # Install Python 3 and pip
    apt update
    apt install --yes python3 python3-pip wget git

    # Install required dependencies of classify.py using pip
    pip3 install --break-system-packages torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
    pip3 install --break-system-packages ftfy==6.3.1 regex==2025.11.3 tqdm==4.67.1
    pip3 install --break-system-packages git+https://github.com/openai/CLIP.git

    # Download and install the classify.py in /usr/local/bin
    cd /tmp
    wget https://gitlab.com/anf-workflow-et-reproductibilite/classify/-/raw/main/classify.py
    mv classify.py /usr/local/bin/
    chmod +x /usr/local/bin/classify.py

    # Cleaning
    apt remove --purge --yes wget git
    apt clean
EOF
```
- Creation of the *classify.sif* image:
```bash
apptainer build classify.sif classify.def
```
:::
</details>

::: boxed
💡 **Note 2:** If the build of the *classify.sif* image fails, you can download this file using the following command:
```bash
wget https://gitlab.com/anf-workflow-et-reproductibilite/conteneurs/-/raw/main/apptainer-images/classify.sif
```
:::


The following command executes the `classify.py` script with some data.
```
classify.py --image data/aussie.png --labels 'cat,dog,cute_dog'
```

::: boxed
**Exercise 10:**

Execute the previous command in an Apptainer container using the previously created *classify.sif* image.
:::

<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Command line to execute:
```bash
apptainer exec classify.sif classify.py --image data/aussie.png --labels 'cat,dog,cute_dog'
```
:::
</details>

::: boxed
**Exercise 11 (Optional):**

Using a Bash loop, process all the images in the *data* directory like in the previous exercise.
:::
<details>
<summary>Click to see an exercise solution</summary>

::: boxed
- Command line to execute:
```bash
for f in data/*.png; do 
  echo -ne "$f\t"
  apptainer exec classify.sif classify.py --image "$f" --labels 'cat,dog,cute_dog'
done
```
:::
</details>

