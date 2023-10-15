# GitHub Actions for Scientific Data Workflows
Tutorial presented at [US-RSE'23 Conference](https://us-rse.org/usrse23/). 


In this tutorial we will introduce Github Actions as a tool for lightweight automation of scientific data workflows. GitHub Actions have become a key tool of the software development lifecycle, however, many scientific programmers who are not involved in software deployment may not be familiar with their functionalities and/or do not know how they can be applied within their data pipeline. Through a sequence of examples, we will demonstrate some of GitHub Actions' applications to automating data processing tasks, such as scheduled deployment of algorithms to streaming data, updating visualizations based on new data, model versioning and performance benchmarking. For the demonstration we will access a public hydrophone stream and compute and visualize statistics of sound patterns. The goal is that participants will leave with their own ideas on how to integrate Github Actions in their own work. 


**Prerequisites:** GitHub account, basic familiarity with git, Github, and version control, programming in a scripting language such as Python/R

**Audience:** scientific programmers interested in automating components of their workflows through existing tools for software continuous integration/deployment.

**Key Learning Objectives:**

* Learners distinguish between Github Actions and Workflows and understand their role within the software development cycle
* Learners are capable of triggering GitHub Action Workflows in several different ways and can determine which method could be useful in typical data science applications
* Learners can export (data) outputs of Github Action Workflows, e.g. tables, plots.

For introduction to GitHub Actions see [here](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions).

# GitHub Actions Introduction
* [slides]()

# Setup 
* Fork this repo
* Enable Github Actions:
  * Settings ->   Actions -> Allow actions and reusable workflows
  * [Managing Permissions Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository) 

# GitHub Actions Python Environment Workflow
First, we will run a basic workflow which creates a python environment with a few scientific packages and prints out their version
* [.github/workflows/python_env.yml](https://github.com/valentina-s/GithubActionsTutorial-USRSE23/blob/main/.github/workflows/python_env.yml)
* go to **Actions** tab, click on **Python Environment**, and click **Run workflow**: this will manually trigger the workflow ([`dispatch_workflow`](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow))
* click on the newly created run to see the execution progress

# Orcasound Spectrogram Visualization Workflow

Next, we will demonstrate how GitHub Actions can be used to display a spectrogram of a snippet from an underwater audio stream.

* [`.github/workflows/orcasound_processing.yml`](https://github.com/valentina-s/GithubActionsTutorial-USRSE23/blob/main/.github/workflows/orcasound_processing.yml)
* workflow steps:
  * download data from S3 for a particular timestamp
  * convert the last file from `.ts` to `.wav` format (in [`orcasound_processing.py`](https://github.com/valentina-s/GithubActionsTutorial-USRSE23/blob/main/orcasound_processing.py))
  * create and save spectrogram in `spec.png` (in [`orcasound_processing.py`](https://github.com/valentina-s/GithubActionsTutorial-USRSE23/blob/main/orcasound_processing.py))
  * upload `spec.png` to GitHub 

After the workflow is executed a `spec.png` file is updated in the repo and is visualized below.
![alt text](https://raw.githubusercontent.com/valentina-s/orca-action-workflow-test/main/bush_point/1618317018/spec.png)
