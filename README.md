# Terraform Monorepo Example

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/refl3ction/terraform-monorepo-example/graphs/commit-activity)
[![lang](https://img.shields.io/badge/Terraform-~%3E%201.0.0-blue)](https://github.com/refl3ction/tfgen)
[![GitHub stars](https://img.shields.io/github/stars/refl3ction/terraform-monorepo-example.svg?style=social&label=Star)](https://github.com/refl3ction/terraform-monorepo-example/stargazers/)

Learn how to design a scalable Terraform monorepo

## Tools

- [tfgen](https://github.com/refl3ction/tfgen) - We use tfgen to generate Terraform boilerplate code for our modules, like backend, provider configuration and variables
- [tfenv](https://github.com/tfutils/tfenv) - Terraform version manager, to switch to different version between modules automatically

## Overview

### High level folders

- `infra-live`: Here you would separate your resources per environment, and inside this folder you can organize the resources in your own way. What matters here is that the pattern is known inside your organization and the people know how to deal with it
- `modules`: Here you would create your own reusable modules. Keep in mind that you can find lots of open source modules from the community, so my recommendation is to look over Github if someone already built a module for your use case. Common modules you can find out there, for example [terraform-aws-vpc](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest), covers pretty much everything you need to provision a VPC on AWS, so probably it is not worth building your own.
- `.tfgen.yaml`: This is a config file used by a tool I created to help us to create boilerplate code for our modules, increasing productivity and reducing risks of making mistakes during copy+paste operations. You can check it [tfgen here](https://github.com/refl3ction/tfgen).

```md
.
├── README.md
├── infra-live
│   ├── dev
│   │   ├── networking
│   │   ├── s3
│   │   ├── security
│   │   ├── stacks
│   │   └── .tfgen.yaml
│   ├── prod
│   │   ├── networking
│   │   ├── s3
│   │   ├── security
│   │   ├── stacks
│   │   └── .tfgen.yaml
│   └── .tfgen.yaml
└── modules
    └── my-custom-module
        └── main.tf
```

## Patterns

Let's cover some patterns to organize the `infra-live` folder, which will contain all the actual infrastructure, separated by environment. Considering an environment folder, you can organize it in several ways.

### By resource

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

### By resource group

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
    ├── vpc
    └── vpc-peering
```

### Mixed

Using this pattern you'll have a mix of the previous two.

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
    ├── vpc
    └── vpc-peering
```

#### Stacks

Let's talk about the `stacks` folder. Sometimes you have an app that uses multiple cloud resources, like `SQS Queues`, `SNS Topics`, `S3 Buckets`, so it could be confused to deploy these resources in different places, so maybe it makes sense to have a module just for this app. You could add it to the `stacks` folder, and deploy all of them together. If you do that, makes sense to give all the resources some kind of prefix, ideally the name of the app that uses it.

> This pattern can get trick if you have a resources that's shared between more than one app, for example a `SQS Queue` that have a consumer and a writer.

## Files organization

To organize your files and have a pattern across multiple modules, you can name your files like this:

- `_backend.tf`: Put your backend configuration here
- `_dependencies.tf`: Whenever you need to query data from the state or the cloud, add it here
- `_provider.tf`: Your providers configuration
- `_vars_.tf|_variables.tf`: The variables declaration
- `main.tf`: The modules and resources declaration

## Anti-Patterns

Some anti-patterns I observed and heard about

### Single module for the entire infrastructure

In my opinion this is the most common anti-pattern. Some people may argument that having a module that deploys the entire infrastructure is a good thing and will be useful in a disaster recovery situation. But the problem is, that you probably never gonna need to do that. The operational overhead for keeping this structure will not be paid by the "benefit" it offers.

In addition, we have other problems by using this structure:

- All the `plans/applies` will take a long time to run, and it will just get worse as your infrastrcture grows. The `-target` option should be used just in exceptional circunstances, as mentioned in the Terraform documentation.
- The companies will grow with time, so will the need for deploying cloud resources and people contributing to the project. Having just one module will be `impracticable`. Velocity will be severely reduced.
- High risk of messing something up.

So, if you see something like this, ~~run~~ show them this repo!

```txt
.
└── entire-infra-module
    ├── backend.tf
    ├── s3.tf
    ├── iam.tf
    ├── eks.tf
    ├── vpc.tf
    └── rds.tf
```

## Related

- [tfgen](https://github.com/refl3ction/tfgen) - The tool used in this example
- [tfenv](https://github.com/tfutils/tfenv) - Terraform version manager
