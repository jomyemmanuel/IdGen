This repo is no longer maintained.

# IdGen

Web app to create ID card for college students and faculty developed using HTML, CSS, JQuery, Django Framework, Reportlab, SQLite. 

Users can input the relevant details, as a result of which a pdf form of the ID card is created. There are options to register, edit, search, delete, change template of id card and generate pdfs for both students and faculty.

[Demo Link](http://idgen.pythonanywhere.com/)
	
### Local Installation (Ubuntu)

1. `virtualenv .` ([virtualenv](https://www.caktusgroup.com/blog/2016/11/03/managing-multiple-python-projects-virtual-environments/))
2. `source bin/activate`
3. `pip install Django==1.9 reportlab`
4. `python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Usage

1. Register Details

![Register Details](https://user-images.githubusercontent.com/8125643/110128626-06383480-7ded-11eb-892a-9a1baffe2177.png)

2. Edit Template as per need

![Edit Template](https://user-images.githubusercontent.com/8125643/110128771-31bb1f00-7ded-11eb-9239-cba6ef95dcd0.png)

3. View List of registered users

![List](https://user-images.githubusercontent.com/8125643/110128796-38499680-7ded-11eb-8bae-619842bf6a94.png)

4. Download PDF

![Download PDF](https://user-images.githubusercontent.com/8125643/110128817-3c75b400-7ded-11eb-8a05-61719c5858ce.png)



