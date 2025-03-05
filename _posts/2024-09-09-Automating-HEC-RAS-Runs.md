---
layout: post
title: Automating HEC-RAS Unsteady Flow Runs for Sensitivity Analysis
author: Alex Thornton-Dunwoody
date: 2024-09-09
categories: HEC-RAS
---

# Automating HEC-RAS Unsteady Flow Runs for Sensitivity Analysis

When conducting hydrologic sensitivity analysis using HEC-RAS, it becomes essential to run multiple unsteady flow simulations with different input hydrographs. This allows you to explore how variations in discharge affect the extent of inundation and the distribution and magnitude of flow velocities. Doing this manually can be time-consuming and tedious, so in this post, I’ll walk you through automating HEC-RAS unsteady flow runs using Python, focusing on how to modify and execute multiple plans efficiently.

## Table of Contents
- [Introduction](#introduction)
- [Setting Up the Environment](#setting-up-the-environment)
- [Creating Unsteady Flow Files](#creating-unsteady-flow-files)
- [Modifying Plan Files](#modifying-plan-files)
- [Automating Plan Execution](#automating-plan-execution)
- [Exporting Results](#exporting-results)
- [Conclusion](#conclusion)

## Introduction
The goal of this workflow is to automate the modification and execution of HEC-RAS plans using unsteady flow files that represent different discharge values. We'll use a "psuedo-steady flow" analysis, where we ramp up flow in a hydrograph to a steady state flow.

We’ll cover how to:
- Create unsteady flow (.u##) files programmatically with varying discharge values.
- Modify plan files to point to new flow files.
- Run multiple plans in HEC-RAS using Python.
- Export and store the results for further analysis.

## Setting Up the Environment
To automate HEC-RAS runs, we’ll use the `pyHMT2D` package, a Python-based interface that allows you to programmatically interact with HEC-RAS. Start by cloning and installing the package**:

```bash
git clone https://github.com/atdunwoody/pyHMT2D
cd pyHMT2D
pip install -e .
```



### Ensure HEC-RAS is Installed

Ensure you have HEC-RAS installed on your system. This workflow is built on pyHMT2D, which currently requires HEC-RAS versions 5.0.7, 6.0.0, 6.1.0, 6.3.1 or 6.4.1. 

### Creating Unsteady Flow Files

To avoid solver instabilities in HEC-RAS, hydrographs should gradually ramp up to the desired discharge values. Below is a Python function that generates a hydrograph that ramps up the flow over a few steps:

```python
import numpy as np

def create_hydrograph(max_flow_value, ramp_steps=2, steady_steps=3):
    """
    Creates a hydrograph that ramps up to the max flow value.
    """
    ramp = [max_flow_value * (i + 1) / (ramp_steps ** 3) for i in range(ramp_steps)]
    steady = [max_flow_value] * steady_steps
    return ramp + steady
```

## Example Hydrograph

For instance, to create a hydrograph that ramps up to 10 cubic meters per second (cms):

```python
hydrograph = create_hydrograph(10)
print(hydrograph)
```

This will output a hydrograph array that can be inserted into an unsteady flow file.

## Updating the Unsteady Flow File
Once the hydrograph is created, the next step is to modify the .u## file to include the new hydrograph values:

```python
import os

def update_flow_hydrograph(input_file, new_hydrograph, max_flow_value):
    """
    Updates the Flow Hydrograph and Flow Title in the unsteady flow file.
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if line.strip().startswith("Flow Hydrograph="):
            lines[i] = f"Flow Hydrograph= {len(new_hydrograph)}\n"
            formatted_hydrograph = ''.join(f'{x:8.3f}' for x in new_hydrograph).rstrip()
            lines[i + 1] = formatted_hydrograph + '\n'
    
    new_file = f"{os.path.splitext(input_file)[0]}_updated.u01"
    with open(new_file, 'w') as file:
        file.writelines(lines)
    
    print(f"Updated file saved as {new_file}")
    return new_file
```
## Modifying Plan Files
HEC-RAS plan files point to specific geometry and unsteady flow files. Each plan file has a "Short Identifier" and a "Plan Title," which must be unique for each scenario.

Here’s how you can modify a plan file to reference a new flow file:

```python
def update_plan_file(file_path, new_flow_file, new_title):
    """
    Updates the Flow File and Short Identifier in the plan file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("Flow File"):
            lines[i] = f"Flow File={new_flow_file}\n"
        elif line.startswith("Short Identifier"):
            lines[i] = f"Short Identifier={new_title}\n"

    new_file_path = f"{os.path.splitext(file_path)[0]}_updated.p01"
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(lines)

    print(f"Updated file saved as {new_file_path}")
    return new_file_path
```
## Automating Plan Execution
Once the flow and plan files are created or updated, the next step is to automate the execution of multiple HEC-RAS runs. Using the pyHMT2D library, you can run HEC-RAS from Python as follows:

```python
import pyHMT2D

def run_HEC_RAS_plan(project_file, plan_file):
    my_hec_ras_model = pyHMT2D.RAS_2D.HEC_RAS_Model(version="6.1.0", faceless=False)
    my_hec_ras_model.init_model()
    my_hec_ras_model.open_project(project_file)
    my_hec_ras_model.set_plan(plan_file)
    
    my_hec_ras_model.run_model()
    my_hec_ras_model.close_project()
    my_hec_ras_model.exit_model()

    print(f"Successfully ran plan {plan_file}")
```
## Running Multiple Plans
You can loop through multiple plans and run them sequentially:

``` python
project_file = r"C:\HEC-RAS\MyProject\project.prj"
plans = ["p01", "p02", "p03"]
# Optionally leave plans empty to process all plans in a project
plans = []

for plan in plans:
    run_HEC_RAS_plan(project_file, plan)
```
## Exporting Results
HEC-RAS allows results to be exported in various formats, including GeoTIFF, through the Results dropdown of RAS Mapper. Currently, pyHMT2D only supports export to Visualization Toolkit (VTK) files, which are a 2.5D mesh product that can only be viewed in a 3D visualization software such as ParaView or Visit. 

## Conclusion

You can find the complete code for this post at my [GitHub repository](https://github.com/atdunwoody/hydraulic_modeling):

- `preprocessing/unsteady_flow_file_generator.py`
- `run_multiple_plans.py`

Happy modeling!

## Acknowledgements

This project was inspired by the following resources:

- Chris Goodell's book *Breaking the HEC-RAS Code*
- The `pyHMT2D` package developed by Xiaofeng Liu, Ph.D., P.E., at Penn State University.  
  GitHub: [https://github.com/psu-efd/pyHMT2D](https://github.com/psu-efd/pyHMT2D)

**Note**: This repository is forked from the original [pyHMT2D repository](https://github.com/psu-efd/pyHMT2D). A couple of dependencies were missing from the original environment, which have been resolved in this version.
