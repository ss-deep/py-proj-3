from flask import Flask, render_template, redirect, flash, request, session,url_for
import jinja2
from melons import all_melons,find_melon
from forms import LoginForm
import customers

app=Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined  # for debugging purposes

app.secret_key = 'dev'

@app.route('/')
def homepage():
   return render_template("base.html")

@app.route("/login", methods=['GET','POST'])
def login():
   username=""
   form=LoginForm(request.form)
   if form.validate_on_submit():
      username=form.username.data
      password=form.password.data
      form.username.data=''
      customer=customers.get_by_username(username)
      if customer and customer['password']==password:
         session['username']=username
         flash('Logged In')
         return redirect('/all-melons')
      else:
         flash('Invalid username or password')
   return render_template('login.html', form=form)

@app.route('/logout')
def logout():
   del session['username']
   session['cart']={}
   flash('Sucessfully logged out.')
   return redirect('/login')
                   
@app.route('/all-melons')
def get_all_melons():
   melon_list=all_melons()
   return render_template("all-melons.html",melon_list=melon_list)

@app.route('/melon/<melon_id>')
def melon_details(melon_id):
   return render_template("melon_details.html", melon=find_melon(melon_id))

@app.route('/add_to_cart/<melon_id> ')
def add_to_cart(melon_id):
   if 'cart' not in session:
      session['cart']={}
   cart = session['cart']  
   cart[melon_id] = cart.get(melon_id, 0) + 1
   session.modified=True

   if 'username' not in session:
      return redirect('/login')
   flash(f"Melon {melon_id} successfully added to cart.")
   return redirect("/cart")

@app.route('/cart')
def cart():
   if 'username' not in session:
      return redirect('/login')
   order_total = 0
   melons_list = []

   if 'cart' not in session:
      session['cart']={}

   for melon_id,qty in session['cart'].items():
      melon=find_melon(melon_id)
      order_total+=qty*melon.price
      melon.quantity=qty
      melon.total_cost=qty*melon.price
      melons_list.append(melon)
   return render_template("cart.html",melons_list=melons_list,order_total=order_total)

@app.route("/remove_melon/<melon_id>")
def remove_melon(melon_id):
   session.modified=True
   if session['cart'][melon_id]>1:
      session['cart'][melon_id]-=1
   else:
      session['cart'].pop(melon_id)
   return redirect('/cart')

@app.route("/empty-cart")
def empty_cart():
   session['cart']={}
   return redirect('/cart')

@app.errorhandler(404)
def error_404(e):
   return render_template('404.html')

if __name__ == "__main__":
   app.env = "development"
   app.run(debug = True, port = 8000, host = "localhost")