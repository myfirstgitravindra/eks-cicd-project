#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack import EksCicdStack

app = cdk.App()
EksCicdStack(app, "EksCicdStack")
app.synth()
