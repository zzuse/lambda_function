# AWS Lambda Service For Weather and Gas Price 

## What 
query Weather and Gas and send messages to Telegram

## Limitation
This Project only for personal study, using by your own risk. 

## Need package and deploy to AWS lambda
1. git clone https://github.com/zzuse/lambda_function.git
2. Go inside crated root folder
% cd lambda_function
3. Create entry point Python file for AWS Lambda.
% vi lambda_function.py
4. Change code in lambda_function.py
add some Bot token
remove last __name__ == '__main__': part
5. Install requests and bs4 library. Note:package folder created
% pip install --target ./package requests bs4
6. Go inside package
% cd package
7. Zip package
zip -r ../deployment-package.zip .
8. Go into parent folder
% cd ..
9. Zip deployment packge and lambda function file
% zip -g deployment-package.zip lambda_function.py
In the AWS Lambda functions tap "Upload from" and pick ".zip file". Navigate to your zip package zip file: deployment-package.zip.
After upload all files will be inside AWS Lambda function.
10. add EventBridge to trigger the job
EventBridge (CloudWatch Events): Periodic
Schedule expression [every hour]: cron(0 0/1 * * ? *)
