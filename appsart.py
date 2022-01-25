import sqlite3 as sql
import os
from modulart import *
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,jsonify

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/display')
def display():
    rows=list_artwork1()
    return render_template('display.html', rows=rows)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('admin.html')
    else:
        return render_template('home.html')
    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/login', methods=['POST'])
def dologin():
    if checklogin(request.form['username'],request.form['password']):
        session['logged_in'] = True
        session['username'] = request.form['username']
        return render_template('home.html')
    else:
        flash('wrong password!')
        return render_template('admin.html',message='Invalid Username or Password!')

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/search_artist',methods=['GET','POST'])
def find():
    if request.method=="POST":
        artist_id=request.form['artist_id']
        rows=find_artwork1(artist_id)
        return render_template('search_list.html',rows=rows)
    else:   
        return render_template('search.html')


@app.route('/new_artist')
def new_artist():
    row=['']*6
    status='0'
    return render_template('add_artist.html',row=row,status=status)


@app.route('/new_gallery')
def new_gallery():
    row=['']*4
    status='0'
    return render_template('add_gallery.html',row=row,status=status)


@app.route('/new_staff')
def new_staff():
    row=['']*2
    status='0'
    return render_template('add_staff.html',row=row,status=status)

@app.route('/new_artwork')
def new_artwork():
    row=['']*7
    status='0'
    artists=list_artist()
    gallerys=list_gallery()
    return render_template('add_artwork.html',row=row,status=status,artists=artists,gallerys=gallerys)

@app.route('/update_staff',methods=['GET','POST'])
def  insert_update_staff():
    username = request.form['username']
    password = request.form['password']
      
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*2
        row[0] = username
        row[1] = password
        if username == '' or password == '':
            msg = '';
            if username == '':
                msg += 'Username' if len(msg)==0 else ',Username'
            if name == '':
                msg += 'Password' if len(msg)==0 else ',Password'
            msg = msg + ' cannot be empty!';
            return render_template('add_staff.html',message=msg,status='0',row=row)
        else:
            if check_admin(username):
                row[0] = ''
                flash('Username already exist!')                
                return render_template('add_staff.html',message='Username '+artist_id+' already exist!',status='0',row=row)

            else:        
                insert_staff(username,password)        
                return redirect('/home') 
             
          
    if request.method=="POST" and request.form['status']=='1':
        update_staff(password,username)
        return redirect('/logout')

@app.route('/update_artist',methods=['GET','POST'])
def  insert_update_artist():
    artist_id = request.form['artist_id']
    artist_name = request.form['artist_name']
    artist_style = request.form['artist_style']
    birthplace = request.form['place']
    dob=request.form['dob']
    age=request.form['age']
      
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*6
        row[0] = artist_id
        row[1] = artist_name
        row[2] = artist_style
        row[3] = birthplace
        row[4] = dob
        row[5] = age
        if artist_id == '' or artist_name == '':
            msg = '';
            if artist_id == '':
                msg += 'Artist ID' if len(msg)==0 else ',Artist ID'
            if name == '':
                msg += 'Artist Name' if len(msg)==0 else ',Artist Name'
            msg = msg + ' cannot be empty!';
            return render_template('add_artist.html',message=msg,status='0',row=row)
        else:
            if check_artist_id(artist_id):
                row[0] = ''
                flash('Artist ID already exist!')                
                return render_template('add_artist.html',message='Artist ID '+artist_id+' already exist!',status='0',row=row)

            else:        
                insert_artist(artist_id,artist_name,artist_style,birthplace,dob,age)        
                return redirect('/artist_list') 
             
          
    if request.method=="POST" and request.form['status']=='1':
        update_artist(artist_name,artist_style,birthplace,dob,age,artist_id)
        return redirect('/artist_list')

@app.route('/update_gallery',methods=['GET','POST'])
def  insert_update_gallery():
    gallery_id = request.form['gallery_id']
    gallery_name = request.form['gallery_name']
    address = request.form['address']
    contact = request.form['contact']
      
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*4
        row[0] = gallery_id
        row[1] = gallery_name
        row[2] = address
        row[3] = contact
        if gallery_id == '' or gallery_name == '':
            msg = '';
            if gallery_id == '':
                msg += 'Gallery ID' if len(msg)==0 else ',Gallery ID'
            if gallery_name == '':
                msg += 'Gallery Name' if len(msg)==0 else ',Gallery Name'
            msg = msg + ' cannot be empty!';
            return render_template('add_gallery.html',message=msg,status='0',row=row)
        else:
            if check_gallery_id(gallery_id):
                row[0] = ''
                flash('Gallery ID already exist!')                
                return render_template('add_gallery.html',message='Gallery ID '+artist_id+' already exist!',status='0',row=row)

            else:        
                insert_gallery(gallery_id,gallery_name,address,contact)        
                return redirect('/gallery_list') 
             
          
    if request.method=="POST" and request.form['status']=='1':
        update_gallery(gallery_name,address,contact,gallery_id)
        return redirect('/gallery_list')
    

@app.route('/update_artwork',methods=['GET','POST'])
def insert_update_artwork():
    artwork_id = request.form['artwork_id']
    title = request.form['title']
    artwork_type = request.form['artwork_type']
    year=request.form['year']
    artist_id=request.form['artist_id']
    gallery_id=request.form['gallery_id']
    picture=request.files['picture']
    
    target = os.path.join(APP_ROOT, 'static/artwork/')
    print(target)
    
    for file in request.files.getlist("picture"):
        print(file)
        filename = str(file.filename)
        extension=filename.split(".")
        extension=str(extension[1])
        new_name = artwork_id+"."+extension
        destination = "/".join([target,new_name])
        print(destination)
        file.save(destination)
        picture_name = new_name
        
        if request.method=='POST' and request.form['status']=='0':
            insert_artwork(artwork_id,title,artwork_type,year,artist_id,gallery_id,picture_name)
            
    return redirect('/artwork_list')
    
    #if request.method=="POST" and request.form['status']=='1':
        
        #update_grade(id,nomatrik,kod_subjek,markah,gred,mata_nilai)
        #return redirect('/list_grade')

@app.route('/edit_artist/<artist_id>')
def edit_artist(artist_id): 
    row=find_artist(artist_id)
    status='1'
    return render_template('add_artist.html',row=row,status=status)


@app.route('/delete_artist/<artist_id>')
def delete_artists(artist_id):  
     delete_artist(artist_id)
     return redirect('/artist_list')
    
@app.route('/edit_gallery/<gallery_id>')
def edit_gallery(gallery_id): 
    row=find_gallery(gallery_id)
    status='1'
    return render_template('add_gallery.html',row=row,status=status)


@app.route('/delete_gallery/<gallery_id>')
def delete_gallerys(gallery_id):  
     delete_gallery(gallery_id)
     return redirect('/gallery_list')
    
    
@app.route('/edit_artwork/<artwork_id>')
def edit_artwork(artwork_id): 
    row=find_artwork(artwork_id)
    status='1'
    return render_template('add_artwork.html',row=row,status=status)


@app.route('/delete_artwork/<artwork_id>')
def delete_artworks(artwork_id):  
     delete_artwork(artwork_id)
     return redirect('/artwork_list')

@app.route('/reset_password/<username>')
def reset_password(username): 
    row=find_staff(username)
    status='1'
    return render_template('add_staff.html',row=row,status=status)

@app.route('/artist_list')
def list_artists():
    rows=list_artist()
    return render_template('artist_list.html', rows=rows)


@app.route('/gallery_list')
def list_gallerys():
    rows=list_gallery()
    return render_template('gallery_list.html', rows=rows)


@app.route('/artwork_list')
def list_artworks():
    rows=list_artwork()
    return render_template('artwork_list.html', rows=rows)

if __name__ == "__main__":
    app.secret_key = "!mzo53678912489"
    app.run(debug=True,host='0.0.0.0', port=5000)
