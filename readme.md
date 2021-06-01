# localtest

A program so you don't need to use VLab anymore.

# Installation

It is recommended that you install localtest by `git clone`ing the repository. That way, you will be able to easily update it by running `localtest update`.

You may also wish to add the python script to your `path` variable for easy invocation.

## Requirements:
* Git (for self-updating)
* Python (I tested using 3.8.5)
* Python modules:
  * Colorama (run `pip3 install colorama`)
  * Paramiko (run `pip3 install paramiko`)
* Linux or Windows Subsystem for Linux (it might work on MacOS but I'm not sure). Writing your code in Windows without the Linux subsystem is not recommended for UNSW COMP courses.

# Usage

Usually, a directory can be set up for use by running the command 
`localtest setup [course] [project]`. This will create a 
`localtest.json` file that is used to determine how autotests and 
submissions are run. If they are provided, then it will also 
download starter code. If a project configuration isn't found, refer 
to the section *Making a Manual Configuration*.

# Making a Manual Configuration

You can create a configuration based off the default template by 
running `localtest setup default`. You can fill out the 
`localtest.json` file using the following specifications:

* `course`: course code of the course this project applies to (eg 
`1511` for COMP1511). Used when running autotests and submitting, eg
 `*1511* autotest my_exercise` or `give cs*1511* thing`.

* `project`: name of the project being worked on (eg `lab01` for Lab
 1). Used when submitting, eg `give cs1511 *lab01*_motd`.

* `starter_code`: bash command used to gather starter code on VLab. 
This command is run on a CSE machine during `localtest setup`, 
before the resulting files are copied to the local machine.

* `exercises`: list of dictionaries describing individual exercises of the project. Each exercise matches the following specification:

   * `name`: name that is presented when submitting or running tests.
   * `identifier`: name used to identify the exercise in autotests and submissions, eg in the command `1511 autotest *hello_world*`.
   * `files`: list of filenames associated with the exercise, used when submitting code, eg in the command `give cs1511 lab01_*hello_world*`.

If you go through the effort of creating one of these files yourself, I'd love it if you created a pull request so that others can access your work too. The json file should be stored under `setups/course_number/project_name.json`.
