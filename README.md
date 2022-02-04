# Python3 function that clones git repository(repositories) and archives it on S3 Bucket

### Lambda configuration
Add layer with installed git, so function can work with git commands:

```arn:aws:lambda:us-east-1:553035198032:layer:git-lambda2:8```

### Add policy to lambda execution role
To allow lambda function put objects to S3 bucket you need to add this policy to current execution role:

```
{
    "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:AbortMultipartUpload"
    ],
    "Effect": "Allow",
    "Resource": [
        "arn:aws:s3:::$S3_BUCKET_NAME/*"
    ]
}
```

### Add policy to S3 bucket
Add policy to S3 bucket that allows lambda to put objects:

```
{
    "Version": "2012-10-17",
    "Id": "ExamplePolicy",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::$ACCOUNT_ID:$ROLE_NAME"
            },
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:AbortMultipartUpload"
            ],
            "Resource": "arn:aws:s3:::$S3_BUCKET_NAME/*"
        }
    ]
}
```
