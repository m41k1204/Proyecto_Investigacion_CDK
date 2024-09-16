from aws_cdk import (
    Stack,
    CfnParameter,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
)
from constructs import Construct

class ProyectoCdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        instance_name = CfnParameter(self, "InstanceName",
            type="String",
            default="MV Websimple & Webplantilla",
            description="Website Websimple & Webplantilla"
        )

        ami_id = CfnParameter(self, "AMI",
            type="String",
            default="ami-0aa28dab1f2852040",
            description="id de AMI"
        )

        vpc = ec2.Vpc.from_lookup(self, "VPC",
            is_default=True
        )

        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
            vpc=vpc,
            description="ssh y http",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        role = iam.Role.from_role_arn(self, "ExistingRole", "arn:aws:iam::484885772849:role/LabRole")

        instance = ec2.Instance(self, "EC2Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group,
            key_name="vockey",
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(20)
                )
            ],
            role=role
        )

        instance.add_user_data(
            "#!/bin/bash",
            "cd /var/www/html/",
            "git clone https://github.com/utec-cc-2024-2-test/websimple.git",
            "git clone https://github.com/utec-cc-2024-2-test/webplantilla.git",
            "ls -l"
        )

        CfnOutput(self, "InstanceId",
            description="ID de la instancia EC2",
            value=instance.instance_id
        )

        CfnOutput(self, "InstancePublicIP",
            description="IP publica de la instancia",
            value=instance.instance_public_ip
        )

        CfnOutput(self, "websimpleURL",
            description="URL de websimple",
            value=f"http://{instance.instance_public_ip}/websimple"
        )

        CfnOutput(self, "webplantillaURL",
            description="URL de webplantilla",
            value=f"http://{instance.instance_public_ip}/webplantilla"
        )
