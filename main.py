import os
import shutil
import boto3
import re

client = boto3.client('lambda')
def main():
    allowed_languages = ['python','go']
    project_name = input("project name: ")
    project_location = input("project location: ")
    
    language = input(f"language (choose one): {allowed_languages}\n")
    
    if language not in allowed_languages:
        print(f"language must be in list: {allowed_languages}")
        os.abort()
    
    create_lambda = input("create lambda in AWS? (y/n)").lower()

    if create_lambda == 'y':
        create_lambda = True
        deploy_lambda(language, project_name)
    elif create_lambda == 'n':
        create_lambda = False
    else:
        print("response must be y or n")
        os.abort()
    
    create_project(language, project_name, project_location, create_lambda)

def create_project(language, project_name, project_location, create_lambda):
    if language == 'python':
        template = "./python_template/"
    elif language == 'go':
        template = './go_template/'
    else:
        return
    full_file_location = f'{project_location}\{project_name}\{template}'
    
    shutil.copytree(src=template,dst=full_file_location)

    # Replace {PROJECT_NAME} with user input 

    # replace in .gitlab-ci.yml file
    with open(f'{full_file_location}\.gitlab-ci.yml', 'r+' ) as fp:
        text = fp.read()
    new_text = re.sub(r"()\bPROJECT_NAME\b(.*)", project_name, text)
    with open(f'{full_file_location}\.gitlab-ci.yml', 'w') as fp:
        fp.write(new_text)

    # replace in global terraform file (IAM)
    with open(f'{full_file_location}\modules\global\main.tf', 'r+' ) as fp:
        text = fp.read()
    new_text = re.sub(r"()\bPROJECT_NAME\b(.*)", project_name, text)
    with open(f'{full_file_location}\modules\global\main.tf', 'w') as fp:
        fp.write(new_text)

    # replace in regional terraform file 
    with open(f'{full_file_location}\\modules\\regional\\main.tf', 'r+' ) as fp:
        text = fp.read()
    new_text = re.sub(r"()\bPROJECT_NAME\b(.*)", project_name, text)
    # if a lambda was requested replace {LAMBDA_NAME} with user input
    if create_lambda:
        new_text = re.sub(r"()\bLAMBDA_NAME\b(.*)", project_name, new_text)
    with open(f'{full_file_location}\\modules\\regional\\main.tf', 'w') as fp:
        fp.write(new_text)
    


def deploy_lambda(language, lambda_name):
    
    if language == 'python':
        runtimes = 'python3.10'
        deployment_package = './python_template/main.zip'
    elif language == 'go':
        runtimes = 'provided.al2'
        deployment_package = './go_template/main.zip'
    print(deployment_package)
    
    with open(deployment_package, 'rb') as f:
        zipped_code=f.read()

    # zip_file = io.BytesIO(deployment_package)

    response = client.create_function(
        FunctionName=lambda_name,
        Runtime=runtimes,
        Role='arn:aws:iam::488975269863:role/send-events',
        Handler='main.lambda_handler',
        Code={"ZipFile": zipped_code},
        Description='TEMPLATE',
        Timeout=5,
        MemorySize=128,
        Publish=True,
        PackageType='Zip',
        Architectures=[
            'x86_64',
        ],
        EphemeralStorage={
            'Size': 512
        },
    )
    print(response)
    

if __name__ == "__main__":
    main()