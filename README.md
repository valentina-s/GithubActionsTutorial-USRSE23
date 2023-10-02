# GitHub Actions for Scientific Data Workflows

In this tutorial we will introduce Github Actions as a tool for lightweight automation of scientific data workflows. GitHub Actions have become a key tool of the software development lifecycle, however, many scientific programmers who are not involved in software deployment may not be familiar with their functionalities and/or do not know how they can be applied within their data pipeline. Through a sequence of examples, we will demonstrate some of GitHub Actions' applications to automating data processing tasks, such as scheduled deployment of algorithms to streaming data, updating visualizations based on new data, model versioning and performance benchmarking. For the demonstration we will access a public hydrophone stream and compute and visualize statistics of sound patterns. The goal is that participants will leave with their own ideas on how to integrate Github Actions in their own work. 


**Prerequisites:** GitHub account, basic familiarity with git, Github, and version control, programming in a scripting language such as Python/R

**Audience:** scientific programmers interested in automating components of their workflows through existing tools for software continuous integration/deployment.

**Key Learning Objectives:**

* Learners distinguish between Github Actions and Workflows and understand their role within the software development cycle
* Learners are capable of triggering GitHub Action Workflows in several different ways and can determine which method could be useful in typical data science applications
* Learners can export (data) outputs of Github Action Workflows, e.g. tables, plots.

For introduction to GitHub Actions see [here](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions).

# Orcasound Spectrogram Visualization Workflow

Orcasound GitHub Actions workflow (located at `.github/workflows/orcasound_processing.yml`) has manual trigger [`dispatch_workflow`](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow). It downloads the full timestamp "directory" from Orcasound AWS bucket (see more [here](https://github.com/orcasound/orcadata/blob/master/access.md)) and processes each file individually. For now you will have to manually change timestamp in the workflow file. If you want to change processing from creating spectrograms to something else look for the loop `for input_wav in sorted(glob.glob("wav/*.wav")):` at the end of the source file (`orcasound_processing.py`).

# Spectrogram
After the workflow is executed a `spec.png` file is update in the repo and is visualized below.
![alt text](https://raw.githubusercontent.com/valentina-s/orca-action-workflow-test/main/bush_point/1618317018/spec.png)
