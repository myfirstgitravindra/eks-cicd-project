from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_ecr as ecr,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct


class EksCicdStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- VPC (small, 1 NAT gateway to save cost) ---
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

        # --- ECR repo for our app image ---
        repo = ecr.Repository(
            self, "AppRepo",
            repository_name="eks-cicd-app",
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        # --- IAM role for cluster admin access (so kubectl from Jenkins EC2 can manage it) ---
        cluster_admin_role = iam.Role(
            self, "ClusterAdminRole",
            assumed_by=iam.AccountRootPrincipal(),
        )

        # --- EKS Cluster (small single small node to stay cheap) ---
        cluster = eks.Cluster(
            self, "EksCluster",
            vpc=vpc,
            cluster_name="cicd-demo-cluster",
            version=eks.KubernetesVersion.V1_29,
            default_capacity=0,          # we add nodegroup manually below
            masters_role=cluster_admin_role,
        )

        cluster.add_nodegroup_capacity(
            "AppNodeGroup",
            instance_types=[ec2.InstanceType("t3.small")],
            min_size=1,
            max_size=2,
            desired_size=1,
            disk_size=20,
        )

        # Allow the cluster to pull from our ECR repo
        repo.grant_pull(cluster.default_nodegroup_role) if cluster.default_nodegroup_role else None
