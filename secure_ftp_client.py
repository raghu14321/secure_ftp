#lib
import subprocess,socket,os
from cryptography.fernet import Fernet
buffer_size = 30 * 1024 * 1024
client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("enter server_ip:-")
ip1 = str(ip)
client_connection.connect((ip1,5050))
def encrypt_data(data):
    key = b'yfwtTSCIL_l1Nfn6M1WVUlOkjnyii39nNkw_wQ8W-fg='
    f = Fernet(key)
    encrypts = f.encrypt(data)
    return encrypts
def decrypt_data(data1):
    key1 = b'yfwtTSCIL_l1Nfn6M1WVUlOkjnyii39nNkw_wQ8W-fg='
    f1 = Fernet(key1)
    decrypts = f1.decrypt(data1)
    return decrypts
#######################################################################################
def list_split(files_name):
    files = files_name.split()
    files1 = files[1]
    files12 = str(files1)
    return files12
####################################################################################
def read_file(file_name):
    with open(file_name,'rb')as readfile:
        reading = readfile.read()
        return reading
def write_file(file_name1,content):
    with open(file_name1,'wb')as writefile:
        writefile.write(content)
        return "[+]ok"
#####################################################################################
def check_file_exist_or_not(file_name_ext):
    file_exist_or_not = subprocess.check_output("dir",shell=True)
    decode_ls_result = file_exist_or_not.decode()
    if file_name_ext in decode_ls_result:
        return "ok"
    else:
        return "file_not_found"
def current_file():
    current_files = subprocess.check_output("dir",shell=True)
    decode_current_files = current_files.decode()
    print(decode_current_files)
def send_user_pass_to_auth1():
    username = input("enter username:-").encode()
    password = input("enter password:-").encode()
    enc_user1 = encrypt_data(username)
    enc_password = encrypt_data(password)
    client_connection.sendall(enc_user1)
    client_connection.sendall(enc_password)
    response_from_server = client_connection.recv(buffer_size)
    response_from_server_dec = decrypt_data(response_from_server)
    response_from_server_decode = response_from_server_dec.decode()
    if response_from_server_decode == "valid":
        pass
    elif response_from_server_decode == "not valid":
        print("[-]username password incorrect")
        connection.close()
        exit()
    else:
        pass
    
send_user_pass_to_auth1()
######################################################################################   
def main():
    while True:
        files_name_1 = input("1.upload <file name> 2.download <file name> >>>>>>>>>>>")
        filters = files_name_1.split()
        filter_lenth = len(filters)
        if filter_lenth == 1:
            if files_name_1 == "exit":
                exit_send = files_name_1.encode()
                exit_send1 = encrypt_data(exit_send)
                client_connection.sendall(exit_send1)
                client_connection.close()
                break
            elif files_name_1 == "ls":
                enc = files_name_1.encode()
                send_result = encrypt_data(enc)
                client_connection.sendall(send_result)
                recv_result = client_connection.recv(buffer_size)
                dec = decrypt_data(recv_result)
                dec_1 = dec.decode()
                print(dec_1)
                continue
            elif files_name_1 == "help":
                print("""1.current files < current files in your local storage >    2.exit   3.ls <list files in server> \n 4.upload  <upload file in server> 5.download <download file from server> 6.shell <shell access run commands> """) 
                continue
        elif filter_lenth == 2:
            if files_name_1 == "current files":
                current_file()
                continue
            elif "upload" in files_name_1 or "Upload" in files_name_1:
                list_files_upload_server = files_name_1.split()
                list_files_upload_server1 = list_files_upload_server[1]
                print(list_files_upload_server1)
                file_valid_check_out = check_file_exist_or_not(list_files_upload_server1)
                if file_valid_check_out == "ok":
                    encode_file_name_1 = files_name_1.encode()
                    list_files_upload_server12 = encrypt_data(encode_file_name_1)
                    client_connection.sendall(list_files_upload_server12)
                    _readFile_ = read_file(list_files_upload_server1)
                    _readFile_1 = encrypt_data(_readFile_)
                    client_connection.sendall(_readFile_1)
                    print(f"{list_files_upload_server1} file upload successfully")
                    continue
                elif file_valid_check_out == "file_not_found":
                    print("[-]file not found")
                    continue
                continue
            elif "download" in files_name_1 or "Download" in files_name_1:
                Download_frome_server = files_name_1.encode()
                Download_frome_server1 = encrypt_data(Download_frome_server)
                client_connection.sendall(Download_frome_server1)
                get_data = client_connection.recv(buffer_size)
                decrypt_data_get_data = decrypt_data(get_data)
                check_out_file_content = decrypt_data_get_data.decode()
                if check_out_file_content == "file not found":
                    print("file not found")
                    continue
                else:
                    #print(decrypt_data_get_data)
                    file_names = files_name_1.split()
                    file_namesss1 = file_names[1]
                    file_response = write_file(file_namesss1,decrypt_data_get_data)
                    print(file_response)
                    continue
            elif "shell" in files_name_1 or "SHELL" in files_name_1:
                shell_command = files_name_1.encode()
                shell_command_1 = encrypt_data(shell_command)
                client_connection.sendall(shell_command_1)
                shell_command_recv = client_connection.recv(buffer_size)
                shell_decrypt = decrypt_data(shell_command_recv)
                shell_command_decode = shell_decrypt.decode()
                print(shell_command_decode)
            else:
                continue
            continue
main()
        




