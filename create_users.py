import pandas as pd
import paramiko

# Define the SSH connection details
hostname = 'your_linux_hostname'
username = 'ubuntu'
password = 'your_linux_password'
port = 22

# Load the Excel file with the user details
user_df = pd.read_excel('user_details.xlsx')

# Loop through each row in the DataFrame
for index, row in user_df.iterrows():
    # Extract the username and public key from the row
    username = row['Username']
    public_key = row['Public Key']
    
    # Connect to the remote Linux machine
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, pkeyusername=username, password=password)
    
    # Execute the commands to create the user and add the public key
    create_user_cmd = f'sudo adduser {username}'
    add_key_cmd = f'sudo su - {username} -c "mkdir .ssh; echo {public_key} >> .ssh/authorized_keys"'
    ssh_client.exec_command(create_user_cmd)
    ssh_client.exec_command(add_key_cmd)
    
    # Close the SSH connection
    ssh_client.close()
