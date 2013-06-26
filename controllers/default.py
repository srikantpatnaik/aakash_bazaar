import os

rows = db(db.developer).select() 
packages=db(db.package).select()

def generateMeta():
    for each in rows:
        with open(returnPath()+'.txt' , 'w') as f:
            f.write('Category: %s\n' %(each.Category))
            f.write('License: %s\n' %(each.License))
            f.write('Web Site: %s\n' %(each.Web_Site))
            f.write('Source Code: %s\n' %(each.Source_Code))
            f.write('Issue Tracker: %s\n\n' %(each.Issue_Tracker))
            f.write('Summary:%s\n' %(each.Summary))
            f.write('Description:\n%s\n.\n\n' %(each.Description))
            f.write('Update Check Mode:Market\n\n')


def returnPath():
    for each in packages:
        if each.user_id==str(auth.user_id):
            package_path=os.getcwd() + '/applications/aakash_bazaar/uploads/' + each.Package_name
            if not os.path.exists(package_path):
                os.makedirs(package_path)  
    return package_path       
    

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
    upload_form = SQLFORM.factory(
           Field('Upload_apk', 'upload', uploadfolder=returnPath() ,requires=IS_NOT_EMPTY()),
           Field('Screenshot1', 'upload', uploadfolder=returnPath(), requires=IS_NOT_EMPTY()),
           Field('Screenshot2', 'upload', requires=IS_NOT_EMPTY()),
           Field('Screenshot3', 'upload', requires=IS_NOT_EMPTY()), )                   
    if upload_form.process().accepted:
        response.flash = 'record inserted'
        redirect(URL('complete'))             
    return dict(upload_form=upload_form)          

                              
@auth.requires_login()
def complete():
    generateMeta()
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
