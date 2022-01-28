# Terraform Monorepo Example

This repo is an example to help you to scale your Terraform monorepo in an organized way.

## Overview

This is our basic structure. Let's dive into it.

- `infra-live`: Here you would separate your resources per environment, and inside this folder you can organize the resources in your own way. What matters here is that the pattern is known inside your organization and the people know how to deal with it
- `modules`: Here you would create your own reusable modules. Keep in mind that you can find lots of open source modules from the community, so my recommendation is to look over Github if someone already built a module for your use case. Common modules you can find out there, for example [terraform-aws-vpc](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest), cover pretty much everything you need to provision a VPC on AWS, so probably is not worth building your own.
- `.tfgen.yaml`: This is a config file used by a tool I created to help us to create boilerplate code for our modules, increasing productivity and reducing risks of making mistakes during copy+paste operations. You can check it [tfgen here](https://github.com/refl3ction/tfgen).

```md
.
├── README.md
├── infra-live
│   ├── dev
│   │   ├── networking
│   │   ├── s3
│   │   ├── stacks
│   │   └── .tfgen.yaml
│   ├── prod
│   │   ├── networking
│   │   ├── s3
│   │   ├── stacks
│   │   └── .tfgen.yaml
│   └── .tfgen.yaml
└── modules
    └── my-custom-module
        └── main.tf
```

## `infra-live` organizaiton

Our `infra-live` folder will contain all our actual infrastructure, separated by environment. Considering an environment folder, you can organize it in several ways, for example:

### Folders by resources

You can create individual folders for each resources in the cloud, so you would have something like this:

```txt
.
├── ec2
├── rds
│   └── my-database-1
├── iam
│   ├── roles
│   └── users
├── s3
│   └── my-bucket-1
└── vpc
```

### Folders by type

You can create folders based on the resources type (compute, security, networking, etc):

```txt
.
├── compute
│   ├── my-asg
│   └── my-eks-cluster
├── security
│   └── iam
│       ├── roles
│       └── users
├── storage
│   ├── rds
│   └── s3
└── networking
│   ├── vpc
│   └── vpc-peering
```

### Mixed

Using this pattern you'll have a mix of the other two. Let's talk about the `stacks` folder. Sometimes you have an app that use multiple cloud resources, like `SQS Queues`, `SNS Topics`, `S3 Buckets`, so it could be confused to deploy these resources in different places, so maybe it makes sense to have a module just for this app. You could add it to the `stacks` folder, and deploy all of them together.

```txt
.
├── compute
│   ├── my-asg
│   └── my-eks-cluster
├── security
│   └── iam
│       ├── roles
│       └── users
├── stacks
│   ├── my-app-stack-1
│   └── my-app-stack-2
├── s3
│   ├── my-bucket-1
│   └── my-bucket-1
└── networking
│   ├── vpc
│   └── vpc-peering
```

## Files organization

To organize your files and have a pattern across multiple modules, somo common files you can have are the following:

- `_backend.tf`: Put your backend configuration here
- `_dependencies.tf`: Whenever you need to query data from the state or the cloud, add it here
- `_provider.tf`: Your providers configuration
- `_vars_.tf|_variables.tf`: The variables declaration

[tfgen](https://github.com/refl3ction/tfgen) is a tool that will help you to create these files from generic templates. Give it a try!
