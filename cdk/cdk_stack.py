from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_ecr as ecr,
    aws_iam as iam,
    RemovalPolicy,
)
from aws_cdk.lambda_layer_kubectl_v32 import KubectlV32Layer
from constructs import Construct


class EksCicdStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "EksVpc",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24
                ),
            ],
        )

        repo = ecr.Repository(
            self, "AppRepo",
            repository_name="eks-cicd-app",
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        cluster_admin_role = iam.Role(
            self, "ClusterAdminRole",
            assumed_by=iam.AccountRootPrincipal(),
        )

        cluster = eks.Cluster(
            self, "EksCluster",
            vpc=vpc,
            cluster_name="cicd-demo-cluster",
            version=eks.KubernetesVersion.V1_32,
            kubectl_layer=KubectlV32Layer(self, "KubectlLayer"),
            default_capacity=0,
            masters_role=cluster_admin_role,
        )

        nodegroup = cluster.add_nodegroup_capacity(
            "AppNodeGroup",
            instance_types=[ec2.InstanceType("t3.small")],
            min_size=1,
            max_size=2,
            desired_size=1,
            disk_size=20,
        )

        repo.grant_pull(nodegroup.role)
