#!/usr/bin/env python3
import os
import aws_cdk as cdk
from proyecto_cdk_python.proyecto_cdk_python_stack import ProyectoCdkPythonStack

app = cdk.App()
ProyectoCdkPythonStack(app, "ProyectoCdkPythonStack",
    env=cdk.Environment(account="484885772849", region="us-east-1")
)
app.synth()
