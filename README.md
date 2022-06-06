![site ui](https://user-images.githubusercontent.com/37404377/171172028-ba705199-dbad-4a3b-8acd-27b4a61b63eb.jpg)


# AnimeCart
- You can visit this site here (Deployed on Heroku):
https://animecart.herokuapp.com/

- AnimeCart is an E-Commerce Website for anime fans. Where fans can buy clothes and merchandises of anime.


To run this project in your local system, follow below steps: 

1. Clone the repo into your local machine/system
2. Run the project by typing this command:
   `python manage.py runserver`
3. To access admin panel:
   - First create the superuser by typing below commands:
   - `python manage.py createsuperuser`
   - Give any username and password you want.
   - Now, run the server again. `python manage.py runserver`
   
   go to `http://127.0.0.1:8000/admin/`
   - username: your_admin_username
   - password: your_admin_password

Features of the site:
- Anime Cart is an E-Commerce website fully integrated with PayPal payment sysyem.
- Customer can visit the site without login/register but to buy stuff he/she has to login/register first.
- Users can add items to the cart and checkout whenever then they want to buy.
