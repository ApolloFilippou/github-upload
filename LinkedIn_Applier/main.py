import LinkedIn_Applier

username = 'apollonasfilippou@gmail.com'
password = 'Apocloud_88'
job_title = 'Data Scientist'
city = 'Worldwide'
location = 'Worldwide&locationId=OTHERS.worldwide'
driver_path = r'C:\Users\Apollo\PycharmProjects\LinkedIn_Applier\chromedriver.exe'
phone = '+447944878339'
resume_path = r'C:\Users\Apollo\Google Drive\CV\Apollo Filippou.pdf'


if __name__ == '__main__':
    apply = LinkedIn_Applier.LinkedIn_Applier(username=username, password=password, job_title=job_title, city=city,
                                              driver_path=driver_path, phone=phone, resume_path=resume_path)
    apply.init_driver()
    apply.login()
    apply.search_jobs()
