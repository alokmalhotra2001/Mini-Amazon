# Mini-Amazon (Database Daddies)
CompSci 316 Undergraduate Course Project for Team Database Daddies (Fall 2021)
Our team chose to complete the 'standard option' Mini-Amazon project

# Team Members and Roles
Our five team members and their corresponding primary roles in completion of this project:
1. Alok Malhotra - Guru of Carts (Cart/Order)
2. Rohin Shahi - Guru of Users (Account/Purchases)
3. OG Alilonu - Guru of Sellers (Inventory/Order Fulfillment)
4. Mimi Larrieux - Guru of Products (Products)
5. Ashley Lo - Guru of Socials (Feedback/Messaging)

# Previous Milestone - 1 (09/23/2021)
Team Database Daddies was created with all current team members.\
Decision was made to pursue the standard course project.

# Previous Milestone - 2 (10/07/2021)
###### Group Progress Report:
E/R designs were separately made and effectively integrated into one design. Tables were generated from resulting E/R design and web design intentions were shared and described. Database was created and populated with sample data.

###### Individual Progress Reports:
**Alok Malhotra** - Designed and created an E/R schema for a user's cart, orders, and order contents. Connected entities to other members' entities using relationship sets. Effectively translated E/R schema into tables in create.sql file. Populated tables with sample data. Developed web design for user's cart page and submitted orders page. \
**Rohin Shahi** - Designed and created an E/R schema for a user account and added features to order contents. Ensured user account was properly connected to other members' entities, and edited create.sql file appropriately. Populated tables with sample data. Developed web design for home page and helped develop web design for account/users in accordance with other teammates' entity constraints. \
**OG Alilonu** - Designed and created E/R schema and tables for a user's inventory and their membership as a seller. Ensured that every seller must belong to the user table and that every seller has an inventory table. Developed web design for inventory and order fulfillment from the seller's perspective, and helped to develop web design for a user's account. Populated tables with sample data. Translated E/R schema to tables in create.sql. \
**Mimi Larrieux** - Designed and created E/R diagram and tables to store listings, listings in carts, tags, and listings sold by sellers. Worked with other members to combine and create one large E/R diagram. Helped to organize meetings times and establish deadlines and expectations. Created csv files to populate by tables. Checked over work to ensure that there were no large discrepancies prior to submission. \
**Ashley Lo** - Designed and created E/R and tables to store product ratings, seller ratings, and messages. Translated E/R relations to create.sql. Populated tables with sample data. Created sample web design for message threads.

# Current Milestone - 3 (11/11/2021)
**Group Progress Report**: Our project progress report is outline on our attached REPORT.pdf

# Setup Instructions

We assume you are in your class VM.
If you have a different setup, your mileage with the following instructions may vary.

## Installing the Current Skeleton

1. Fork this repo by clicking the small 'Fork' button at the very top right [on Gitlab](www.example.com).
   It's important that you fork first, because if you clone the directory directly you won't be able to push changes (save your progress) back to Gitlab.
   Name your forked repo as you prefer.

2. In your newly forked repo, find the blue "Clone" button.
   Copy the "Clone with SSH" text.
   In your terminal on the VM, you can now issue the command `git clone THE_TEXT_YOU_JUST_COPIED`.
   Make sure to replace 'THE_TEXT_YOU_JUST_COPIED' with the "Clone with SSH" text.

3. In your VM, move into the repository directory and then run `install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.

4. If you are running a Google VM, to view the app in your browser, you may need to edit the firewall rules.
   The [Google VM instructions](https://sites.duke.edu/compsci316_01_f2021/creating-and-running-vm-on-google-cloud/) on the course page has instructions for how to add rules at the bottom.
   if those for some reason are outdated, here are [instructions provided by Google](https://cloud.google.com/vpc/docs/using-firewalls).
   Create a rule to open up port 5000, which flask will run on.

## Running/Stopping the Website

To run your website, in your VM, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```
The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).
If you are running a Google VM, you will need to point your browser to `http://vm_external_ip_addr:5000/`, where `vm_external_ip_addr` is the external IP address of your Google VM.

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

# Tips for Working on This Project

## Set up VS Code on Google Cloud VM

The following instructions also exist as a recorded video, which you can find [at this link](https://youtu.be/y-l6FLSsCz0).
If you need specific help setting up VSCode, the TAs will be able to help you in office hours.

1. First we need to set up SSH access through your local machine (Mac) to the Google VM.
   1. Create an SSH key-pair on your local machine. If you have a macOS, use: `ssh-keygen -f /Users/YOUR_MAC_USERNAME/.ssh/vm_316`. If you are on Windows, use: `ssh-keygen -f C:\Users\YOUR_WINDOWS_USERNAME\.ssh\vm_316`. Make sure to replace 'YOUR_XXX_USERNAME' with your local machine's username. For the passphrase, just hit enter to opt out.
   2. Now, we need to give the public key (`vm_316.pub`) to the VM instance on Google Cloud. You might have already done this if you followed along with the "SETTING UP AN SSH KEY PAIR TO ACCESS VMS" tutorial on the course website. If so, skip this.
      1. In your internet browser, go to Google Cloud and find the VM instance you want to be able to connect with. Click on its name and then click 'Edit' in the top bar.
      2. Find 'SSH Keys', click 'Show and edit'. The section will expand. Click on the '+ Add Item' button. Now keep this tab open, we are going to paste your key in here.
      3. Back in your local host terminal, run the command `cat /Users/YOUR_MAC_USERNAME/.ssh/vm_316.pub` The output will be your public key. Copy this text (all of it). 
      4. Paste the text into the text box you just opened in your browser. Before saving, however, edit the username at the very end of this key. The key will look something like "...OFUNwEsWO/dJNK user@MBP.local". Replace the last bit with your gmail username. That means it would look like this: "...OFUNwEsWO/dJNK gmailusername". Now click save.
2. Download Visual Studio Code (VS Code) from [this link](https://code.visualstudio.com/Download).
3. VS Code has a bunch of useful extensions. To use it with our VM we are going to need to download the 'remote-ssh' extension.
   - Open VS Code and click on the Extensions button in the left-most navigation bar. This button looks like a 3-block tetris piece with a 4th block hovering above it.
   - Search for an extension named 'Remote - SSH'. It will be the one by Microsoft with a description that begins with "Open any folder on a remote machine...". Click it and install the extension.
4. Now you're almost ready to log onto the VM. Open your browser again and find your VM Instances on Google Cloud. The IP Address will be listed under the 'External IP' column. Copy this IP address for the next step.
5. Open a new VS Code window, and click on 'Run a Command' (alternatively, use the shortcut `F1` or `⇧⌘P`). Type in 'Remote-SSH: Connect to Host', scroll down to 'add new host' and hit enter. Here, enter the username and IP address you just looked up like this, along with your local device username as before to specify where the private key is: `ssh -i /Users/YOUR_MAC_USERNAME/.ssh/vm_316 gmailusername@IP_adress`. The `-i` flag specifies to use the given private key instead of the default. If you already set up your SSH keys earlier, you can just issue the command `ssh gmailusername@IP_adress`.
6. You will be asked what type of platform the VM is. Select `Linux`.
7. Now you're connected! In the lower left corner of the window you'll see a green bar that reads "SSH: ...". You can access files and run things through the terminal just as you would be able to locally.

## Keep Track of Your Project with Gitlab: Merge Requests

These instructions seem long, but they aren't complicated.
If you've never worked with merge requests, make sure to read this thoroughly. 

To work on a gitlab project with many team members, you want to avoid working directly on the 'main' branch as much as possible. If multiple people work on this branch at the same time, you are likely to run into conflicts and be forced to restore old versions. This is a mess. Instead, use new branches every time you add a feature or make an edit, and then merge these into the main branch. This is how to do it:

Let's imagine we want to create a new function to help with some specific query of the database. Before you begin, create and checkout a new branch for this feature.
1. `git branch -b checkout query-feature` will create a branch named "query-feature". You can change the name as you'd like.
2. Once you are on this branch, get to work. Make the edits you need to the files you want to work on.
3. Run the command `git status` to see what files have changed. Let's say you only edit the file `app/db.py` to add the new function along with some comments, and `README.md` to include some information about this feature. These files will then appear in red under the title 'modified:'.
4. Now that you're done editing, you want to save your changes. Each save appears as a notification on gitlab in the form of a 'commit'. To be helpful, we save our edits in small chunks so that others can easily read these notifications and follow along which changes were made. Let's say we want to make two 'commits', one for `app/db.py` and another for `README.md`. 
   1. We make the first commit ready by adding the changes to `app/db.py` using the command `git add app/db.py`. Now, running `git status` will show the `app/db.py` file in green, indicating it is being tracked.
   2. Now we can commit this change using the command `git commit -m "MESSAGE"` We replace 'MESSAGE' with a short description of what the change entailed. This is what shows up in the notification on gitlab. For example: `git commit -m "created a new function to find the total amount spent by a user"`
   3. Now repeat this process for the `README.md` file. That is: `git add README.md`, then `git commit -m "updated readme to include description of 'all-time spending' feature"`.
   4. You've saved your changes! But they're still only local.. To upload them to gitlab you need to do is run `git push --set-upstream origin query-feature`.By now you should be able to see that you've made changes on the gitlab website. These changes appear in your repository under 'Repository'>'Branches'>'query-feature'.
5. To merge the changes into the main project so others can add on top of your work, you need to open a merge request. This request is an open invitation for your teammates to take a look at your code, make sure the changes look good to them, and then incorporate them onto the main branch for others to use. To open a merge request, click on 'merge requests' in the left hand navigation bar, and then hit the blue 'New merge request' button at the top right. It will ask you to select a source branch. For our example above this would be the `query-feature` branch. For the target branch, leave it as main.
6. Once the merge request is created, ping your teammates to take a look at it. If they think it's acceptable, they just need to click 'merge' and the code you've written get's incorporated. Now you can safely delete the `query-feature` branch on gitlab.
Done!

## Important! before you push to the repo: Hide Passwords

For all your password/secret key needs, use `.flaskenv`.
This file is NOT tracked by git and it was automatically generated when you first ran `install.sh` (from a template file).
You can change any credentials in this file.
Only share this file securely with your teammates, but don't check it into git.

You can randomly generate passwords with this tool: https://www.lastpass.com/password-generator
