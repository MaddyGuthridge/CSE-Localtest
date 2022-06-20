# localtest

A program so you don't need to use VLab anymore.
 - Fetch starter code
 - Run autotests
 - Complete submissions

# This software is archived

I don't intend to maintain this code anymore. If you think it is useful, feel 
free to use it in your own projects. Be warned, it was a first-year project, so 
it is exceptionally poorly designed, and will need a lot of reworking though.

# Installation

1. Ensure you are using MacOS, Linux, or Windows Subsystem for Linux (WSL).
Note that as Windows is vastly different to Linux and MacOS, results may differ 
when programming with it and as such, it is recommended to use WSL.
2. Launch a terminal and `cd` into a folder where you want to install Localtest.
3. Run the command 
`git clone https://github.com/MiguelGuthridge/CSE-Localtest.git` to download the
required files. This will download them to a folder named CSE-Localtest.
3. `cd` into this folder.
4. Install the required Python modules by running 
`pip3 install -r requirements.txt`. If you get an error, you may not have Python
installed. Install python from the 
[official website](https://www.python.org/downloads/), ensuring you choose the
correct version for your OS. If you are using Linux or WSL, install it using 
your package manager (eg `apt install python3.8`). After installing Python, try 
running the command again.
5. Run the installation script by running the command `python3 install.py`.
This will add Localtest to the alias files for both ZSH and Bash. For other
shells, you will need to add the alias it prints manually. Consider submitting a
pull request adding support for your favourite shell!
6. Make localtest.py executable by running `chmod +x localtest.py`
7. Restart your terminal. Localtest is now ready to use.

## Requirements:
* Git (for self-updating)
* Python (I tested using 3.8.10)
* Python modules:
  * Colorama
  * Paramiko
  * Getpass
* Linux or Windows Subsystem for Linux (it might work on MacOS but I'm not 
sure). Writing your code in Windows without the Linux subsystem is not 
recommended for UNSW COMP courses.

# Usage

Usually, a directory can be set up for use by running the command 
`localtest setup [course] [project]`. This will create a `localtest.json` file 
that is used to determine how autotests and submissions are run. If it is 
provided, then it will also download starter code. If a project configuration 
isn't found, refer to the section *Making a Manual Configuration*.

**Testing exercises**: run `localtest test` to test all exercises, or 
`localtest test [exercise name]` to test an individual exercise.

**Submitting exercises**: run `localtest give` to submit all exercises, or 
`localtest give [exercise name]` to submit an individual exercise.

**Copying files to VLab**: run `localtest upload` to copy all files in the 
directory to VLab.

**Displaying project instructions**: run `localtest instruct` to open the 
instruction page for the project in your web browser.

**Updating Localtest**: run `localtest update` to run a `git pull` command to 
update Localtest (requires the program to have been installed using a 
`git clone` command).

When running a `test` or `give` command, adding a `-v` argument will cause all 
output to be printed regardless of whether it submitted or not. This is great 
people with trust issues.

# Making a Manual Configuration

For some work (tests and exams), setup configurations are not provided to 
prevent seeing the questions in advance.For such cases, you should create a 
manual configuration based on the default template.

You can do this by running `localtest setup default`. You can fill out the 
`localtest.json` file using the following specifications:

* `course`: course code of the course this project applies to (eg `1511` for 
COMP1511). Used when running autotests and submitting, eg 
`*1511* autotest my_exercise` or `give cs*1511* thing`.

* `project`: name of the project being worked on (eg `lab01` for Lab 1). Used 
when submitting, eg `give cs1511 *lab01*_motd`.

* `starter_code`: bash command used to gather starter code on VLab. This command 
is run on a CSE machine during `localtest setup`, before the resulting files are 
copied to the local machine.

* `exercises`: list of dictionaries describing individual exercises of the 
project. Each exercise matches the following specification:

   * `name`: name that is presented when submitting or running tests.
   * `identifier`: name used to identify the exercise in autotests and 
   submissions, eg in the command `1511 autotest *hello_world*`.
   * `files`: list of filenames associated with the exercise, used when 
   submitting code, eg in the command `give cs1511 lab01_*hello_world*`.

If you go through the effort of creating one of these files yourself, I'd love 
it if you created a pull request so that others can access your work too. The 
json file should be stored under `setups/course_number/project_name.json`.

# Including Extra Files in Tests and Submissions

If you need to include extra files in your tests or submissions, you can 
modify the `localtest.json` file for your project, adding extra files to the
files list of any required exercises.
