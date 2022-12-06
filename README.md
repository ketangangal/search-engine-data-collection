# Embedding based Image Search Engine DataCollection
This Repository contains code for data collection which is required to train Embedding Based Image Search Engine.

# Architecture
![image](https://user-images.githubusercontent.com/40850370/194913612-69d32e6d-56b7-4b1b-a811-48c6c5b27f52.png)
![image](https://user-images.githubusercontent.com/40850370/194917419-ca176a45-bafb-4346-9942-cd59f042f33b.png)

## Actions Workflow 
1. On push checkout the code and create docker container on git-hub server.
2. Push the image to Ecr with production tag 
3. Once action push is completed pull and run the image on Ec2 instance.
![image](https://user-images.githubusercontent.com/40850370/189590432-7009c484-dcd6-4de4-8861-dd93d5eb1572.png)

## Git-hub Configurations
```text
1. Go to setting -> actions -> runner
2. Add runner/ec2 instance by using X86_64 arc
3. Add pages for github
4. Go to secrets tab -> Repository secrets and add secrets 
```
## Route Details 
![image](https://user-images.githubusercontent.com/40850370/189587344-4044f19a-2da7-495f-a482-3533fc362e74.png)

1. **/fetch**  : To get labels currently present in the database. Important to call as it updates in memory database.
2. **/Single_upload** : This Api Should be used to upload single image to s3 bucket
3. **/bulk_upload**   : This Api should be used to upload bulk images to s3 bucket
4. **/add_label** :  This api should be ued to add new label in s3 bucket.

## Infrastructure Details
- S3 Bucket 
- Mongo Database
- Elastic Container Registry
- Elastic Compute Cloud

## Steps
1. Create data folder 
2. Put archive.zip in data folder 
3. run s3 setup and mongo setup
4. Done

## To Replicate [ Requirements ]
```yaml
aws_cli:
  download: True
  configure: True
  
S3_Configurations:
  create_bucket: <bucket-name>
  region: <bucket-region>
  access: public-access [ To all the images ]

Mongo_configuration:
  mongo_url: <url-with-id-pass>

```
## Env variable

```bash

export ATLAS_CLUSTER_USERNAME=<username>
export ATLAS_CLUSTER_PASSWORD=<password>

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_REGION=<region>

export AWS_BUCKET_NAME=<AWS_BUCKET_NAME>
export AWS_ECR_LOGIN_URI=<AWS_ECR_LOGIN_URI>
export ECR_REPOSITORY_NAME=<name>

export DATABASE_NAME=<name>
```

## Cost Involved
- For s3 bucket    :  Since we are using S3 Standard `$0.023 per GB`
- For Ec2 Instance :  Since we are using t2.small with 20Gb storage 1vCpu and 2Gb ram `$0.0248 USD per hour`
- For Mysql : Since we are using `$db.t3.micro` Free tier.
- For ECR : Storage is $0.10 per GB / month for data stored in private or public repositories.
- Data Transfer IN  - All data transfer in	`$0.00 per GB`
- Data Transfer OUT - Next 9.999 TB / month	`$0.132 per GB`