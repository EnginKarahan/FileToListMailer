# FileToListMailer
 
FileToListMailer is a little Python script for mailing an PDF attachment. The script ist looking into a folder for a file with a specific beginning. If there is no such file, the sript terminates. If there is a matching file, part of the filename is used as mail subject. The File is used as an attachment. The list of mails is saved in a csv-file. The body-text in a markdown file. The mail is send via SMTP. After sending the mail, the attachment-file is moved into the Archive. 

#Python #Mailing #attachment #bcc 

## License
This software is licensed via the [GNU GPL v3-License](https://www.gnu.org/licenses/gpl-3.0.en.html).