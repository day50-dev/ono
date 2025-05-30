# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "<?ono get aws region from environment or default to us-west-2 ?>"
}

resource "aws_instance" "example" {
  ami           = "<?ono get appropriate ami id for ubuntu 20.04 in the selected region ?>"
  instance_type = "t2.micro"
}