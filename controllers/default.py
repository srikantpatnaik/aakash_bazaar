# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################



import os
import shutil

rows = db(db.developer).select() 
packages = db(db.package).select()
relative_path = os.getcwd() + '/applications/aakash_bazaar/uploads/'

def generateMeta():
    for each in rows:
        with open(returnPath()+'.txt' , 'w') as f:
            f.write('Category: %s\n' %(each.Category))
            f.write('License: %s\n' %(each.License))
            f.write('Web Site: %s\n' %(each.Web_Site))
            f.write('Source Code: %s\n' %(each.Source_Code))
            f.write('Issue Tracker: %s\n\n' %(each.Issue_Tracker))
            f.write('Summary:%s\n' %(each.Summary))
            f.write('Description:\n%s\n\n' %(each.Description))
            f.write('Changelog - \n%s\n. \n\n' %(each.Changelog))
            f.write('Update Check Mode:Market\n\n')



def returnPath():
    for each in packages:
        if each.user_id == str(auth.user_id):
            package_path = relative_path + each.Package_name
            if not os.path.exists(package_path):
                os.makedirs(package_path)  
    return package_path       
    
    
def deletePath():
    for each in packages:
        if (each.user_id==str(auth.user_id) and os.path.exists(relative_path + each.Package_name)):
            shutil.rmtree(relative_path + each.Package_name)
            
    
def renameFiles():
    count=1
    for each in packages:
        if each.user_id == str(auth.user_id):
            package_name = each.Package_name            
    for each in rows:
        if each.user_id == str(auth.user_id):
            list_of_files=os.listdir(relative_path + package_name)
            apk_name = each.Name_of_the_apk            
    for each in list_of_files:
        print list_of_files
        if '.png' in each:            
            shutil.move(relative_path + package_name + '/' + each,\
            relative_path + package_name + '/' + package_name + '.' + str(count) +'.png')
            count=count+1                   
        if '.apk' in each: 
            shutil.move(relative_path + package_name + '/' + each,\
                        relative_path + '/' + apk_name + '.apk')
                    
            

@auth.requires_login()
def index():
    form_package = SQLFORM(db.package)
    if form_package.process().accepted:
        response.flash = 'record inserted'
        redirect(URL('developer'))
    return dict(form_package=form_package)          
    

@auth.requires_login()
def developer():
    form = SQLFORM(db.developer)
    if form.process().accepted:
        response.flash = 'record inserted'
        redirect(URL('upload'))      
    return dict(form=form)


@auth.requires_login()
def upload():
    deletePath()                             
    upload_form = SQLFORM.factory(
           Field('Upload_apk' , 'upload', uploadfolder=returnPath(), requires=IS_NOT_EMPTY()),
           Field('Screenshot1', 'upload', uploadfolder=returnPath(), requires=IS_NOT_EMPTY()),
           Field('Screenshot2', 'upload', uploadfolder=returnPath()),
           Field('Screenshot3', 'upload', uploadfolder=returnPath()))                   
    if upload_form.process().accepted:
        response.flash = 'record inserted'
        redirect(URL('complete'))             
    return dict(upload_form=upload_form)          

                              
@auth.requires_login()
def complete():
    generateMeta()
    renameFiles()
    return dict(done=T('Congratulations %(first_name)s. \n \
                    Your app and screenshots will be reviewed, and would appear within 24 hours' %auth.user))


def user():
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
