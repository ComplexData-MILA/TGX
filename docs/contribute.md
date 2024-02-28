<!-- # TGX -->
![TGX logo](2023_TGX_logo.png)

# TGX Community Contribution Guidelines

TGX is a community driven project and we hope to continue to add new features to it so that it is useful for a wide range of analysis and scenarios. This guide documents the best way to make various types of contribution to TGX, including what is required before submitting a code change. Note that as the package evolves, this guideline will be improved as well, so feel free to check back here for more information in the near future too. 

Contributing to TGX is more than submitting code changes, we also welcome new research suggestions, inviting new users, testing releases and improving the documentation. Raising issues on Github to point out any issues or directions of improvement are also welcome. 


## Reporting issues on Github

Creating issues on Github is a useful way to manage problems and identify priorities. When possible, please add appropriate tags to the issue you are creating. For example, if it is related to the documentation website or error in documentation, you can include the `documentation` tag. If it is related to package installation, you can add the `install` tag. Overall, combining multiple issues that are related into a single one to report is also helpful to avoid trackig too many issues. 

### Bugs

Bug reports are useful when they are accompanied by ways to understand and reproduce the bug. When reporting a bug, try to include detailed steps on how you encountered the bug and how to reproduce it. If you would like to propose a fix to the bug, feel free to link it to a pull request on the issue as well.

### Feedbacks and Improvements

Feedbacks and improvements on TGX are welcome. If you would like to see new temporal graph statistics or visualization added, feel free to reach out directly by [email](mailto:shenyang.huang@mail.mcgill.ca) or create an issue on Github. You are of course more than welcome to add visualization and statistics from your own paper as well. 

## Preparing code changes

If you are interested in adding new features or fixing bugs in TGX, thanks for your help. This section walks you through on how to propose code changes to TGX. 

### Deciding what to work on

The first step is to decide on which aspects you want to improve for TGX. The best way is to look at currently [active issues](https://github.com/ComplexData-MILA/TGX/issues) on Github. You can find the future improvements we are planning in the [Roadmap](https://github.com/ComplexData-MILA/TGX/issues/43), from there you can find detailed instructions on what each task means. You are also very welcome to fix any bugs that you encounters or someone else encounters by proposing pull request on the github. Once you have decided on what you want to fix, reach out to us on TG slack (check the most recent link to join on the [TG website](https://www.cs.mcgill.ca/~shuang43/rg.html)) or by [email](mailto:shenyang.huang@mail.mcgill.ca) and let's work on it together. 

### setting up dev environment

First, identify the issue you want to solve and create a new branch linked to the issue. (see create a branch button on right side of the issue.) Install TGX to the latest version as instructed below.

1. Set up virtual environment (conda should work as well).

```
python -m venv tgx_env/
source tgx_env/bin/activate
```

2. Upgrade pip (Optional)
	
```
pip install --upgrade pip
```

3. Install external packages

```
pip install -r requirements.txt
```

4. Install local dependencies under root directory `/TGX`.

```
pip install -e .
```

5. Install `mkdocs` dependencies to serve the documentation locally. 

```
pip install mkdocs mkdocs-material mkdocstrings-python mkdocs-glightbox mkdocs-jupyter ipython_genutils
```

6. Switch to the branch you created from the issue (swap out `test` with name of your branch)
    ```
    git fetch origin

    git checkout -b test origin/test
    ```

### Creating Pull Request

please make sure you have tested your code before creating a pull request, also created documentation for any new functions that you have added. 
Once you created the pull request, you can reach out for a code review on slack or by email.