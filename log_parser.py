# -*- coding: utf-8 -*-
import paramiko
import os
import time

def replace_selected_elements(where, what, than):
    for item in what:
        where = where.replace(item, than)
    return where

def main():
    #  king of pigs
    king_of_pigs = "\
 ######################@%%%%#######################\n \
#####################%%%%%%%%#####################\n \
####################%%%%%%%%%%####################\n \
###################%%%%%%%%%%%%###################\n \
##################%%%%%%.:%%%%%%##################\n \
################%%%%%%%.  -%%%%%%#################\n \
###############%%%%%%=.    .%%%%%%%###############\n \
##############%%%%%%+ *####:.=%%%%%%##############\n \
#############%%%%%%*  +####+  +%%%%%@#############\n \
############%%%%%%:   *####*   *%%%%%%############\n \
##########%%%%%%%-    :####:    -%%%%%%###########\n \
#########%%%%%%%.     .####-     .%%%%%%##########\n \
########%%%%%%=.       ####.      .%%%%%%%########\n \
#######%%%%%%+         @###         =%%%%%@#######\n \
######%%%%%%*          -@@-          *%%%%%%######\n \
#####%%%%%%:           .+=:           :%%%%%%#####\n \
###%%%%%%%-           -####=           -%%%%%%####\n \
##%%%%%%%.             *##%.            .%%%%%%%##\n \
#%%%%%%%-........-------------------------%%%%%%%#\n \
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n \
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n \
\n \
"
    if os.path.exists(str(os.getcwd()) + '/logs/') == False: 
        print 'ERROR: Folder "logs" not found! \n You can create a folder with the following command: mkdir logs'
        return None
    # setup
    first_iter = True
    logfile_list = list()
    logfile_list_old = list()
    found_error = False
    # settings
    # chosen server
    SERVER_LIST = ["0.0.0.0", "0.0.0.1", "0.0.0.2"] #add or delete server
    user = 'YOUUSERS'.decode('utf-8')
    secret = 'SUPERSECRET'.decode('utf-8')
    port = 22
    # text error for search
    TEXT_FOR_SEARCH = ['some text', 'some text1']
    # some text for stoping read from logfile
    LIST_WITH_TEXT_FOR_STOP = ['final text', 'final text 2']
    # where we want found something?
    DICT_WITH_SERVER = {
                        '0.0.0.0': ['path/to/logs/log1.log', 
                                    'path/to/logs/log2.log'], 
                        '0.0.0.1': ['path/to/logs/log1.log', 
                                    'path/to/logs/log2.log'],
                        '0.0.0.2':  ['path/to/logs/log1.log', 
                                    'path/to/logs/log2.log']
                        }
    # frequency give logfiles from server in seconds
    TIME_FOR_SLEEP = 1
    # time for read error
    SLEEP_FOR_READ = 0
    # quantity string of context
    context = 2
    # dont touch!
    # context += 1
    LIST_WITH_WHAT = ["'", "[", "]"]

    while (True):
        print ('Start work!')
        for ip in SERVER_LIST:
            print 'Server: ', ip

            # if connection is lost, then pass the iteration
            try: 
                list_with_path_to_file = DICT_WITH_SERVER[ip]
                transport = paramiko.Transport((ip, port))
                transport.connect(username=user, password=secret)
                sftp = paramiko.SFTPClient.from_transport(transport)

            except paramiko.ssh_exception.SSHException:
                print 'Cannot connect to server! ', ip
                continue
                
            for file_path in list_with_path_to_file:
                # set name for files
                name_logfiles = file_path.split('/')
                name_logfiles = str(name_logfiles[-1:]) + '_from_' + ip + '.txt'
                name_logfiles = replace_selected_elements(name_logfiles, LIST_WITH_WHAT, '')
                name_parser_logfiles = 'parser_logfile_for_' + ip + '.txt'

                path_local = str(os.getcwd()) + '/logs/' + name_logfiles
                path_to_logs_parser = os.getcwd() + '/logs/' + name_parser_logfiles
                
                print "Parsing file: ", file_path
                # save to current dir
                 
                if first_iter == False:
                    logfile = open(path_local, 'r')  # open file for read
                    for line in logfile:
                        logfile_list_old.append(line)
                    logfile.close()

                # get logfile
                try:
                    sftp.get(file_path, path_local)
                except IOError: 
                    print 'file not found!', ip, file_path

                # work with log file
                logfile = open(path_local, 'r')  # open file for read
                output = open(path_to_logs_parser, 'a')  # open file for write
                i, j, x = [0,0,0]
                mode = 'R'

                list_with_index_for_write = list()
                
                for line in logfile:
                    logfile_list.append(line)
                logfile.close()
               
                count = 0
                if first_iter == False:
                    count = len(logfile_list) - len(logfile_list_old) 
                    if count == 0:
                        print 'I did not find any new errors in the file!'
                        continue
                    else:
                        print 'Try to catch something..'
                        logfile_list = logfile_list[-count:]

                for line in logfile_list:
                    if mode == 'R':
                        for element in TEXT_FOR_SEARCH:
                            if element in line:
                                found_error = True
                                mode = 'RW'
                                if i - context < 0: j = 0
                                else: j = i - context
                                string_for_out = '\n TIME: ' + time.strftime('%A %B %d -- %H:%M') + ' \n I FOUND ERROR: ' + line + ' ON TEMPLATE: ' + element + '\n IN STRING NUMBER: ' + str(i+2) +' \n ON SERVER: ' + ip + ' \n IN FILELOGS: ' + file_path  + ' \n TEXT ERROR: '
                                
                                print '\n TIME: ' + time.strftime('%A %B %d -- %H:%M') +  ' \n I FOUND ERROR: ' + line + ' ON TEMPLATE: ' + element + '\n IN STRING NUMBER: ' + str(i+2) +' \n ON SERVER: ' + ip + ' \n IN FILELOGS: ' + file_path
                        
                    if mode == 'RW':
                        for element in LIST_WITH_TEXT_FOR_STOP:
                            if element in line:
                                mode = 'R'
                                if i + context > len(logfile_list): list_with_index_for_write.append([j, i, string_for_out])
                                else: list_with_index_for_write.append([j, i + context, string_for_out])
                                break;
                    i += 1
                i = 0
                try:
                    list_with_index_for_write[len(list_with_index_for_write)-1][1] -= 1
                except IndexError:
                    pass
                for line in list_with_index_for_write:
                    print king_of_pigs
                    print ' ', time.strftime('Time: %H:%M')
                    print line[2]
                    output.write(line[2])
                    for index in range(line[0],line[1]):
                        output.write(logfile_list[index])
                        print logfile_list[index]
                    if first_iter == False and found_error: time.sleep(SLEEP_FOR_READ)
                output.close()
                list_with_index_for_write = [];
                logfile_list = []
                logfile_list_old = []
            sftp.close()
            transport.close()
        first_iter = False
        if found_error == False:
            print '\nI did not find any new errors in the iteration!'
        else: 
            print '\nI found an error!'
        found_error = False
        print ('\nAll done! I will sleep next '+ str(TIME_FOR_SLEEP) +'  seconds' + '\n')
        time.sleep(TIME_FOR_SLEEP)
        
if __name__ == "__main__":
    main()
