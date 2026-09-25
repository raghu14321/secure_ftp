#lib
import subprocess,socket
from cryptography.fernet import Fernet
from datetime import datetime
#######################################################################################################
def set_user_pass_to_auth1():
    usernmae = input("enter username:-")
    password = input("enter password:-")
    with open("database_file.txt",'w')as file_in_username_password:
        file_in_username_password.write(f"""{usernmae}
{password}
""")
def check_username_password_exist_or_not():
    check_username_password = subprocess.check_output(["dir"],shell=True)
    decode_check_username_password = check_username_password.decode()
    if "database_file.txt" in decode_check_username_password:
        pass
    else:
        set_user_pass_to_auth1()
check_username_password_exist_or_not()
#####################################################################################################
def check_client_username_password_(user_name_user,password_pass):
    with open("database_file.txt", "r") as f:
        var1 = f.readline().strip()
        var2 = f.readline().strip()
    if user_name_user == var1:
        if password_pass == var2:
            return "valid user"
    else:
        return "not valid"  

######################################################################################################

buffer_size = 30 * 1024 * 1024
server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.bind(("0.0.0.0",5050))
server_connection.listen(1)
print("server listening on port 5050")
connection,address = server_connection.accept()
######################################################################################    
def encrypt_data(data):
    key = b'yfwtTSCIL_l1Nfn6M1WVUlOkjnyii39nNkw_wQ8W-fg=' #change the keys
    f = Fernet(key)
    encrypts = f.encrypt(data)
    return encrypts
def decrypt_data(data1):
    key1 = b'yfwtTSCIL_l1Nfn6M1WVUlOkjnyii39nNkw_wQ8W-fg=' # change the keys
    f1 = Fernet(key1)
    decrypts = f1.decrypt(data1)
    return decrypts
######################################################################################
#######################################################################################
def read_file(file_name):
    with open(file_name,'rb')as readfile:
        reading = readfile.read()
        return reading
def write_file(file_content_write,content):
    with open(file_content_write,'wb')as writefile:
        writefile.write(content)
        return "[+]file uploads successfully"
#####################################################################################
def check_file_exist_or_not(file_name_ext):
    file_exist_or_not = subprocess.check_output(["dir"],shell=True)
    decode_ls_result = file_exist_or_not.decode()
    if file_name_ext in decode_ls_result:
        return "ok"
    else:
        return "file_not_found"
######################################################################################   
def execute_ls_command():
    execute_command = subprocess.check_output(["dir"],shell=True)
    return execute_command
def exeute_shell_commands(shell_command):
    try:
        execshell = subprocess.check_output([shell_command],shell=True)
        return execshell
    except Exception:
        pass
with open("server_log",'a')as server_log:
    server_log.write(f"""LOG_FILE
{datetime.now()} => ip_address{address}
""")
########################################################################################################
#extra functionalitites
def change_directory(path):
    pass
def recv_user_pass():
    user_recv = connection.recv(buffer_size)
    pass_recv = connection.recv(buffer_size)
    user_rev_decrypt = decrypt_data(user_recv)
    pass_recv_decrypt = decrypt_data(pass_recv)
    user_rev_decrypt_decode = user_rev_decrypt.decode()
    pass_recv_decrypt_decode = pass_recv_decrypt.decode()
    return_response1 = check_client_username_password_(user_rev_decrypt_decode,pass_recv_decrypt_decode)
    if return_response1 == "valid user":
        token_valid = "valid".encode()
        token_send = encrypt_data(token_valid)
        connection.sendall(token_send)
    elif return_response1 == "not valid":
        flase_token = "not valid".encode()
        not_valid_token = encrypt_data(flase_token)
        connection.sendall(not_valid_token)
        connection.close()
recv_user_pass()      
try:
    def main():
        while True:
            command = connection.recv(buffer_size)
            decrypt_command = decrypt_data(command)        
            decrypt_command_decode = decrypt_command.decode()
            #print(decrypt_command_decode)
            _lenth_ = decrypt_command_decode.split()
            lenth_1 = len(_lenth_)
            if lenth_1 == 1:
                if decrypt_command_decode == "exit": # # # # # # # # # #
                    connection.close()
                    break
                elif decrypt_command_decode == "ls":
                    execute = execute_ls_command()
                    send_command_data = encrypt_data(execute)
                    connection.sendall(send_command_data)
                    continue
                continue
            if lenth_1 == 2:
                if "upload" in decrypt_command_decode or "Upload" in decrypt_command_decode:
                    upload_file_list = connection.recv(buffer_size)
                    upload_file_list1 = decrypt_data(upload_file_list)
            ##################################################### create file
                    server_write_here = decrypt_command_decode.split()
                    server_write_here1 = server_write_here[1]
                    write_file(server_write_here1,upload_file_list1)
                    upload_file_list2 = upload_file_list1.decode()
                #print(upload_file_list2)
                    pass
                elif "download" in decrypt_command_decode or "Download" in decrypt_command_decode:
                    listing = decrypt_command_decode.split()
                    lisitng1 = listing[1]
                    return_check_result = check_file_exist_or_not(lisitng1)
                    if return_check_result == "ok":
                        read_data = read_file(lisitng1)
                        encrypt_read_data = encrypt_data(read_data)
                        connection.sendall(encrypt_read_data)
                        pass
                    elif return_check_result == "file_not_found":
                        massg = "file not found".encode()
                        massg1 = encrypt_data(massg)
                        connection.sendall(massg1)
                        pass
                    pass
                elif "shell" in decrypt_command_decode or "SHELL" in decrypt_command_decode:
                    shell = decrypt_command_decode
                    shell1 = shell.split()
                    shell123 = shell1[1]
                    shell3 = exeute_shell_commands(shell123)
                    encrypt_shell_data = encrypt_data(shell3)
                    connection.sendall(encrypt_shell_data)
                    pass
                pass
            else:
                continue
except Exception:
    pass
main()